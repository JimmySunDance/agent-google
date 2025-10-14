import asyncio
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from question_answering_agent.agent import question_answering_agent


async def main():
    # Create a new session service to store state
    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Adam Smith", 
        "user_preferences": """
    I Like to play Tennis and go climbing. 
    My favorite food is Italian, especially pizza. 
    My favorite music is blues and rock. 
    My favorite movies are action and thriller.
    """
    }

    APP_NAME="John Bot"
    USER_ID="John_Smith_1234"
    SESSION_ID=str(uuid.uuid4())

    await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    print("CREATED NEW SESSION")
    print(f"SESSION ID: {SESSION_ID}")

    runner = Runner(
        app_name=APP_NAME,
        agent=question_answering_agent,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role="user", parts=[types.Part(text="What is Johns favorite food?")]
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print("\nFINAL RESPONSE:")
                print(event.content.parts[0].text)


    print("\n==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(session)

    print("\n==== Final Session State ====")
    if session:
        for key, value in session.state.items():
            print(f"{key}: {value}")
    else:
        print("Session not found.")
    
    return

if __name__ == "__main__":
    asyncio.run(main())