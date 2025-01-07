from maslib.messages.base import BaseMessage

class AIMessage(BaseMessage):
    VALID_ROLES = ["assistant"]

    def __init__(self, role: str = "assistant", content: str = ""):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role. Available roles are {self.VALID_ROLES}.")
        super().__init__(role, content)

    def __repr__(self):
        return f"AIMessage(role={self.role}, content={self.content})"
