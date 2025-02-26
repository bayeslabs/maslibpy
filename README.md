# MASLibPy: Multi-Agent System Python Library

**maslibpy** is a lightweight, modular Python library designed to facilitate the creation and management of multi-agent systems with enhanced reasoning capabilities. It offers a structured framework for building agents, managing message flows, integrating with various LLM providers, and leveraging advanced reasoning modules.

---

## Features
- **Modular Agent Design:** Create and manage agents with customizable roles, goals, and LLM integrations.
- **Message Flow Management:** Built-in support for system, user, and assistant communications.
- **Advanced Reasoning:** Utilizes Prompt-based and Mathematical-based reaoning with various prompt templates like chain-of-thought (CoT), REACT, ReWOO, Reflection and Reflexion prompt for improved decision-making.
- **LLM Integration:** Seamless connectivity with multiple providers (e.g., OpenAI, Together, Groq, Replicate).
- **Dynamic Collaboration:** Orchestrate multi-agent interactions with integrated reasoning and scoring modules.

---

## Installation

Clone the repository and install the dependencies using Poetry:

```bash
git clone https://github.com/bayeslabs/maslibpy.git
cd maslibpy
```
```bash
pip install poetry
poetry install
```
---

## Directory Structure
``` bash
maslibpy/
├── assets/
│   ├── reasoning_workflow.png
│   └── MathematicalReasoning_Experimentations.pdf
├── prompts/
│   ├── cot/
│   │   └── cot_prompts.py
│   └── react/
│       └── react_prompts.py
├── reasoning/
│   ├── scorer.py
│   ├── prompt_based.py
│   └── mathematical.py
├── agent/
│   ├── baseagent.py
│   └── agent.py
├── messages/
│   ├── base.py
│   ├── system.py
│   ├── user.py
│   └── assistant.py
├── patttern/
│   └── sequential.py
├── llm/
│   ├── llm.py
│   └── constants.py
├── pyproject.toml
└── README.md

```

---

## File Descriptions

### Prompts
- **prompts/cot/cot_prompts.py**: Contains chain-of-thought (CoT) prompt templates that guide agents through step-by-step reasoning.
- **prompts/react/react_prompts.py**: Provides REACT prompt templates (REACT, Reflection, Reflexion, ReWoo) to help agents integrate reasoning and decision-making within their interactions.

### Reasoning
- **reasoning/scorer.py**: Implements functionality to evaluate and score the reasoning outputs of agents.
- **reasoning/prompt_based.py**: Offers prompt-based reasoning modules to assist in structured problem solving.
- **reasoning/mathematical.py**: Contains utilities for mathematical reasoning and computations during agent interactions.

### Agent
- **agent/baseagent.py**: Defines the base agent class with core attributes (e.g., id, name, role, goal) and LLM integration.
- **agent/agent.py**: Extends the base agent class with additional behaviors and advanced interaction capabilities.

### Messages
- **messages/base.py**: Establishes the foundational `BaseMessage` class for managing message flows.
- **messages/system.py**: Implements the `SystemMessage` class for system-level communications.
- **messages/user.py**: Implements the `UserMessage` class for user-initiated communications.
- **messages/assistant.py**: Implements the `Assistant` (AI) message class for agent responses.

### Pattern
- **pattern/sequential.py**: Provides a sequential coordination mechanism for orchestrating multi-agent collaborations.  

### LLM
- **llm/llm.py**: Manages integration with LLM providers, handling model invocations and API key validations.
- **llm/constants.py**: Defines environment variables, supported LLM providers, and available model configurations.

---

## Example Usage

To see how `maslibpy` works, instantiate an `Agent` and invoke a query. Below is a simple example of creating an agent and asking it about AI Agents.

```python
from maslibpy.agent.agent import Agent
from maslibpy.llm.llm import LLM

# Initialize an agent with specific attributes
agent = Agent(
    name="TestAgent",
    role="AI Assistant",
    goal="Assist users effectively",
    backstory="An advanced AI designed to provide helpful insights.",
    prompt_type="cot",
    max_iterations=2,
    critique_llm=LLM(provider="together", model_name="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"),
    generator_llm=LLM(provider="together", model_name="together_ai/mistralai/Mistral-7B-Instruct-v0.1"),
    score_type="mathematical"
)

# Invoke the agent with a user query
response = agent.invoke([{"role": "user", "content": "What are AI Agents?"}])

# Print the response
print(response)
```

### Customization & Flexibility

The `Agent` class extends `BaseAgent`, which comes with several configurable attributes. The example above demonstrates a basic use case, but you can modify additional parameters to fine-tune the agent’s behavior.

#### **Available Attributes**
The following attributes can be customized:

| Attribute           | Description |
|---------------------|-------------|
| `name`             | Name of the agent. |
| `role`             | The agent’s assigned role. |
| `goal`             | The main objective of the agent. |
| `backstory`        | Background information about the agent. |
| `generator_llm`    | LLM used for generating responses. |
| `critique_llm`     | LLM used for critique (if applicable). |
| `prompt_type`      | Type of prompting strategy (`cot` or `react`). |
| `prompt_pattern`   | Specific prompt pattern for reasoning. |
| `max_iterations`   | Number of reasoning iterations before stopping. |
| `score_type`       | Scoring mechanism (`mathematical` or `prompt_based`). |
| `entropy_threshold` | Threshold for entropy-based scoring. |
| `conciseness_weight` | Weight factor for response conciseness. |
| `max_plateau_count` | Limit for consecutive non-improving iterations. |

#### **How to Modify Attributes**
If you need to adjust any of these attributes, simply pass them as keyword arguments when instantiating the agent.

##### **Example: Modifying Additional Parameters**
```python
agent = Agent(
    name="CustomAgent",
    role="Scientific Researcher",
    goal="Analyze complex datasets and generate insights.",
    backstory="An AI model specialized in data science and reasoning.",
    prompt_type="react",  
    max_iterations=5,  # Increased iterations for deeper reasoning
    entropy_threshold=0.2,  # Adjusted entropy for stricter evaluation
    conciseness_weight=0.5  # Prioritizing concise responses
)
```

---

## Configuration

Environment Variables

Ensure the appropriate API keys are set in your environment variables:
- TOGETHER_API_KEY
- GROQ_API_KEY
- REPLICATE_API_KEY

Supported LLM Providers and Models:
- Refer to maslibpy/llm/constants.py for the list of supported providers and models.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description.

---

## Contact 

- For questions or support, please reach out to the repository maintainers: contact@bayeslabs.co

---
