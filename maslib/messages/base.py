from typing import List, Dict

class BaseMessage:
    messages:List[Dict[str, str]]=[]
    def __init__(self, role: str, content: str):
        """
        Initialize a BaseMessage instance and add it to the global message list.

        Parameters:
        - role (str): The role associated with the message (e.g., "user", "assistant").
        - content (str): The content of the message.

        Attributes:
        - role (str): Stores the role of the message.
        - content (str): Stores the content of the message.

        The message is appended to the shared `messages` list as a dictionary with keys `role` and `content`.
        """
        self.role = role
        self.content = content
        BaseMessage.messages.append({"role": role, "content": content})
