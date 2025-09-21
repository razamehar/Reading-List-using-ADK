async def get_or_create_session(session_service, app_name, user_id, initial_state):
    existing = await session_service.list_sessions(app_name=app_name, user_id=user_id)

    if getattr(existing, "sessions", None):
        session_id = existing.sessions[0].id
        print(f"Continuing existing session: {session_id}")
    else:
        new_session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            state=initial_state,
        )
        session_id = new_session.id
        print(f"Created new session: {session_id}")
    return session_id