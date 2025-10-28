from datetime import datetime

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

prompt_path = "./customer_service_agent/sub_agents/order_agent/agent_prompt.txt"
PROMPT = open(prompt_path).read()

def get_current_time() -> dict:
    """
    Get the current date and time in the format YYYY-MM-DD HH:MM:SS.
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def refund_course(tool_context: ToolContext) -> dict:
    """
    Simulates refunding the AI Marketing Platform course.
    Updates state by removing the course from purchased_courses.
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current purchased courses
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user owns the course
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id not in course_ids:
        return {
            "status": "error",
            "message": "You don't own this course, so it can't be refunded.",
        }

    # Create new list without the course to be refunded
    new_purchased_courses = []
    for course in current_purchased_courses:
        # Skip empty entries or non-dict entries
        if not course or not isinstance(course, dict):
            continue
        # Skip the course being refunded
        if course.get("id") == course_id:
            continue
        # Keep all other courses
        new_purchased_courses.append(course)

    # Update purchased courses in state via assignment
    tool_context.state["purchased_courses"] = new_purchased_courses

    # Get current interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])

    # Create new interaction history with refund added
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append(
        {"action": "refund_course", "course_id": course_id, "timestamp": current_time}
    )

    # Update interaction history in state via assignment
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": """Successfully refunded the AI Marketing Platform course! 
         Your $149 will be returned to your original payment method within 3-5 business days.""",
        "course_id": course_id,
        "timestamp": current_time,
    }


# Create the order agent
order_agent = Agent(
    name="order_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="Order agent for viewing purchase history & processing refunds",
    instruction=PROMPT,
    tools=[
        refund_course, 
        get_current_time
    ],
)