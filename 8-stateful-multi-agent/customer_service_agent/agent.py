from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .sub_agents.course_support_agent.agent import course_support_agent
from .sub_agents.order_agent.agent import order_agent
from .sub_agents.policy_agent.agent import policy_agent
from .sub_agents.sales_agent.agent import sales_agent

prompt_path = "./customer_service_agent/agent_prompt.txt"
PROMPT = open(prompt_path).read()

# Create the root customer service agent
customer_service_agent = Agent(
    name="customer_service_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="Customer service agent for AI Developer Accelerator community",
    instruction=PROMPT,
    sub_agents=[policy_agent, sales_agent, course_support_agent, order_agent],
    tools=[],
)