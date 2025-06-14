
import os
import openai
import streamlit as st
from alfred_persona import AlfredPersona

class OpenAIClient:
    """Handles all OpenAI API interactions"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            st.error("❌ OpenAI API key not found! Please check your .env file.")
            st.stop()
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"
        self.alfred_persona = AlfredPersona()
    
    def get_alfred_response(self, conversation_history, user_message):
        """
        Get a response from Alfred using OpenAI API
        
        Args:
            conversation_history: List of previous messages
            user_message: Current user input
            
        Returns:
            Alfred's response as a string
        """
        try:
            # Prepare messages for API call
            messages = [
                {"role": "system", "content": self.alfred_persona.get_system_prompt()}
            ]
            
            # Add conversation history (excluding the system message and initial greeting)
            for msg in conversation_history:
                if msg["role"] in ["user", "assistant"] and not self._is_greeting(msg["content"]):
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except openai.APIError as e:
            return f"I do apologize, Master Bruce, but I'm experiencing some technical difficulties. The error appears to be: {str(e)}"
        except openai.RateLimitError:
            return "Master Bruce, it seems we've reached our conversation limit for the moment. Perhaps we might continue our discussion shortly?"
        except openai.AuthenticationError:
            return "I'm afraid there seems to be an authentication issue, Master Bruce. You may need to check the API credentials."
        except Exception as e:
            return f"Most peculiar, Master Bruce. I've encountered an unexpected issue: {str(e)}"
    
    def _is_greeting(self, content):
        """Check if the message is likely a greeting"""
        greeting_indicators = [
            "Good day, Master Bruce",
            "Master Bruce, I trust you are well",
            "At your service, Master Bruce",
            "Good to see you, Master Bruce"
        ]
        return any(indicator in content for indicator in greeting_indicators)
    
    def test_connection(self):
        """Test the OpenAI API connection"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=10
            )
            return True, "Connection successful"
        except Exception as e:
            return False, str(e)