"""
Claim Assistant Page - Multi-page Streamlit component
Provides persistent chat functionality with message history
"""

import streamlit as st
from utils.chat_history import (
    get_session_messages,
    add_message,
    get_sessions
)
from utils.chatbot import ask_gemini

# Set page config
st.set_page_config(
    page_title="Claim Assistant",
    page_icon="💬",
    layout="wide"
)

st.title("💬 AI Insurance Claim Assistant")

# Ensure current_session is set (fallback to latest session)
if "current_session" not in st.session_state:
    sessions = get_sessions()
    if sessions:
        st.session_state.current_session = sessions[0]["session_id"]
    else:
        st.error("No active session. Please create one from the main app.")
        st.stop()

# Get current session details
sessions = get_sessions()
current_session = None
for s in sessions:
    if s["session_id"] == st.session_state.current_session:
        current_session = s
        break

if not current_session:
    st.error("Session not found. Please select a session from the main app.")
    st.stop()

# Display current session info
st.markdown(f"**Current Session:** {current_session['title']}")
st.markdown(f"**Created:** {current_session.get('created_at', 'N/A')}")
st.divider()

# Display Chat History
messages = get_session_messages(st.session_state.current_session)

st.subheader("Chat History")

if messages:
    for msg in messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["text"])
            if "timestamp" in msg:
                st.caption(msg["timestamp"])
else:
    st.info("💭 No messages yet. Start a conversation below!")

st.divider()

# Input Section
st.subheader("Ask a Question")

col1, col2 = st.columns([4, 1])

with col1:
    question = st.text_area(
        "Your question:",
        placeholder="Example: What documents are required for a car accident claim?",
        height=100,
        label_visibility="collapsed"
    )

with col2:
    submit_btn = st.button("🚀 Send", use_container_width=True, type="primary", key="send_btn")
    clear_btn = st.button("🔄 Clear", use_container_width=True, key="clear_btn")

if clear_btn:
    # Clear this session's messages
    from utils.storage import load_data, save_data
    data = load_data()
    for s in data["sessions"]:
        if s["session_id"] == st.session_state.current_session:
            s["messages"] = []
            break
    save_data(data)
    st.success("Chat cleared!")
    st.rerun()

if submit_btn:
    if question.strip() == "":
        st.warning("⚠️ Please enter a question.")
    else:
        # Save user message
        add_message(st.session_state.current_session, "user", question)
        
        # Get AI response
        with st.spinner("🤖 Thinking..."):
            try:
                answer = ask_gemini(question)
            except Exception as e:
                answer = f"❌ Sorry, I encountered an error: {str(e)}"
        
        # Save AI response
        add_message(st.session_state.current_session, "assistant", answer)
        
        st.success("Message saved!")
        st.rerun()
