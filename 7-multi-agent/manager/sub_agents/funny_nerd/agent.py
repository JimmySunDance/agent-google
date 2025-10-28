from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

def get_nerd_joke(topic:str, tool_context:ToolContext) -> dict:
    """Get a nerdy joke about a specific topic"""
    print(f"--- Tool: get_nerd_joke, Topic: {topic} ---")

    jokes = {
        "python": "Why don't Python programmers like to use inheritance? Because they don't like to inherit anything!",
        "javascript": "Why did the JavaScript developer go broke? Because he used up all his cache!",
        "java": "Why do Java developers wear glasses? Because they can't C#!",
        "programming": "Why do programmers prefer dark mode? Because light attracts bugs!",
        "math": "Why was the equal sign so humble? Because he knew he wasn't less than or greater than anyone else!",
        "physics": "Why did the photon check a hotel? Because it was traveling light!",
        "chemistry": "Why did the acid go to the gym? To become a buffer solution!",
        "biology": "Why did the cell go to therapy? Because it had too many issues!",
        "default": "Why did the computer go to the doctor? Because it had a virus!",
    }

    joke = jokes.get(topic.lower(), jokes["default"])
    tool_context.state["last_joke_topic"] = topic

    return {
        "status": "success",
        "joke": joke,
        "topic": topic,
    }


SYSTEM_PROMPT = """
You are a funny nerd agent that tells nerdy jokes about various topics.

When asked to tell as joke:
1. Use the get_nerd_joke tool to get a joke about the specified topic.
If no specific topic is mentioned, ask the user for a topic.
3. Format the response to include both the joke and an explanation. 

Available topics are:
- Python
- JavaScript
- Java
- Programming
- Math
- Physics
- Chemistry
- Biology
- Default (for any other topic)

Example response:
"Here is a joke about TOPIC:
<JOKE>

Explanation: {brief explanation if needed}"

If the user asked about anything else, delegate the task to the manager agent.
"""


funny_nerd = Agent(
    name="funny_nerd",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="A funny nerd who tells nerdy jokes about various topics",
    instruction=SYSTEM_PROMPT,
    tools=[get_nerd_joke],
)