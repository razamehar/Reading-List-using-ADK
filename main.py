import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from src.app.config.state import INITIAL_STATE
from src.app.agents.agent import reading_agent
from src.app.utils.utils import call_agent_async, display_state_async
from src.app.utils.session import get_or_create_session
from src.app.db.db_init import initialize_db


load_dotenv()

DB_URL = os.getenv("DB_URL")
APP_NAME = os.getenv("ADK_APP_NAME")
USER_ID = os.getenv("ADK_USER_ID")

session_service = initialize_db(DB_URL)


async def main_async():
    session_id = await get_or_create_session(session_service, APP_NAME, USER_ID, INITIAL_STATE)
    runner = Runner(agent=reading_agent, app_name=APP_NAME, session_service=session_service)

    print(f"\nWelcome to {APP_NAME}! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "bye", "goodbye", "good bye"}:
            print("Your reading list has been saved.")
            print("Bye")
            break

        await display_state_async(session_service, APP_NAME, USER_ID, session_id, "State BEFORE")
        await call_agent_async(runner, USER_ID, session_id, user_input)
        await display_state_async(session_service, APP_NAME, USER_ID, session_id, "State AFTER")


if __name__ == "__main__":
    asyncio.run(main_async())
