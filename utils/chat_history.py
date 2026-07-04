from utils.storage import load_data, save_data
import uuid
from datetime import datetime


def create_session(title="New Chat"):
    """Create a new chat session with initial message storage"""
    data = load_data()

    session = {
        "session_id": str(uuid.uuid4()),
        "title": title,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": [],
        "message_count": 0  # Track for auto-title generation
    }

    data["sessions"].append(session)
    save_data(data)

    return session["session_id"]


def get_sessions():
    """Retrieve all sessions sorted by most recent first"""
    data = load_data()
    # Sort by creation date (newest first)
    sessions = sorted(
        data.get("sessions", []),
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )
    return sessions


def get_session_messages(session_id):
    """Get all messages from a specific session"""
    data = load_data()
    for session in data.get("sessions", []):
        if session["session_id"] == session_id:
            return session.get("messages", [])
    return []


def add_message(session_id, role, text):
    """Add a message to session and auto-generate title if needed"""
    data = load_data()

    for session in data["sessions"]:
        if session["session_id"] == session_id:
            # Add message
            session["messages"].append({
                "role": role,
                "text": text,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Auto-generate title from first user message
            if role == "user" and session["title"] == "New Chat":
                # Trim to 30 characters max
                title = text[:30] + ("..." if len(text) > 30 else "")
                session["title"] = title
            
            break

    save_data(data)


def update_session_title(session_id, new_title):
    """Update the title of an existing session"""
    data = load_data()
    
    for session in data["sessions"]:
        if session["session_id"] == session_id:
            session["title"] = new_title
            break
    
    save_data(data)


def delete_session(session_id):
    """Delete a session and all its messages"""
    data = load_data()
    data["sessions"] = [s for s in data["sessions"] if s["session_id"] != session_id]
    save_data(data)


def clear_all():
    """Clear all sessions"""
    save_data({"sessions": []})