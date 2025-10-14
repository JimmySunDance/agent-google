from datetime import datetime as dt

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import google_search

AGENT_INSTRUCTION = """
You are a helpful assistant that can use the following tools:
- google_search
"""

### adk requires a return type and doc string for each tool
def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS.
    """
    return {
        "current_time": dt.now().strftime("%Y-%m-%d %H:%M:%S")
    }



root_agent = Agent(
    name="tool_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="An agent that can use tools to answer questions.",
    instruction=AGENT_INSTRUCTION, 
    ### adk cannot take built in and custom tools at the same time
    tools=[get_current_time],
    ### or - requires Google AI 
    # tools=[google_search],
)
