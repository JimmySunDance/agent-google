from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

prompt_path = "./memory_agent/agent_prompt.txt"
PROMPT = open(prompt_path).read()

def add_reminder(remainder:str, tool_context:ToolContext) -> dict:
    """
    Add a new reminder to the user's reminders list.
    
    Args: 
        reminder (str): The reminder text to add.
        tool_context: Context for accessing and updating session state.

    Returns:
        a conformation message.
    """
    print(f"--- Tool: added_reminder called with: {remainder} ---")

    reminders = tool_context.state.get("reminders", [])
    reminders.append(remainder)
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": remainder,
        "message": f"Reminder added: {remainder}",
    }


def view_reminders(tool_context:ToolContext) -> dict:
    """View all current reminders.

    Args:
        tool_context: Context for accessing session state

    Returns:
        The list of reminders
    """
    print("--- Tool: view_reminders called ---")
    reminders = tool_context.state.get("reminders", [])

    return {
        "action": "view_reminders", 
        "reminders": reminders, 
        "count": len(reminders)
    }

def update_reminder(
        index: int, updated_text: str, tool_context: ToolContext
    ) -> dict:
    """Update an existing reminder.

    Args:
        index: The 1-based index of the reminder to update
        updated_text: The new text for the reminder
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(
        f"--- Tool: update_reminder called for index {index} with '{updated_text}' ---"
    )

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"Could not find reminder at position {index}. Currently there are {len(reminders)} reminders.",
        }

    # Update the reminder (adjusting for 0-based indices)
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text

    # Update state with the modified list
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_text": old_reminder,
        "updated_text": updated_text,
        "message": f"Updated reminder {index} from '{old_reminder}' to '{updated_text}'",
    }


def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete a reminder.

    Args:
        index: The 1-based index of the reminder to delete
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: delete_reminder called for index {index} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"Could not find reminder at position {index}. Currently there are {len(reminders)} reminders.",
        }

    # Remove the reminder (adjusting for 0-based indices)
    deleted_reminder = reminders.pop(index - 1)

    # Update state with the modified list
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"Deleted reminder {index}: '{deleted_reminder}'",
    }


def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_user_name called with '{name}' ---")

    # Get current name from state
    old_name = tool_context.state.get("user_name", "")

    # Update the name in state
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"Updated your name to: {name}",
    }


memory_agent = Agent(
    name="memory_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="Reminder agent with persistent memory",
    instruction=PROMPT,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
)