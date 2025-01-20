from maslibpy.messages.base import BaseMessage

class SystemMessage(BaseMessage):
    VALID_ROLES = ["system"]

    def __init__(self, role: str = "system", content: str = ""):
        """
        Initialize a SystemMessage instance.

        Parameters:
        - role (str): The role associated with the message. Default is "system".
        - content (str): The content of the system message. Default is an empty string.

        Raises:
        - ValueError: If the role is not "system".

        Attributes:
        - role (str): Stores the role of the message (restricted to "system").
        - content (str): Stores the content of the system message.
        """
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role. Available roles are {self.VALID_ROLES}.")
        super().__init__(role, content)

    def __repr__(self):
        """
        Return a string representation of the SystemMessage instance.

        Returns:
        - str: A string in the format `SystemMessage(role=<role>, content=<content>)`.
        """
        return f"SystemMessage(role={self.role}, content={self.content})"
