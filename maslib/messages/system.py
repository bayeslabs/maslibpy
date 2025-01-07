from maslib.messages.base import BaseMessage

class SystemMessage(BaseMessage):
    VALID_ROLES = ["system"]

    def __init__(self, role: str = "system", content: str = ""):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role. Available roles are {self.VALID_ROLES}.")
        super().__init__(role, content)

    def __repr__(self):
        return f"SystemMessage(role={self.role}, content={self.content})"
