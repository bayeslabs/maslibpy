from maslibpy.messages.system import SystemMessage
from maslibpy.llm.llm import LLM
from maslibpy.reasoning.scorer import Scorer
from typing import List, Dict, Union
from maslibpy.prompts.react.react_prompts import ReAct
from maslibpy.prompts.cot.cot_prompts import CoT
from maslibpy.agent.baseagent import BaseAgent


class Agent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages.append(
            SystemMessage(
                content=f"You are a {self.name} agent with your task as {self.role}. "
                        f"Your goal is: {self.goal}. Backstory: {self.backstory}"))
        self.select_prompt(kwargs)

    def select_prompt(self,kwargs):
        """Default React will be set"""
        if self.prompt_type=="cot":
            self.prompt_pattern=kwargs.get("prompt_pattern","cot")
            cot_instance=CoT(**{self.prompt_pattern: True})
            self.system_prompt = cot_instance.fetch_prompt()
            print("cot instane",cot_instance)   
        else:
            self.prompt_pattern=kwargs.get("prompt_pattern","react")
            react_instance = ReAct(**{self.prompt_pattern: True})
            self.system_prompt = react_instance.fetch_prompt()
            print("react instane",react_instance)
    
    def invoke(self, query: Union[str, List[Dict[str, str]]]):
        """Default Scoring function is prompt based"""
        
        if self.score_type=="mathematical":
            generated_response=Scorer().mathematical(agent=self,query=query)
        else:
            generated_response=Scorer().prompt_based(agent=self,query=query)
        return generated_response

agent = Agent(
    name="TestAgent",
    role="AI Assistant",
    goal="Assist users effectively",
    backstory="An advanced AI designed to provide helpful insights.",
    prompt_type="react",
    prompt_pattern="react"
    max_iterations=3,
    critique_llm=LLM(provider="together", model_name="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"),
    generator_llm=LLM(provider="together", model_name="together_ai/mistralai/Mistral-7B-Instruct-v0.1"),
    score_type="prompt_based"
) 

agent.invoke([{"role":"user","content":"what are AI Agents"}])
