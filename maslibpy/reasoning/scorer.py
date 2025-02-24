from typing import List, Dict, Union
from maslibpy.reasoning.mathematical import Mathematical
from maslibpy.reasoning.prompt_based import PromptBased
class Scorer():
    def mathematical(self,agent,query: Union[str, List[Dict[str, str]]]):
        scorer=Mathematical(agent)
        generated_response=scorer.invoke(agent,query)
        return generated_response
    def prompt_based(self,agent,query:Union[str, List[Dict[str, str]]]):
        prompter=PromptBased()
        generated_response=prompter.invoke(agent,query)
        return generated_response