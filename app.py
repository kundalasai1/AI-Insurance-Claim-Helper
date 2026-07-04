import os
import streamlit as st
from utils.chatbot import ask_gemini
from utils.checklist import load_checklist
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

    st.title("📄 Insurance Document Checklist")

    insurance_data = load_checklist()

    claim_type = st.selectbox(
        "Select Claim Type",
        list(insurance_data.keys())
    )

    st.info(insurance_data[claim_type]["description"])

    if st.button("Generate Checklist"):

        st.success("Required Documents")

        for document in insurance_data[claim_type]["documents"]:
            st.checkbox(document)

    st.title("📄 Insurance Document Checklist")

    insurance_data = load_checklist()

    claim_type = st.selectbox(
        "Select Claim Type",
        list(insurance_data.keys()),
         key="claim_type_select"
    )


elif st.session_state.page == "Upload":

    st.title("📤 Upload Claim Documents")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        st.image(uploaded_file, width=300)

        save_path = os.path.join("uploads", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Analyze Document"):

            with st.spinner("Analyzing..."):

                result = analyze_document(save_path)

            st.success("Analysis Complete")

            st.write(result)

elif st.session_state.page == "History":
    st.title("📜 Chat History")
    st.write("View previous conversations.")