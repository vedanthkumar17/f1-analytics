import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    url = os.environ.get("DATABASE_URL")
    if not url and hasattr(st, "secrets") and "DATABASE_URL" in st.secrets:
        url = st.secrets["DATABASE_URL"]
    if not url:
        raise ValueError("DATABASE_URL is not set in environment variables or Streamlit secrets.")
    return url
