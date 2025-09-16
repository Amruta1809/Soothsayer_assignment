import streamlit as st
from document_parser import parse_pdf, parse_excel, extract_financial_metrics
from qa_engine import simple_lookup, answer_with_model

st.set_page_config(page_title="Financial Q&A Assistant", layout="wide")

st.title("📊 Financial Document Q&A Assistant")

# Session state
if "context" not in st.session_state:
    st.session_state["context"] = ""
if "metrics" not in st.session_state:
    st.session_state["metrics"] = {}

uploaded_file = st.file_uploader("Upload Financial Document (PDF/Excel)", type=["pdf", "xlsx", "xls"])

if uploaded_file:
    with st.spinner("Processing document..."):
        if uploaded_file.type == "application/pdf":
            text, tables = parse_pdf(uploaded_file)
            st.session_state["context"] = text
        else:
            dfs = parse_excel(uploaded_file)
            text = "\n".join([df.to_string() for df in dfs.values()])
            st.session_state["context"] = text

        # Extract metrics
        st.session_state["metrics"] = extract_financial_metrics(st.session_state["context"], [])

    st.success("✅ Document processed successfully!")

# Chat section
if st.session_state["context"]:
    st.subheader("💬 Ask Questions")

    user_question = st.chat_input("Ask about revenue, profit, expenses...")
    if user_question:
        st.chat_message("user").write(user_question)

        # Try simple lookup first
        answer = simple_lookup(user_question, st.session_state["metrics"])
        if not answer:
            answer = answer_with_model(user_question, st.session_state["context"])

        st.chat_message("assistant").write(answer)
