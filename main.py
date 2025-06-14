import streamlit as st
import os
from dotenv import load_dotenv
from alfred_persona import AlfredPersona
from chat_interface import ChatInterface
from openai_client import OpenAIClient

# Load environment variables
load_dotenv()

def main():
    # Page configuration
    st.set_page_config(
        page_title="Alfred - Your Personal Assistant",
        page_icon="🎩",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for chat interface
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .alfred-message {
        background-color: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 20%;
        text-align: left;
    }
    
    .input-container {
        position: sticky;
        bottom: 0;
        background-color: white;
        padding: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add Alfred's greeting
        alfred = AlfredPersona()
        greeting = alfred.get_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    
    if 'openai_client' not in st.session_state:
        st.session_state.openai_client = OpenAIClient()
    
    # Header
    st.markdown("<h1 class='main-header'>🎩 Alfred - Your Personal Assistant</h1>", unsafe_allow_html=True)
    
    # Chat interface
    chat_interface = ChatInterface()
    
    # Display chat messages
    chat_interface.display_messages(st.session_state.messages)
    
    # User input
    user_input = st.chat_input("What can I help you with today, Master Bruce?")
    
    if user_input:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get Alfred's response
        with st.spinner("Alfred is thinking..."):
            response = st.session_state.openai_client.get_alfred_response(
                st.session_state.messages, 
                user_input
            )
        
        # Add Alfred's response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to display new messages
        st.rerun()
    
    # Sidebar with controls
    with st.sidebar:
        st.markdown("### 🏰 Wayne Manor Controls")
        
        if st.button("🔄 Clear Conversation"):
            st.session_state.messages = []
            alfred = AlfredPersona()
            greeting = alfred.get_greeting()
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Session Info")
        st.write(f"Messages in conversation: {len(st.session_state.messages)}")
        
        st.markdown("---")
        st.markdown("### ℹ️ About Alfred")
        st.write("Your loyal digital butler, ready to assist you with wit, wisdom, and unwavering dedication.")

if __name__ == "__main__":
    main()