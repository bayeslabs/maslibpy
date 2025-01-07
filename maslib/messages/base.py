from typing import List, Dict

class BaseMessage:
    messages:List[Dict[str, str]]=[]
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        BaseMessage.messages.append({"role": role, "content": content})
