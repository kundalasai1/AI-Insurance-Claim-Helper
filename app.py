import os
import streamlit as st
from utils.chatbot import ask_gemini
from utils.checklist import load_checklist, get_documents
from utils.document_analyzer import analyze_document

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

    st.title("💬 AI Insurance Claim Assistant")

    st.write("Ask any insurance-related question.")

    question = st.text_area(
        "Enter your question",
        placeholder="Example: What documents are required for a car accident claim?"
    )

    if st.button("Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:
            with st.spinner("Thinking..."):
                answer = ask_gemini(question)

            st.success("AI Response")

            st.write(answer)

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
    
elif st.session_state.page == "History":
    st.title("📜 Chat History")
    st.write("View previous conversations.")