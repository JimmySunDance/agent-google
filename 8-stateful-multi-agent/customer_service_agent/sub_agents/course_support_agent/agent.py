from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


prompt_path = "./customer_service_agent/sub_agents/course_support_agent/agent_prompt.txt"
PROMPT = open(prompt_path).read()

# Create the course support agent
course_support_agent = Agent(
    name="course_support",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="Course support agent for the AI Marketing Platform course",
    instruction=PROMPT,
    tools=[],
)