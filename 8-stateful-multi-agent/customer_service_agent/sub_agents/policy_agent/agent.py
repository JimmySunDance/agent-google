from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


prompt_path = "./customer_service_agent/sub_agents/policy_agent/agent_prompt.txt"
PROMPT = open(prompt_path).read()


# Create the policy agent
policy_agent = Agent(
    name="policy_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="Policy agent for the AI Developer Accelerator community",
    instruction=PROMPT,
    tools=[],
)