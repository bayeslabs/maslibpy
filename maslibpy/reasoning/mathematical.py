import logging
import torch
from typing import Union,Dict
from maslibpy.messages.user import UserMessage
from maslibpy.messages.assistant import AIMessage
from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoModelForCausalLM
from typing import List
from tqdm import tqdm
import numpy as np
import os
import time

logger = logging.getLogger(__name__)
LN_2 = np.log(2)

class Mathematical():
    @staticmethod
    def _softmax(x: np.ndarray) -> np.ndarray:
        """Compute softmax values for each set of logits."""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True) + 1e-8
    
    def __init__(self, use_gpu: bool = True, model_weights: dict = None):
        self.device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
        self.model_weights = model_weights or {'bert-base-cased': 0.4, 'roberta-base': 0.4, 'gpt2': 0.2}
        self.models = {}
        self._load_models()
        
    def _load_models(self):
        model_configs = [
            ('bert-base-cased', AutoModelForMaskedLM),
            ('roberta-base', AutoModelForMaskedLM),
            ('gpt2', AutoModelForCausalLM)
        ]
        for model_name, model_class in model_configs:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = model_class.from_pretrained(model_name).to(self.device).eval()
            self.models[model_name] = {'tokenizer': tokenizer, 'model': model}
        self.normalize_weights()
        
    def normalize_weights(self):
        """Normalize model weights so they sum to 1."""
        total_weight = sum(self.model_weights.values())
        for model in self.model_weights:
            self.model_weights[model] /= total_weight
            
    def _normalize_logits(self, logits: np.ndarray) -> np.ndarray:
        """Normalize logits using z-score."""
        mean = np.mean(logits, axis=-1, keepdims=True)
        std = np.std(logits, axis=-1, keepdims=True) + 1e-8
        return (logits - mean) / std

    def calculate_metrics(self, text: str) -> dict:
        """Calculate evaluation metrics based on logits and probabilities."""
        weighted_logits, weighted_probs = [], []
        for model_name, config in self.models.items():
            weight = self.model_weights[model_name]
            if not text.strip():
                logger.warning(f"Empty input text for {model_name}")
                continue
            if model_name == 'gpt2':
                    config['tokenizer'].pad_token = config['tokenizer'].eos_token
                    config['model'].config.pad_token_id = config['model'].config.eos_token_id
            inputs = config['tokenizer'](text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(self.device)
            with torch.no_grad():
                logits = config['model'](**inputs).logits.cpu().numpy()
                logits = self._normalize_logits(logits)
                probs = self._softmax(logits)
                weighted_logits.append(logits * weight)
                weighted_probs.append(probs * weight)
        return self._compute_metrics(weighted_logits, weighted_probs)
    
    def _compute_metrics(self, weighted_logits: list, weighted_probs: list) -> dict:
        """Compute entropy, perplexity, and coherence from weighted logits and probabilities."""
        if not weighted_logits or not weighted_probs:
            return self._fallback_metrics()

        target_shape = weighted_logits[0].shape
        weighted_logits = [x for x in weighted_logits if x.shape == target_shape]
        weighted_probs = [x for x in weighted_probs if x.shape == target_shape]
        
        probs_sum = np.sum(weighted_probs, axis=0)
        
        log_probs = np.log(probs_sum + 1e-10)
        entropy = -np.sum(probs_sum * log_probs, axis=-1) / LN_2
        varentropy = np.sum(probs_sum * (log_probs / LN_2 + entropy[..., None])**2, axis=-1)
        perplexity = np.exp(np.mean(-log_probs, axis=-1))
        coherence = np.mean(np.max(probs_sum, axis=-1))
        
        vocab_size = probs_sum.shape[-1]
        metrics = {
            'entropy': float(np.mean(entropy)),
            'entropy_max_possible': float(np.log2(vocab_size)),
            'varentropy': float(np.mean(varentropy)),
            'perplexity': float(np.mean(perplexity)),
            'perplexity_max_possible': float(vocab_size),
            'coherence': float(np.mean(coherence)),
            'vocab_size': int(vocab_size),
            'entropy_ratio': np.mean(entropy) / np.log2(vocab_size),
            'perplexity_ratio': np.mean(perplexity) / vocab_size
        }
        return metrics
    
    def _calculate_composite_score(self, agent,metrics: dict) -> float:
        """Calculate a composite score based on entropy, perplexity, and coherence."""
        entropy_max = metrics.get('entropy_max_possible', 10.0)
        perplexity_max = metrics.get('perplexity_max_possible', 1000.0)

        entropy_score = max(0, 1 - (metrics['entropy'] / entropy_max))
        perplexity_score = max(0, 1 - (np.log(metrics['perplexity']) / np.log(perplexity_max)))
        coherence_score = metrics['coherence']
        weighted_score = (
            agent.conciseness_weight * (0.5 * entropy_score + 0.5 * perplexity_score)+
            (1 - agent.conciseness_weight) * coherence_score
        )
        return weighted_score
    
    def invoke(self,agent,query: Union[str, List[Dict[str, str]]]) -> str:
        """Evaluate and refine model responses based on entropy and coherence."""
        best_score, best_response = float('-inf'), None
        plateau_count = 0
        
        for i in tqdm(range(agent.max_iterations), desc="Iterations"):
            
            initial_response = self.generate(agent,agent.generator_llm,query)
            
            critique_comments = self.critique(agent,agent.critique_llm,initial_response, query)
            
            revised_response = self.refine_response(agent,agent.generator_llm,initial_response, critique_comments)
            
            metrics = self.calculate_metrics(revised_response)
            current_score = self._calculate_composite_score(agent,metrics)
            
            logger.info(f"Epoch {i+1} - Metrics: {metrics}")

            if current_score > best_score + agent.entropy_threshold:
                best_score = current_score
                best_response = revised_response
                plateau_count = 0
            else:
                plateau_count += 1

            if plateau_count >= agent.max_plateau_count:
                logger.info("Stopping due to plateau.")
                break
        
        return best_response or revised_response


    def update_chat_history(self,agent,query:Union[str, List[Dict[str, str]]]):
        if isinstance(query, str):
            agent.messages.append(UserMessage(
                content=agent.system_prompt.format(query=query)))
        elif isinstance(query,List):
            if isinstance(query[-1],UserMessage):
                agent.messages.extend(query)
            elif isinstance(query[-1],dict):
                if query[-1]["role"]=="user":
                    user_msg=UserMessage(content=agent.system_prompt.format(query=query[-1]["content"]))
                    query[-1]=user_msg
                agent.messages.extend(query)
        
        
    def generate(self, agent,llm,query: Union[str, List[Dict[str, str]]]) -> str:
        """Generate response for a given query using the provided LLM"""
        
        self.update_chat_history(agent,query)
        messages = [{"role": msg.role, "content": msg.content} for msg in agent.messages]
        res = llm.invoke(messages)
        updates_res=res["choices"][0]["message"]["content"]
        if updates_res:
            agent.messages.append(AIMessage(
                    content=updates_res))
            return updates_res

    def critique(self, agent,llm,response: str, original_query: Union[str, List[Dict[str, str]]]) -> str:
        # mathematical critique and prompt critique are two different
        """Generate critique comments for the response balancing completeness and conciseness."""
        if isinstance(original_query,UserMessage):
            
            original_query=original_query[-1].content
        elif isinstance(original_query, list) and all(isinstance(msg, dict) for msg in original_query):
            original_query=original_query[-1]["content"]
        
        critique_prompt = (
            f"Analyze this response for '{original_query}' and provide specific critique comments.\n\n"
            f"Response to analyze:\n{response}\n\n"
            "First, evaluate quality aspects:\n"
            "1. Accuracy of the information\n"
            "2. Completeness of core concepts\n"
            "3. Clarity and logical flow\n"
            "4. Depth of essential insights\n\n"
            "Then, evaluate conciseness:\n"
            "5. Identify unnecessary information that can be removed\n"
            "6. Suggest simpler ways to express complex ideas\n"
            "7. Mark redundant content for removal\n\n"
            "Focus on maintaining high coherence while reducing length. "
            "Prioritize simple, clear language over complex explanations."
        )
        return self.generate(agent,llm,critique_prompt)
    
    def refine_response(self,agent,llm, initial_response: str, critique_comments: str) -> str:
        refine_prompt=f"""Based on these critique comments:\n{critique_comments}
                Original response:\n{initial_response}
                Generate a refined response focusing on essential information only"""
        return self.generate(agent,llm,query=refine_prompt)