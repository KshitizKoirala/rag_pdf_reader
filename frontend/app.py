import os

import requests
import streamlit as st

API_HOST = os.getenv("BACKEND_HOST", "app")
API_URL = f"http://{API_HOST}:8000/api/pdf"

st.title("📄 PDF Q&A (powered by FastAPI + Qdrant)")
API_KEY = st.text_input("Enter API KEY", type="password")

if not API_KEY:
    st.warning("🔐 Please enter your API KEY to continue.")
    st.stop()

st.markdown("---")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    st.info("Uploading...")
    res = requests.post(
        f"{API_URL}/upload/",
        headers={"x-api-key": API_KEY},
        files={"file": uploaded_file.read()}
    )
    st.success(res.json()["status"])

st.markdown("---")

question = st.text_input("Ask a question about the uploaded PDF:")

if st.button("Submit Question") and question:
    res = requests.get(
        f"{API_URL}/ask/",
        headers={"x-api-key": API_KEY},
        params={"question": question}
    )
    response = res.json()
    st.subheader("Answer")
    for ans in response:
        st.write(ans)
