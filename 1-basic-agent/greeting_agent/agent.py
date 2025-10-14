from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

INSTRUCTIONS="""
Youa are a helpful assistant whose only job is to greet the user.
Ask for the user's name and greet them warmly.
"""

root_agent = Agent(
    name="greeting_agent",
    model=LiteLlm(model="ollama_chat/llama3.2:latest"),
    description="An agent that greets the user.",
    instruction=INSTRUCTIONS,
)