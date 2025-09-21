from google.adk.tools.tool_context import ToolContext
from typing import Optional, List


def _ensure_state(tool_context: ToolContext) -> None:
    st = tool_context.state
    if "user_name" not in st or st["user_name"] is None:
        st["user_name"] = ""
    if "reading_list" not in st or st["reading_list"] is None:
        st["reading_list"] = []


def _valid_status(status: Optional[str]) -> bool:
    return status in {None, "to read", "currently reading", "read"}

def normalize_status(status: Optional[str]) -> Optional[str]:
    if not status:
        return None
    mapping = {
        "to read": "to read",
        "queued": "to read",
        "reading": "currently reading",
        "currently reading": "currently reading",
        "done": "read",
        "read": "read"
    }
    return mapping.get(status.lower())


def set_user_name(name: str, tool_context: ToolContext) -> dict:
    _ensure_state(tool_context)
    old = tool_context.state.get("user_name", "")
    tool_context.state["user_name"] = name or ""
    return {
        "action": "set_user_name",
        "old_name": old,
        "new_name": tool_context.state["user_name"],
        "message": f"Saved your name as '{tool_context.state['user_name'] or 'Unknown'}'.",
    }


def add_item(
    title: str,
    status: str,
    notes: str,
    tool_context: ToolContext,
) -> dict:

    _ensure_state(tool_context)
    if not _valid_status(status):
        status = "queued"

    item = {
        "title": title.strip() if title else "(untitled)",
        "status": status,
        "notes": (notes or "").strip(),
    }
    rl = tool_context.state["reading_list"]
    rl.append(item)
    tool_context.state["reading_list"] = rl

    return {
        "action": "add_item",
        "item": item,
        "index": len(rl),
        "message": f"Added '{item['title']}' to your reading list.",
    }


def list_items(
    filter_status: Optional[str] = None,
    tool_context: ToolContext = None,
) -> dict:

    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    filtered = []
    for it in rl:
        if filter_status and it.get("status") != filter_status:
            continue
        filtered.append(it)

    return {
        "action": "list_items",
        "count": len(filtered),
        "items": filtered,
        "filters": {"status": filter_status},
        "message": f"Found {len(filtered)} item(s).",
    }


def update_item(
    index: int,
    title: Optional[str] = None,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    tool_context: ToolContext = None,
) -> dict:

    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    if index < 1 or index > len(rl):
        return {
            "action": "update_item",
            "status": "error",
            "message": f"No item at position {index}. You currently have {len(rl)} item(s).",
        }

    item = rl[index - 1]
    before = item.copy()

    if title is not None:
        item["title"] = title.strip() or item["title"]

    # Normalize the status before updating
    normalized_status = normalize_status(status)
    if normalized_status and _valid_status(normalized_status):
        item["status"] = normalized_status

    if notes is not None:
        item["notes"] = (notes or "").strip()

    rl[index - 1] = item
    tool_context.state["reading_list"] = rl

    return {
        "action": "update_item",
        "index": index,
        "before": before,
        "after": item,
        "message": f"Updated item {index} ('{before.get('title','')}').",
    }




def annotate_item(
    index: int,
    notes: str,
    tool_context: ToolContext,
) -> dict:

    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    if index < 1 or index > len(rl):
        return {
            "action": "annotate_item",
            "status": "error",
            "message": f"No item at position {index}. You currently have {len(rl)} item(s).",
        }

    item = rl[index - 1]
    before_notes = item.get("notes", "")
    item["notes"] = (notes or "").strip()
    rl[index - 1] = item
    tool_context.state["reading_list"] = rl

    return {
        "action": "annotate_item",
        "index": index,
        "old_notes": before_notes,
        "new_notes": item["notes"],
        "message": f"Noted item {index} ('{item.get('title','')}').",
    }


def remove_item(index: int, tool_context: ToolContext) -> dict:
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    if index < 1 or index > len(rl):
        return {
            "action": "remove_item",
            "status": "error",
            "message": f"No item at position {index}. You currently have {len(rl)} item(s).",
        }

    removed = rl.pop(index - 1)
    tool_context.state["reading_list"] = rl

    return {
        "action": "remove_item",
        "index": index,
        "removed": removed,
        "message": f"Removed '{removed.get('title','')}' from your reading list.",
    }
