from pydantic import BaseModel, Field, model_validator
from typing import ClassVar

class ReAct(BaseModel):
    available_patterns: ClassVar[list] = ['react', 'reflection', 'reflexion', 'rewoo']
    
    react: bool = Field(default=False, description="Default react prompt")
    reflection: bool = Field(default=False, description="Flag to use reflection")
    reflexion: bool = Field(default=False, description="Flag to use reflexion")
    rewoo: bool = Field(default=False, description="Flag to exclude observations")
    
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

    def get_react_prompt(self):
        """Default ReAct prompt."""
        return """Answer the following questions as best you can. 
        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat 2 times)
        Thought: I now know the final answer
        Final Answer: Return the final answer to the original input question
        Begin!
        Question: {query}
        Thought: """
        
        # """Default ReAct prompt."""
        # return """Answer the following questions as best you can. 
        # You must plan forward to proceed in a series of steps, in a cycle of 'Thought:', 
        # 'Action:', and 'Observation:' sequences.
        # At each step, in the 'Thought:' sequence, you should first explain your reasoning 
        # towards answering the question.
        # Then in the 'Action' sequence you should take the action.
        # In the 'Observation' sequence you should observe your answer or monitor the result 
        # of your action.
        
        # Use the following format:
        # Question: the input question you must answer
        # Thought: you should always think about what to do
        # Action: the action to take
        # Observation: the result of the action
        # Thought: I now know the final answer
        # Final Answer: Return the final answer to the original input question
        # Begin!
        # Question: {query}
        # Thought: """
    

    def get_reflection_prompt(self):
        """Prompt for reflection mode."""
        return """You are now using the Reflection strategy to solve the problem.
        Use the following format:
        Reflection Thought: Think deeply about past experiences
        Reflection Action: Take an action based on reflection
        Reflection Observation: Learn from the action
        Final Thought: I have refined my answer
        Final Answer: {query}"""
    
        # """Prompt for reflection mode."""
        # return """You are now using the Reflection strategy to answer user's query.
        # Use the following format:
        # Thought: Answer the user query from your knowledge
        # Action: Take an action based on your thought
        # Reflection: Review your previous response and identify any missing points or 
        # areas that could be improved
        # Final Thought: I have refined my answer
        # Final Answer: {query}"""

    def get_reflexion_prompt(self):
        """Prompt for reflexion mode."""
        return """This is the Reflexion strategy. Focus on self-correction.
        Thought: What mistakes might I have made?
        Action: Adjust based on new insights
        Observation: Evaluate correctness
        Final Thought: I have corrected myself
        Final Answer: 
        {query}"""

        # """Prompt for reflexion mode."""
        # return """This is the Reflexion strategy. Focus on self-correction.
        # Thought: Answer the user query from your knowledge
        # Action: Take an action based on your thought
        # Observation: observe the result of the action
        # Evaluate: Evaluate the accuracy of your previous response. Suggest improvements if necessary.
        # Reflection: Consider your thought, action, observation and evaluation.
        # Action: Take an action based on your reflection
        # Final Thought: I have the correct answer 
        # Final Answer: {query}"""

    def get_rewoo_prompt(self):
        """Prompt for rewoo mode (excluding observations)."""
        return """Answer the following questions as best you can.
        Observations will be excluded.
        Thought: Think carefully before taking action
        Action: Take the best action
        Thought: Without observations, I will rely on reasoning
        User Query: {query}"""
    
        # """Prompt for rewoo mode (excluding observations). Planner- Worker- Solver"""
        # return """For the following task, make plans that can solve the problem step by step.
        # Planner: Create a step by step plan to answer the user's query. Each plan can be named P1, P2, ... 
        # Worker: Work on your plans and collect evidence for each plan. Evidence for each corresponding 
        # plan can be named as E1, E2,..
        # Solver: Process all plans and evidence to formulate a solution to the original task or problem.
        # Final Answer: {query}"""

    def fetch_prompt(self):
        """Returns the correct prompt based on the selected flag."""
        if self.reflection:
            return self.get_reflection_prompt()
        elif self.reflexion:
            return self.get_reflexion_prompt()
        elif self.rewoo:
            return self.get_rewoo_prompt()
        self.react=True
        return self.get_react_prompt()
