from maslibpy.messages.base import BaseMessage

class UserMessage(BaseMessage):
    VALID_ROLES = ["user"]

    def __init__(self, role: str = "user", content: str = ""):
        """
        Initialize a UserMessage instance.

        Parameters:
        - role (str): The role associated with the message. Default is "user".
        - content (str): The content of the user message. Default is an empty string.

        Raises:
        - ValueError: If the role is not "user".

        Attributes:
        - role (str): Stores the role of the message (restricted to "user").
        - content (str): Stores the content of the user message.
        """
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role. Available roles are {self.VALID_ROLES}.")
        super().__init__(role, content)
        
    def __repr__(self):
        """
        Return a string representation of the UserMessage instance.

        Returns:
        - str: A string in the format `UserMessage(role=<role>, content=<content>)`.
        """
        return f"UserMessage(role={self.role}, content={self.content})"
