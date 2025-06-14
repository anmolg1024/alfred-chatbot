import streamlit as st
from datetime import datetime

class ChatInterface:
    """Handles the chat interface and message display"""
    
    def __init__(self):
        self.user_avatar = "👤"
        self.alfred_avatar = "🎩"
    
    def display_messages(self, messages):
        """Display all messages in the chat interface"""
        
        # Create a container for messages
        chat_container = st.container()
        
        with chat_container:
            for i, message in enumerate(messages):
                if message["role"] == "user":
                    self._display_user_message(message["content"])
                elif message["role"] == "assistant":
                    self._display_alfred_message(message["content"])
    
    def _display_user_message(self, content):
        """Display a user message with proper styling"""
        col1, col2 = st.columns([1, 4])
        
        with col2:
            with st.chat_message("user", avatar=self.user_avatar):
                st.markdown(f"**Master Bruce:** {content}")
    
    def _display_alfred_message(self, content):
        """Display Alfred's message with proper styling"""
        col1, col2 = st.columns([4, 1])
        
        with col1:
            with st.chat_message("assistant", avatar=self.alfred_avatar):
                st.markdown(f"**Alfred:** {content}")
    
    def get_message_count(self, messages):
        """Get count of messages by type"""
        user_messages = len([msg for msg in messages if msg["role"] == "user"])
        alfred_messages = len([msg for msg in messages if msg["role"] == "assistant"])
        return user_messages, alfred_messages
    
    def format_timestamp(self):
        """Get formatted timestamp for messages"""
        return datetime.now().strftime("%H:%M")
    
    def create_message_bubble(self, content, is_user=False):
        """Create a styled message bubble"""
        if is_user:
            bubble_class = "user-message"
            sender = "Master Bruce"
        else:
            bubble_class = "alfred-message"
            sender = "Alfred"
        
        return f"""
        <div class="{bubble_class}">
            <strong>{sender}:</strong> {content}
        </div>
        """
    
    def display_typing_indicator(self):
        """Show typing indicator while Alfred is responding"""
        with st.empty():
            st.markdown("*Alfred is typing...*")
    
    def clear_chat_display(self):
        """Clear the chat display"""
        st.empty()
    
    def export_conversation(self, messages):
        """Export conversation to text format"""
        conversation_text = "=== Conversation with Alfred ===\n\n"
        
        for message in messages:
            if message["role"] == "user":
                conversation_text += f"Master Bruce: {message['content']}\n\n"
            elif message["role"] == "assistant":
                conversation_text += f"Alfred: {message['content']}\n\n"
        
        conversation_text += f"=== End of Conversation ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ==="
        
        return conversation_text