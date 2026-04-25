import os
from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
from bot_logic import process_chat

load_dotenv()

st.set_page_config(page_title="Voter-Ready Bot", layout="wide", initial_sidebar_state="collapsed")

# --- THE FIXED BOX CSS ---
st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    header, footer { display: none !important; }
    body, html { overflow: auto !important; background: #121212 !important; }
    /* HARDCODED 900px HEIGHT. IT WILL NEVER LOOP. */
    iframe { border: none !important; height: 900px !important; width: 100vw !important; display: block !important; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_processed_prompt" not in st.session_state:
    st.session_state.last_processed_prompt = None

wizard_ui = components.declare_component("wizard_ui", path="frontend")
result = wizard_ui(messages=st.session_state.messages, key="wizard")

if result and isinstance(result, dict):
    if result.get("action") in ["fetch_result", "chat"]:
        prompt = result.get("prompt")
        
        if prompt and st.session_state.last_processed_prompt != prompt:
            st.session_state.last_processed_prompt = prompt
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            history_str = ""
            for m in st.session_state.messages:
                prefix = "User: " if m["role"] == "user" else "Bot: "
                history_str += f"{prefix}{m['content']}\n"
                
            response = process_chat(history_str)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
    elif result.get("action") == "reset":
        if len(st.session_state.messages) > 0:
            st.session_state.messages = []
            st.session_state.last_processed_prompt = None
            st.rerun()