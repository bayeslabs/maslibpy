# MASLibPy: Multi-Agent System Library

**maslibpy** is a lightweight, modular Python library designed to facilitate the creation and management of multi-agent systems. It provides a structured framework for building agents, defining their communication protocols, and integrating them with various Large Language Models (LLMs).

## Features
- Modular design for agent creation and management.
- Built-in support for system, user, and assistant message flows.
- Seamless integration with multiple LLM providers (e.g., OpenAI, Together, Groq, Replicate).
- Easy-to-use APIs for invoking and orchestrating agent interactions.
- Dynamic crew management for multi-agent collaborations.

---

## Installation 
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
├── agent/
│   ├── baseagent.py
│   ├── agent.py
│   └── agent_prompt.py
├── messages/
│   ├── base.py
│   ├── system.py
│   ├── user.py
│   └── assistant.py
├── pattern/
│   └── sequential.py
├── llm/
│   ├── llm.py
│   └── constants.py
```

---

## File Descriptions

### Agent: 
- baseagent.py: Contains the base agent class BaseAgent with core properties like id, name, role, and goal. Also includes integration with LLMs.
- agent.py: Implements the Agent class, extending BaseAgent. It defines the agent's behavior, including how queries are handled and responses are generated.
- agent_prompt.py: Provides the template prompt used by agents for structured reasoning and interaction.

### Message:
- base.py: Defines the foundational BaseMessage class for managing the message flow within the system.
- system.py: Implements the SystemMessage class for system-level communication.
- user.py: Implements the UserMessage class for user-initiated communication.
- assistant.py: Implements the AIMessage class for assistant responses.

### Pattern: 
- sequential.py: Implements the Crew class, which manages a group of agents and orchestrates their collaborative tasks using an LLM backend in a sequantial manner.

### LLM:
- llm.py: Manages LLM integration, including provider validation, model invocation, and environment variable checks for API keys.
- constants.py: Defines environment variables, supported LLM providers, and available model configurations.

---

## Example Usage 

Note: pattern/sequential.py was previsously crew/crew.py

```bash
from maslibpy.agent.agent import Agent
from maslibpy.crew.crew import Crew
from maslibpy.llm.llm import LLM

symptom_collector_agent=Agent(
    name="Symptom Collector Agent",
    role="Gather user-provided symptoms and health details.",
    goal="Ensure accurate and complete collection of symptoms to aid in diagnosis",
    backstory=" A meticulous assistant trained in identifying and documenting symptoms for medical evaluations.",
    llm=LLM(provider="groq",model_name="groq/llama-3.1-8b-instant")
)

diagnosis_agent=Agent(
    name="Diagnosis Agent",
    role="Analyze symptoms to hypothesize potential diagnoses.",
    goal=" Provide an accurate and reasoned diagnosis based on the input symptoms",
    backstory="A seasoned diagnostician trained on vast medical data to recognize patterns in health issues.",
    llm=LLM(provider="groq",model_name="groq/llama-3.1-8b-instant")
)

treatment_recommender_agent=Agent(
    name="Treatment Recommender Agent",
    role="Suggest treatments or next steps based on diagnosis.",
    goal=" Recommend the most effective and feasible treatment options.",
    backstory="A caring guide with expertise in medical treatments, always prioritizing patient well-being.",
    llm=LLM(provider="groq",model_name="groq/llama-3.1-8b-instant")
)

sys_prompt="""
You are an assistant helping in healthcare diagnosis.  
- Step 1: Symptom Collector: Collect and summarize symptoms and relevant information from the user.  
- Step 2: Diagnosis Agent: Based on the collected symptoms, suggest a potential diagnosis with reasoning.  
- Step 3: Treatment Recommender: Provide treatment options or next steps.  
Always think step-by-step and clearly explain your reasoning at each stage.
"""

# Main #

crew=Crew([symptom_collector_agent,diagnosis_agent,treatment_recommender_agent],
          system_prompt=sys_prompt)
          
response = crew.invoke("I have been experiencing headaches, nausea, and sensitivity to light.")
print(response)
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
