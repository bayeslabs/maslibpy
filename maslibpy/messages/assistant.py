from maslibpy.messages.base import BaseMessage

class AIMessage(BaseMessage):
    VALID_ROLES = ["assistant"]

    def __init__(self, role: str = "assistant", content: str = ""):
        """
        Initialize an AIMessage instance.

        Parameters:
        - role (str): The role associated with the message. Default is "assistant".
        - content (str): The content of the message. Default is an empty string.

        Raises:
        - ValueError: If the role is not one of the `VALID_ROLES`.

        This method ensures that the role of the message is restricted to "assistant".
        """
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role. Available roles are {self.VALID_ROLES}.")
        super().__init__(role, content)

    def __repr__(self):
        """
        Return a string representation of the AIMessage instance.

        Returns:
        - str: A string in the format `AIMessage(role=<role>, content=<content>)`.
        """
        return f"AIMessage(role={self.role}, content={self.content})"
