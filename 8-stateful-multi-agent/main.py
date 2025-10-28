import asyncio
from typing import Dict, Any

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from customer_service_agent.agent import customer_service_agent
from utils import add_user_query_to_history, call_agent_async

# Constants
APP_NAME = "Customer Service Agent"
USER_ID = "ai_with_james"

# ===== PART 1: Initialize In-Memory Session Service =====
session_service = InMemorySessionService()

# ===== PART 2: Define Initial State =====
initial_state: Dict[str, Any] = {
    "user_name": "John Smyth",
    "purchased_courses": [],
    "interaction_history": [],
}

async def main_async():
    # Setup constants
    APP_NAME = "Customer Service Agent"
    USER_ID = "ai_with_james"

    # ===== PART 3: Session Management - Find or Create =====
    try:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        if not new_session:
            raise RuntimeError("Failed to create session")
        
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")
    except Exception as e:
        print(f"Error creating session: {str(e)}")
        return

    # ===== PART 4: Agent Runner Setup =====
    # Create a runner with the customer service agent
    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nWelcome to Customer Service Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")


    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the conversation. Goodbye!")
            break

        await add_user_query_to_history(
            session_service=session_service,
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
            query=user_input
        )

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # ===== PART 6: State Examination =====
    # Show final session state
    final_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if final_session is None:
        print("\nError: Could not retrieve final session state")
    else:
        print("\nFinal Session State:")
        for key, value in final_session.state.items():
            print(f"{key}: {value}")



if __name__ == "__main__":
    asyncio.run(main_async())