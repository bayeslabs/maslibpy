from pydantic import BaseModel
from uuid import uuid4
from maslib.llm.llm import LLM

class BaseAgent(BaseModel):
    id:str=str(uuid4())
    name:str=""
    role:str=""
    goal:str=""
    backstory:str=""
    llm: LLM = None
    class Config:
        arbitrary_types_allowed = True