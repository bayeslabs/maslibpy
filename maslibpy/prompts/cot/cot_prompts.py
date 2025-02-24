from pydantic import BaseModel, Field, model_validator
from typing import ClassVar

class CoT(BaseModel):
   
    available_patterns: ClassVar[list] = ['cot', 'one_shot']
    
    cot: bool = Field(default=False, description="Default cot prompt")
    one_shot: bool = Field(default=False, description="Cot prompt with single example")
    
    @model_validator(mode="before")
    @classmethod
    def validate_flags(cls, values: dict):
        """Ensures that only one prompt type is selected."""
        selected_flags = [key for key, value in values.items() if value is True]
        if len(selected_flags) > 1:
            raise ValueError(f"Only one prompt type can be selected at a time. Selected: {selected_flags}")
        
        if values.get('prompt_pattern') and values['prompt_pattern'] not in cls.available_patterns:
            raise ValueError(f"Invalid prompt pattern. Available patterns are: {cls.available_patterns}")
        
        return values
    def get_cot_prompt(self):
        """Default COT prompt."""
        return """Answer the following questions as best you can. 
        You must think step by step to answer the question.
        Final Answer: Return the final answer to the original input question
        Begin!
        Question: {query}
        """
    
    # def get_cot_prompt(self):
    #     """Default COT prompt."""
    #     return """Answer the following questions as best you can. 
    #     You must think step by step to answer the question.
    #     Final Answer: Return the final answer to the original input question
    #     Begin!
    #     Question: {query}
    #     """

    def get_reflection_prompt(self):
        """Prompt for reflection mode."""
        return """You are now using the Reflection strategy to solve the problem.
        Use the following format:
        Reflection Thought: Think deeply about past experiences
        Reflection Action: Take an action based on reflection
        Reflection Observation: Learn from the action
        Final Thought: I have refined my answer
        Final Answer: {query}"""


    # def get_cot_oneshot_prompt(self):
    #     """Prompt for reflection mode."""
    #     return """You must think step by step to answer the question.

    #     For example:
    #     Question- Roger has 5 tennis balls. He buys 2 more cans of tennis balls. 
    #               Each can has 3 balls. How many balls in total he has now?
    #     Solution-       
    #     To find the total number of tennis balls Roger has now, we need to follow these steps:

    #     1. First, we note that Roger initially has 5 tennis balls.
    #     2. Then, he buys 2 more cans of tennis balls, with each can containing 3 balls.
    #     3. To find out how many balls are in the 2 cans, we multiply the number of cans by the number of balls per can: 2 cans * 3 balls/can = 6 balls.
    #     4. Finally, we add the initial number of balls Roger had to the number of balls in the 2 cans he bought: 5 (initial balls) + 6 (balls from the cans) = 11 balls.

    #     Therefore, Roger now has a total of 11 tennis balls.

    #     Final Answer: The final answer is 11. 
    #     Always think step by step to answer the user's question.
    #     Final Answer: {query}"""

    def fetch_prompt(self):
        """Returns the correct prompt based on the selected flag."""
        if self.one_shot:
            return self.get_cot_oneshot_prompt()
        self.cot=True
        return self.get_cot_prompt()