from maslib.agent.agent import Agent
from maslib.crew.crew import Crew
from maslib.llm.llm import LLM

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

###MAIN###

crew=Crew([symptom_collector_agent,diagnosis_agent,treatment_recommender_agent],
          system_prompt=sys_prompt)

re=crew.invoke("I have been experiencing headaches, nausea, and sensitivity to light.")

print(re)