from google.adk.sessions import DatabaseSessionService


def initialize_db(db_url: str) -> DatabaseSessionService:
    return DatabaseSessionService(db_url=db_url)
