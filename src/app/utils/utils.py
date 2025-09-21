from google.genai import types


async def display_state_async(session_service, app_name, user_id, session_id, label="State"):
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        st = session.state or {}
        print(f"\n---- {label} ----")

        user_name = st.get("user_name", "") or "Unknown"
        print(f"User: {user_name}")

        items = st.get("reading_list", [])
        if not items:
            print("Reading List: [empty]")
        else:
            print("Reading List:")
            for i, it in enumerate(items, 1):
                title = it.get("title", "(untitled)")
                status = it.get("status", "queued")
                tags = ", ".join(it.get("tags", []) or [])
                url = it.get("url", "")
                notes = it.get("notes", "")
                print(f"  {i}. {title}  [{status}]")
                if url:
                    print(f"     URL: {url}")
                if tags:
                    print(f"     Tags: {tags}")
                if notes:
                    print(f"     Notes: {notes}")

        print("-" * (12 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    print(f"Event ID: {event.id}, Author: {event.author}")

    if event.content and event.content.parts:
        for part in event.content.parts:
            if getattr(part, "text", None):
                txt = (part.text or "").strip()
                if txt:
                    print(f"Text: '{txt}'")
            if getattr(part, "tool_response", None):
                print(f"Tool Response: {part.tool_response.output}")
            if getattr(part, "executable_code", None):
                print("Executable Code:\n", part.executable_code.code)
            if getattr(part, "code_execution_result", None):
                cer = part.code_execution_result
                print(f"Code Result: {cer.outcome}\n{cer.output}")

    if event.is_final_response():
        final_text = ""
        if event.content and event.content.parts and getattr(event.content.parts[0], "text", None):
            final_text = (event.content.parts[0].text or "").strip()

        if final_text:
            print(f"AGENT RESPONSE:\n{final_text}\n")
        else:
            print("Final Agent Response: [No text in final event]\n")
        return final_text

    return None


async def call_agent_async(runner, user_id, session_id, query: str):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"\nRunning Query: {query}")

    final_response_text = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            maybe_text = await process_agent_response(event)
            if maybe_text:
                final_response_text = maybe_text
    except Exception as e:
        print(f"Error during agent call: {e}")

    return final_response_text
