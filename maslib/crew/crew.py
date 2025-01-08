from maslib.messages.system import SystemMessage
from maslib.messages.base import BaseMessage
from maslib.messages.user import UserMessage
from maslib.messages.assistant import AIMessage
from maslib.agent.agent_prompt import prompt_template
from litellm import completion
from maslib.agent.agent import Agent
import random
class Crew:
    def __init__(self,agents:list[Agent],llm=None,max_iterations=3,system_prompt=None):
        self.crew=agents
        self.llm =llm
        if system_prompt is None:
            # using default prompt
            system_prompt=prompt_template.format(
            agents=agents,agent_names=[agent.name for agent in agents],
            max_iterations=max_iterations,
            input="",
            agent_scratchpad="")    
        SystemMessage(content=system_prompt)
        if self.llm is None:
            available_llms=[agent.llm for agent in agents]
            self.llm=random.choice(available_llms)
    def invoke(self,query):
        
        UserMessage(content=query)
        res=completion(model=self.llm.model_name,messages=BaseMessage.messages,stream=False)
        return res.content.choices[0]["message"]["content"]
    def __repr__(self):

        return f"Crew(agents:{self.crew})"
