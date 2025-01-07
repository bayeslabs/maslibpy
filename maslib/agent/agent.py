from maslib.agent.baseagent import BaseAgent
from maslib.messages.user import UserMessage
from maslib.messages.system import SystemMessage
from maslib.messages.base import BaseMessage
class Agent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SystemMessage(content=f"""You are a {self.name} agent with your task as {self.role} with a goal of:{self.goal} and with a backstory of {self.backstory}""")

    def invoke(self, query: str) -> str:
        UserMessage(content=query)
        
        response = self.llm.invoke(BaseMessage.messages)
        return response
