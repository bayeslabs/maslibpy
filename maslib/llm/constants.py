ENV_VARS = {
    "together": 
        {
            "prompt": "Provide you TOGETHER_API_KEY in the environment varibales",
            "key_name": "TOGETHER_API_KEY",
        },
        "groq": 
        {
            "prompt": "Enter your GROQ_API_KEY in the environment variables",
            "key_name": "GROQ_API_KEY",
        },
        "replicate":
        {
            "prompt": "Enter your REPLICATE_API_KEY in the environment variables",
            "key_name": "REPLICATE_API_KEY",
        }
    
}

PROVIDERS = ["openai", "groq", "together","replicate"]

MODELS = {
    "together": [
        # https://docs.together.ai/docs/function-calling
        "together_ai/meta-llama/meta-llama/Llama-3.3-70B-Instruct-Turbo",

        "together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1",
        "together_ai/mistralai/Mistral-7B-Instruct-v0.1"
        
    ],
    "groq": [
        "groq/llama-3.1-8b-instant",
        "groq/llama-3.1-70b-versatile",
        "groq/llama-3.1-405b-reasoning",
        "groq/gemma2-9b-it",
        "groq/gemma-7b-it",
    ],
    "replicate":[
        "replicate/meta/meta-llama-3-8b-instruct",
        "replicate/meta/meta-llama-3-70b-instruct",
    ]
}
