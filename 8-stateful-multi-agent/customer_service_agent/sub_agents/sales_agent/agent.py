from datetime import datetime

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext



prompt_path = "./customer_service_agent/sub_agents/policy_agent/agent_prompt.txt"
PROMPT = open(prompt_path).read()


def purchase_course(tool_context: ToolContext) -> dict:
    """
    Simulates purchasing the AI Marketing Platform course.
    Updates state with purchase information.
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current purchased courses
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user already owns the course
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id in course_ids:
        return {"status": "error", "message": "You already own this course!"}

    # Create new list with the course added
    new_purchased_courses = []
    # Only include valid dictionary courses
    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            new_purchased_courses.append(course)

    # Add the new course as a dictionary with id and purchase_date
    new_purchased_courses.append({"id": course_id, "purchase_date": current_time})

    # Update purchased courses in state via assignment
    tool_context.state["purchased_courses"] = new_purchased_courses

    # Get current interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])

    # Create new interaction history with purchase added
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append(
        {"action": "purchase_course", "course_id": course_id, "timestamp": current_time}
    )

    # Update interaction history in state via assignment
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": "Successfully purchased the AI Marketing Platform course!",
        "course_id": course_id,
        "timestamp": current_time,
    }


# Create the sales agent
sales_agent = Agent(
    name="sales_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="Sales agent for the AI Marketing Platform course",
    instruction=PROMPT,
    tools=[purchase_course],
)