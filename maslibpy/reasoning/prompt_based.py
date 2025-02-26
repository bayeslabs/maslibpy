from typing import Union,Dict,List
from tqdm import tqdm
from maslibpy.messages.user import UserMessage
from maslibpy.messages.assistant import AIMessage
import time
import os
from pydantic import BaseModel
class GradeNode(BaseModel):
    status:bool
class PromptBased():
    
    def invoke(self,agent,query: Union[str, List[Dict[str, str]]]) -> str:
        actual_query = query
        
        for i in tqdm(range(agent.max_iterations),desc="Iterations"):
            try:
                generated_response = self.generate(agent,agent.generator_llm,actual_query)
                
                if generated_response is not None:
                    ind=generated_response.rfind("Final Answer")
                    if ind>=0:
                        generated_response=generated_response[ind+len("Final Answer:"):]
                else:
                    generated_response=""
                    raise Exception 
                
                critiqued_response = self.critique(agent,agent.critique_llm,generated_response,original_query=query)
                
                
                grade_output=self.grade(agent,agent.critique_llm,query,generated_response,critiqued_response)
                
                if grade_output:
                    print("breaking the loop")
                    break
                
            except Exception as e:
                raise e
                
        
        return generated_response
        
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
        # return agent.messages

    def generate(self, agent,llm,query: Union[str, List[Dict[str, str]]],response_format="",tools=[]) -> str:
        """Generate response for a given query using the provided LLM"""
        # agent.messages=self.update_chat_history(agent,query)
        self.update_chat_history(agent,query)

        messages = [{"role": msg.role, "content": msg.content} for msg in agent.messages]
        res = llm.invoke(messages,response_format,tools)
        updates_res=res["choices"][0]["message"]["content"]
        if updates_res:
            agent.messages.append(AIMessage(
                    content=updates_res))
            return updates_res
        
    def grade(self, agent,llm, query: str, generated_response: str, critiqued_response: str) -> bool:
        """Returns true if the response meets the criteria, otherwise False."""
        
        grade_prompt = f"""
            You are a boolean evaluator that must only return True or False without any additional text or explanation.
            Evaluate the response based on these criteria:
            1. Accuracy: Is the response factually correct?
            2. Completeness: Does it fully address all aspects of the query?
            3. Clarity: Is it well-structured and easy to understand?
            4. Relevance: Does it directly address the topic asked?

            Evaluate:
            - **User Query**: {query}
            - **Generated Response**: {generated_response}
            - **Critiqued Response**: {critiqued_response}

            Return exactly 'True' if all criteria are met, or exactly 'False' if any criterion fails.
            Do not include any reasoning, explanations, or additional characters - your entire output must be either the word 'True' or the word 'False'.
            """
        tools = [{
            "type": "function",
            "function": {
                "name": "evaluate_grade",
                "description": "Returns a boolean indicating if the response meets all criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "boolean",
                            "description": "True if response meets all criteria, False otherwise"
                        }
                    },
                    "required": ["status"]
                }
            }
        }]
        
        # Try response schema with function calling first
        if hasattr(llm, 'supports_response_schema') and llm.supports_response_schema and hasattr(agent.critique_llm, 'supports_parallel_function_calling') and agent.critique_llm.supports_parallel_function_calling:
            grade_result = self.generate(agent,llm,query= grade_prompt, response_format=GradeNode, tools=tools)
            if isinstance(grade_result, GradeNode):
                return grade_result.status
        
        if hasattr(llm, 'supports_parallel_function_calling') and llm.supports_parallel_function_calling:
            print("Using function calling for grading.")
            grade_result = self.generate(agent, llm,grade_prompt, tools=tools)
            if isinstance(grade_result, dict) and "status" in grade_result:
                return grade_result["status"]
            elif isinstance(grade_result, str) and "true" in grade_result.lower():
                
                return True
            return False
        
        grade_result = self.generate(agent,llm,grade_prompt)
        
        result_text = grade_result.strip().lower()
        if result_text == 'true':
            return True
        elif 'true' in result_text and 'false' not in result_text:
            return True
        return False

    def critique(self, agent,llm,response: Union[str, List[Dict[str, str]]],original_query: str = ""):
        """Generates a critique of the initial response."""
        critique_prompt = f"""Evaluate this response for "{original_query}":

        {response}

        Check:
        1. Accuracy: Any errors?
        2. Completeness: Missing key info?
        3. Clarity: Clear and logical?

        If accurate and complete, return exactly: {response}
        Otherwise, provide corrected version."""
        
        return self.generate(agent,llm,critique_prompt)