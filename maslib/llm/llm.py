import os
import logging
import litellm
from typing import  List, Dict, Union
from litellm import completion
from maslib.messages.user import UserMessage
from maslib.messages.assistant import AIMessage
from maslib.llm.constants import MODELS,PROVIDERS,ENV_VARS
logging.basicConfig(level=logging.INFO)
litellm.set_verbose=True

class LLM():
    def __init__(
            self, 
            provider: str = "together",
            model_name: str = "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1"):
        """
        Initialize the LLM instance with the specified provider and model.
        Default values are provided for quick setup.
        """
        self.provider = provider
        self.model_name = model_name
        self.api_key = None
        self.validate_provider()

    def validate_provider(self):
        """
        Validate the provider and model, and check for the required API key in environment variables.
        """
        if self.provider not in PROVIDERS:
            logging.error(f"Unsupported provider: {self.provider}. Supported providers are: {PROVIDERS}")
            raise ValueError(f"Unsupported provider. Supported providers: {PROVIDERS}")
        
        if self.model_name not in MODELS[self.provider]:
            logging.error(f"Unsupported model: {self.model_name}. Supported models for {self.provider}: {MODELS[self.provider]}")
            raise ValueError(
                f"Unsupported model: {self.model_name} for provider: {self.provider}. "
                f"Available models for {self.provider}: {MODELS[self.provider]}"
            )
        
        env_key = ENV_VARS[self.provider]["key_name"]
        if not os.environ.get(env_key):
            logging.error(f"Missing environment variable: {env_key}")

            raise EnvironmentError(ENV_VARS[self.provider]["prompt"])
        
        self.api_key = os.environ.get(env_key)
        logging.info(f"API key validated for provider {self.provider}")

    def invoke(self, messages: Union[str, List[Dict[str, str]]]) -> str:
        """
        Invoke the LLM with the given messages.

        :param messages: A string or a list of dictionaries representing the messages.
        :return: The content of the response from the LLM.
        """
        if isinstance(messages, str):
            human_msg=UserMessage(role="user",content=messages)
            formatted_messages=human_msg.messages
        elif isinstance(messages, list) and all(isinstance(msg, dict) for msg in messages):
            formatted_messages = messages
        else:
            logging.error("Input must be a string or a list of dictionaries for messages.")
            raise ValueError("Input must be a string or a list of dictionaries for messages.")
        try:
            print("current model  supports function calling:",litellm.supports_function_calling(model=self.model_name))
            response = completion(model=self.model_name, messages=formatted_messages,stream=False)
            res= response["choices"][0]["message"]["content"]
            ai_msg=AIMessage(content=res)
            return ai_msg
        except Exception as e:
            logging.error(f"Error invoking the model: {e}")
            raise
