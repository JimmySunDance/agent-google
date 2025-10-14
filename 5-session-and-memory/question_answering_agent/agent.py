from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


INSTRUCTION = """
You are a helpful assistant that can answer questions about a user based on their preferences.

Here is some information about the user:
Name: {user_name}

Preferences: 
{user_preferences}
"""

question_answering_agent = Agent(
    name="question_answering_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="An agent that can answer questions about a user based on their preferences and history.",
    instruction=INSTRUCTION
)