import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Insurance Claim Helper",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🛡️ Insurance AI")

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

    if st.button("💬 Claim Assistant", use_container_width=True):
        st.session_state.page = "Assistant"

    if st.button("📄 Document Checklist", use_container_width=True):
        st.session_state.page = "Checklist"

    if st.button("📤 Upload Documents", use_container_width=True):
        st.session_state.page = "Upload"

    if st.button("📜 Chat History", use_container_width=True):
        st.session_state.page = "History"

    st.markdown("---")
    st.caption("Version 1.0")

# -----------------------------
# Pages
# -----------------------------
if st.session_state.page == "Home":
    st.title("🏠 Home")
    st.write("Welcome to AI Insurance Claim Helper.")

elif st.session_state.page == "Assistant":
    st.title("💬 Claim Assistant")
    st.write("Ask your insurance-related questions here.")

elif st.session_state.page == "Checklist":
    st.title("📄 Document Checklist")
    st.write("Generate claim document checklists.")

elif st.session_state.page == "Upload":
    st.title("📤 Upload Documents")
    st.write("Upload your claim documents.")

elif st.session_state.page == "History":
    st.title("📜 Chat History")
    st.write("View previous conversations.")