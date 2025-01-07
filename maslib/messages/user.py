from maslib.messages.base import BaseMessage

class UserMessage(BaseMessage):
    VALID_ROLES = ["user"]

    def __init__(self, role: str = "user", content: str = ""):
        
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role. Available roles are {self.VALID_ROLES}.")
        super().__init__(role, content)
        
    def __repr__(self):
        return f"UserMessage(role={self.role}, content={self.content})"
