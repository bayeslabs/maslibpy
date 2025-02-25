from typing import Literal, Optional, List
from uuid import uuid4
from maslibpy.llm.llm import LLM
from pydantic import BaseModel, Field

class BaseAgent(BaseModel):
    agent_id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = ""
    role: str = ""
    goal: str = ""
    backstory: str = ""
    generator_llm:Optional[LLM]=None
    critique_llm:Optional[LLM]=None
    system_prompt: Optional[str] = None
    prompt_type: Literal["cot", "react"] = Field(default="react")
    prompt_pattern: Optional[str] = None
    messages:List=Field(default_factory=list)
    max_iterations: int = 3
    score_type:Literal["mathematical","prompt_based"]=Field(default="prompt_based")
    entropy_threshold:float =Field(default=0.13)
    conciseness_weight:float=Field(default=0.4)
    max_plateau_count:int=Field(default=3)
    class Config:
        arbitrary_types_allowed = True
