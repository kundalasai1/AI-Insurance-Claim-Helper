import os
import streamlit as st
from utils.chatbot import ask_gemini, generate_checklist
from utils.checklist import load_checklist, get_documents
from utils.document_analyzer import analyze_document
from utils.database import get_claim_status
from utils.chat_history import (
    create_session,
    get_sessions,
    delete_session,
    clear_all,
    add_message,
    get_session_messages
)

# ======================
# INITIALIZE SESSION STATE
# ======================
# Must be done BEFORE st.set_page_config()

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False

if "show_stats" not in st.session_state:
    st.session_state.show_stats = False

# Auto-create first session on app startup (only once per session)
if not st.session_state.initialized:
    sessions = get_sessions()
    
    if not sessions:
        # No sessions exist - create first one
        new_session_id = create_session("New Chat")
        st.session_state.current_session = new_session_id
    elif st.session_state.current_session is None:
        # Sessions exist but none selected - use latest
        st.session_state.current_session = sessions[0]["session_id"]
    
    st.session_state.initialized = True

# ======================
# PAGE CONFIGURATION
# ======================
st.set_page_config(
    page_title="AI Insurance Claim Helper",
    page_icon="🛡️",
    layout="wide"
)

# Hide the default multipage navigation
hide_multipage_nav = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stSidebarContent"] {
            padding-top: 0 !important;
        }
    </style>
"""
st.markdown(hide_multipage_nav, unsafe_allow_html=True)


# ======================
# SIDEBAR
# ======================
with st.sidebar:
    # Header with Logo
    col_logo, col_title = st.columns([0.3, 0.7])
    with col_logo:
        st.markdown("# 🛡️")
    with col_title:
        st.markdown("### Insurance AI")
    
    st.markdown("---")

    # Navigation Section
    st.markdown("#### 🗂️ **Navigation**")
    
    pages = [
        ("🏠 Home", "Home"),
        ("💬 Assistant", "Assistant"),
        ("📋 Status", "Status"),
        ("📄 Checklist", "Checklist"),
        ("📤 Upload", "Upload"),
        ("📜 History", "History"),
    ]
    
    # Display navigation buttons in single column
    for page_display, page_key in pages:
        is_active = st.session_state.page == page_key
        btn_type = "primary" if is_active else "secondary"
        
        if st.button(
            page_display,
            key=f"nav_{page_key}",
            use_container_width=True,
            type=btn_type
        ):
            st.session_state.page = page_key
    
    st.markdown("---")

    # Chat Sessions Section
    st.markdown("#### 💬 **Chat Sessions**")
    
    # Session Controls
    col_new, col_sort = st.columns([2, 1])
    
    with col_new:
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            new_session_id = create_session("New Chat")
            st.session_state.current_session = new_session_id
            st.rerun()
    
    with col_sort:
        if st.button("↻", help="Refresh sessions", use_container_width=True):
            st.rerun()
    
    # Session Search/Filter
    search_query = st.text_input(
        "🔍 Search sessions",
        placeholder="Type to filter...",
        label_visibility="collapsed",
        key="session_search"
    )
    
    st.markdown("---")

    # Display Sessions List
    sessions = get_sessions()
    
    if sessions:
        # Session Stats
        cols_stats = st.columns(3)
        with cols_stats[0]:
            st.metric("Total", len(sessions), delta=None)
        with cols_stats[1]:
            messages_count = sum(len(s.get("messages", [])) for s in sessions)
            st.metric("Messages", messages_count)
        with cols_stats[2]:
            st.metric("Active", "✓" if st.session_state.current_session else "✗")
        
        st.markdown("---")
        
        # Filter sessions by search query
        filtered_sessions = [
            s for s in sessions 
            if search_query.lower() in s["title"].lower()
        ] if search_query else sessions
        
        if filtered_sessions:
            for session in filtered_sessions:
                session_id = session["session_id"]
                title = session["title"]
                is_active = session_id == st.session_state.current_session
                msg_count = len(session.get("messages", []))
                created_at = session.get("created_at", "N/A")
                
                # Session Card
                session_container = st.container(border=is_active)
                
                with session_container:
                    # Session Title and Controls
                    col_title_main, col_delete = st.columns([3.5, 0.5])
                    
                    with col_title_main:
                        # Active indicator
                        if is_active:
                            st.markdown(f"**◀ {title}** ✨")
                        else:
                            st.markdown(f"{title}")
                        
                        # Session metadata
                        col_date, col_msgs = st.columns(2)
                        with col_date:
                            st.caption(f"📅 {created_at[:10]}")
                        with col_msgs:
                            st.caption(f"💬 {msg_count} msgs")
                        
                        # Click to activate
                        if st.button(
                            "📂 Open",
                            key=f"session_btn_{session_id}",
                            use_container_width=True,
                            type="primary" if is_active else "secondary"
                        ):
                            st.session_state.current_session = session_id
                            st.rerun()
                    
                    with col_delete:
                        if st.button(
                            "🗑️",
                            key=f"del_{session_id}",
                            help="Delete session"
                        ):
                            delete_session(session_id)
                            if session_id == st.session_state.current_session:
                                remaining = get_sessions()
                                st.session_state.current_session = remaining[0]["session_id"] if remaining else None
                            st.rerun()
        else:
            st.info(f"No sessions matching '{search_query}'")
    else:
        st.info("📭 No sessions yet. Create one to start!")
    
    st.markdown("---")
    
    # Session Management
    st.markdown("#### ⚙️ **Settings**")
    
    col_settings_1, col_settings_2 = st.columns(2)
    
    with col_settings_1:
        if st.button("🔄 Clear All", use_container_width=True):
            if st.session_state.get("confirm_clear"):
                clear_all()
                st.session_state.current_session = None
                st.session_state.initialized = False
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm")
    
    with col_settings_2:
        if st.button("📊 Stats", use_container_width=True):
            st.session_state.show_stats = not st.session_state.get("show_stats", False)
    
    if st.session_state.get("show_stats"):
        st.markdown("**📈 Session Stats**")
        total_sessions = len(sessions)
        total_messages = sum(len(s.get("messages", [])) for s in sessions)
        avg_messages = total_messages / total_sessions if total_sessions > 0 else 0
        
        st.metric("Sessions", total_sessions)
        st.metric("Total Messages", total_messages)
        st.metric("Avg per Session", f"{avg_messages:.1f}")
    
    st.markdown("---")
    st.caption("🚀 v1.1 • Insurance Helper")


# ======================
# PAGE ROUTING
# ======================

if st.session_state.page == "Home":
    st.title("🏠 Home")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Welcome to AI Insurance Claim Helper 🛡️
        
        This intelligent assistant helps you with:
        - **📋 Claim Processing**: Quick answers to insurance questions
        - **📄 Document Checklist**: Get required documents for your claim
        - **📤 Document Upload**: Securely upload your insurance documents
        - **📊 Claim Status**: Track your claim in real-time
        """)
    
    with col2:
        st.info("""
        **Current Session:** 
        
        """ + (f"✓ Active" if st.session_state.current_session else "⚠️ No session"))

elif st.session_state.page == "Assistant":
    st.title("💬 AI Insurance Claim Assistant")
    
    if not st.session_state.current_session:
        st.warning("⚠️ No active session. Creating one now...")
        new_session_id = create_session("New Chat")
        st.session_state.current_session = new_session_id
        st.rerun()
    
    # Display Chat History
    messages = get_session_messages(st.session_state.current_session)
    
    st.subheader("Chat History")
    
    if messages:
        for msg in messages:
            with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["text"])
                st.caption(msg.get("timestamp", ""))
    else:
        st.info("No messages yet. Start a conversation!")
    
    st.divider()
    
    # Input Section
    st.subheader("Your Question")
    question = st.text_area(
        "Ask any insurance-related question:",
        placeholder="Example: What documents are required for a car accident claim?",
        height=100,
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        submit_btn = st.button("🚀 Send Message", use_container_width=True)
    with col2:
        clear_btn = st.button("🔄 Clear Chat", use_container_width=True)
    
    if clear_btn:
        # Clear this session's messages
        sessions = get_sessions()
        for s in sessions:
            if s["session_id"] == st.session_state.current_session:
                s["messages"] = []
                break
        st.rerun()
    
    if submit_btn:
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Save user message
            add_message(st.session_state.current_session, "user", question)
            
            # Get AI response
            with st.spinner("🤖 Thinking..."):
                try:
                    answer = ask_gemini(question)
                except Exception as e:
                    answer = f"Sorry, I encountered an error: {str(e)}"
            
            # Save AI response
            add_message(st.session_state.current_session, "assistant", answer)
            
            st.rerun()

elif st.session_state.page == "Checklist":

    st.title("📄 Document Checklist Generator")

    insurance_data = load_checklist()

    claim_type = st.selectbox(
        "Select Claim Type",
        list(insurance_data.keys()),
        key="claim_type"
    )

    st.info(insurance_data[claim_type]["description"])

    if "show_checklist" not in st.session_state:
        st.session_state.show_checklist = False

    if st.button("Generate Checklist", key="generate_btn"):
        st.session_state.show_checklist = True

    if st.session_state.show_checklist:

        st.success("Required Documents")

        for i, doc in enumerate(insurance_data[claim_type]["documents"]):
            st.checkbox(
                doc,
                key=f"{claim_type}_{i}"
            )
    st.divider()

    st.info(
      f"Total Required Documents: {len(insurance_data[claim_type]['documents'])}"
    )
    checklist_text = f"Insurance Claim Type: {claim_type}\n\n"

    for doc in insurance_data[claim_type]["documents"]:
        checklist_text += f"☐ {doc}\n"

    st.download_button(
        label="📥 Download Checklist",
        data=checklist_text,
        file_name=f"{claim_type}_Checklist.txt",
        mime="text/plain"
    )
    # ---------------------------------------
    # AI Checklist Generator
    # ---------------------------------------

    st.divider()

    st.subheader("🤖 AI Checklist Generator")

    incident = st.text_area(
        "Describe your incident",
        placeholder="Example: My bike met with an accident yesterday.",
        key="incident_input"
    )

    if st.button("Generate AI Checklist", key="ai_checklist_btn"):

        if incident.strip():

            with st.spinner("Generating checklist..."):

                result = generate_checklist(incident)

            st.markdown(result)

        else:

            st.warning("Please describe your incident.")

elif st.session_state.page == "Upload":

    st.title("📤 Upload Insurance Documents")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        st.success("File uploaded successfully!")

        st.write("### File Information")
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Type:** {uploaded_file.type}")
        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

        os.makedirs("uploads", exist_ok=True)

        save_path = os.path.join("uploads", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File saved successfully!")

        if uploaded_file.type.startswith("image"):
            st.image(
                uploaded_file,
                caption="Uploaded Image",
                use_container_width=True
            )

        elif uploaded_file.type == "application/pdf":
            st.info("PDF uploaded successfully.")

elif st.session_state.page == "Status":

    st.title("📋 Claim Status Checker")

    claim_id = st.text_input(
        "Enter Claim ID",
        placeholder="Example: CLM1001"
    )

    if st.button("Check Status"):

        result = get_claim_status(claim_id)

        if result:

            st.success("Claim Found")

            st.write(f"**Status:** {result['status']}")
            st.write(f"**Last Updated:** {result['updated']}")

        else:

            st.error("Claim ID not found.")

elif st.session_state.page == "History":
    st.title("📜 Chat History")
    
    sessions = get_sessions()
    
    if not sessions:
        st.info("No chat history yet. Start a conversation in the Claim Assistant!")
    else:
        st.write(f"**Total Sessions:** {len(sessions)}")
        
        for session in sessions:
            with st.expander(f"📋 {session['title']}", expanded=False):
                st.caption(f"Session ID: {session['session_id']}")
                st.caption(f"Created: {session.get('created_at', 'N/A')}")
                
                messages = session.get("messages", [])
                
                if messages:
                    st.write(f"**Messages:** {len(messages)}")
                    for msg in messages:
                        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
                            st.markdown(msg["text"])
                            st.caption(msg.get("timestamp", ""))
                else:
                    st.info("No messages in this session")