from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
# from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time


prompt_path = "./manager/prompt.txt"
INSTRUCTIONS = open(prompt_path).read()

root_agent = Agent(
    name="manager",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="Manager agent to delegate tasks to sub-agents",
    instruction=INSTRUCTIONS,
    sub_agents=[
        funny_nerd, 
        stock_analyst
    ],
    tools=[
        # AgentTool(news_analyst), # how to wrap agents to make them tools.
        get_current_time,
    ],
)