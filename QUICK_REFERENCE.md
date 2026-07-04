# 🚀 Quick Reference - Chat History System

## ⚡ Quick Start
```bash
# Navigate to project
cd c:\Users\Sai Kumar\Desktop\internship\AI-Insurance-Claim-Helper

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the app
python -m streamlit run app.py

# Open browser
# http://localhost:8501
```

## 🎯 Key Functions

### Chat History Functions (utils/chat_history.py)
```python
# Create new session
create_session("New Chat")  # Returns session_id

# Get all sessions
get_sessions()  # Returns list sorted by date

# Get messages from session
get_session_messages(session_id)  # Returns list of messages

# Add message (auto-saves & auto-titles)
add_message(session_id, "user", "Your question")
add_message(session_id, "assistant", "AI response")

# Update session title
update_session_title(session_id, "New Title")

# Delete operations
delete_session(session_id)
clear_all()  # Delete everything
```

## 📊 Session Structure
```python
{
    "session_id": "uuid-string",
    "title": "First message or custom (max 30 chars)",
    "created_at": "2026-07-05 10:30:45",
    "messages": [
        {"role": "user", "text": "...", "timestamp": "..."},
        {"role": "assistant", "text": "...", "timestamp": "..."}
    ]
}
```

## 🎨 UI Features

| Feature | Location | Action |
|---------|----------|--------|
| **New Chat** | Sidebar | Create new session |
| **Session List** | Sidebar | Click to switch session |
| **Delete Session** | Sidebar | 🗑️ button next to session |
| **Clear All** | Sidebar | ❌ button at bottom |
| **Send Message** | Assistant page | Type & click 🚀 |
| **Clear Chat** | Assistant page | 🔄 button |
| **View History** | History page | See all conversations |

## 🔑 Session State Variables

```python
st.session_state.current_session  # Active session ID
st.session_state.page             # Current page being displayed
st.session_state.initialized      # Flag to prevent duplicate creation
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Main app with session management & UI |
| `utils/chat_history.py` | Session/message functions |
| `utils/storage.py` | JSON read/write utilities |
| `data.json` | Session storage |
| `pages/2_Claim_Assistant.py` | Alternative multipage component |

## ⚙️ How Auto Session Creation Works

1. App starts → checks `if "current_session" not in st.session_state`
2. Loads sessions from `data.json`
3. If no sessions exist → creates one automatically
4. If sessions exist but none selected → loads latest
5. Sets `initialized = True` to prevent duplicate on rerun

## 💾 Message Flow

```
User sends message
    ↓
add_message(session_id, "user", text)
    ↓
If title == "New Chat" → update to first 30 chars
    ↓
Send to AI API
    ↓
add_message(session_id, "assistant", response)
    ↓
Both saved to data.json automatically
    ↓
Display updated chat
```

## 🔍 Common Tasks

### Switch to Different Session
```python
st.session_state.current_session = session_id
st.rerun()
```

### Save User Message
```python
from utils.chat_history import add_message
add_message(st.session_state.current_session, "user", user_text)
```

### Get Current Session Messages
```python
from utils.chat_history import get_session_messages
messages = get_session_messages(st.session_state.current_session)
for msg in messages:
    print(f"{msg['role']}: {msg['text']}")
```

### Clear Current Session
```python
from utils.storage import load_data, save_data
data = load_data()
for s in data["sessions"]:
    if s["session_id"] == st.session_state.current_session:
        s["messages"] = []
save_data(data)
```

## ⚠️ Common Issues

### No messages appear after refresh?
- Check `data.json` exists
- Verify session_id matches
- Check browser cache (Ctrl+Shift+Del)

### New sessions created every refresh?
- Make sure `initialized` flag is working
- Check if `st.rerun()` is being called unnecessarily
- Verify session state initialization order

### Session not saving?
- Check write permissions on `data.json`
- Verify `add_message()` is being called
- Check for JSON syntax errors

### App crashes on startup?
- Verify `utils/chat_history.py` imports work
- Check `data.json` is valid JSON
- Look for Python syntax errors: `python -m py_compile app.py`

## 📈 Performance Tips

- Sessions sorted by date → faster access to recent chats
- Lazy load messages (only display when viewing)
- Use expanders for message history (reduces DOM size)
- Limit message display in preview (show count instead)

## 🔄 Auto-Title Generation Logic

```python
if role == "user" and session["title"] == "New Chat":
    title = text[:30] + ("..." if len(text) > 30 else "")
    session["title"] = title
```

Example:
- User: "What documents do I need for a car accident claim?"
- Title becomes: "What documents do I need fo..."

## 🎯 Architecture Overview

```
app.py (Main Entry)
    ├── Initialize Session State
    ├── Render Sidebar
    │   └── Session Management
    └── Route to Pages
        ├── Home
        ├── Assistant (Chat)
        ├── Checklist
        ├── Upload
        ├── Status
        └── History
        
utils/chat_history.py
    ├── Session CRUD
    ├── Message Management
    └── Auto-Title Logic
    
utils/storage.py
    ├── JSON I/O
    └── Error Handling
    
data.json
    └── Session Storage
```

## ✅ Verification Checklist

- [ ] App starts without errors
- [ ] First session auto-created
- [ ] Messages save after sending
- [ ] Messages persist after refresh
- [ ] Session title auto-generates
- [ ] Can switch between sessions
- [ ] Can delete sessions
- [ ] History page shows conversations
- [ ] Timestamps on all messages

---

**Version 1.0 - Production Ready** ✨
