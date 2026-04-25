import os
import logging
from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
from bot_logic import process_chat

# Safer Google Cloud Logging Initialization
try:
    from google.cloud import logging as cloud_logging
    client = cloud_logging.Client()
    client.setup_logging()
except ImportError:
    logging.basicConfig(level=logging.INFO)

logging.info("Voter-Ready Bot is starting up...")
load_dotenv()


# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Voter-Ready Bot | AI Assistant", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- THE UNBREAKABLE FIXED BOX CSS ---
st.markdown("""
<style>
    /* Nuke default Streamlit spacing */
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    header, footer { display: none !important; }
    
    /* Global scroll allowed, but background locked */
    body, html { overflow: auto !important; background: #121212 !important; }
    
    /* HARDCODED 900px HEIGHT: Prevents the Infinite Render Loop */
    iframe { 
        border: none !important; 
        height: 900px !important; 
        width: 100vw !important; 
        display: block !important; 
    }
</style>
""", unsafe_allow_html=True)

# Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = []
    logging.info("New Session Started.")

if "last_processed_prompt" not in st.session_state:
    st.session_state.last_processed_prompt = None

# Declare the Custom Component
wizard_ui = components.declare_component("wizard_ui", path="frontend")

# Render the UI and capture interactions
result = wizard_ui(messages=st.session_state.messages, key="wizard")

# --- BI-DIRECTIONAL COMMUNICATION LOGIC ---
if result and isinstance(result, dict):
    action = result.get("action")
    prompt = result.get("prompt")
    
    if action in ["fetch_result", "chat"]:
        # Prevent duplicate processing
        if prompt and st.session_state.last_processed_prompt != prompt:
            logging.info(f"Processing AI Request for action: {action}")
            
            st.session_state.last_processed_prompt = prompt
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Construct history for the Gemini model
            history_str = ""
            for m in st.session_state.messages:
                prefix = "User: " if m["role"] == "user" else "Bot: "
                history_str += f"{prefix}{m['content']}\n"
            
            # Get response from bot_logic.py
            try:
                response = process_chat(history_str)
                st.session_state.messages.append({"role": "assistant", "content": response})
                logging.info("Gemini API Response Received Successfully.")
            except Exception as error:
                logging.error(f"Gemini API Error: {error}")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "I'm having trouble connecting to my brain right now. Please try again."
                })
            
            st.rerun()
            
    elif action == "reset":
        logging.info("User Reset the Wizard.")
        st.session_state.messages = []
        st.session_state.last_processed_prompt = None
        st.rerun()