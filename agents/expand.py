import os
import requests
from utils.base_agent import BaseAgent

class ExpandAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.endpoint = "http://localhost:11434/api/generate"

    def process(self, message, code="", readme=""):
        # Convert message to string if it's a dict
        message_str = message if isinstance(message, str) else str(message)
        
        data = {
            "model": self.model,
            "prompt": f"""Take the following online content:   {message_str} , and expand upon it. Provide additional context and details to enrich the idea and make it more comprehensive.""",
            "stream": False
        }
        
        try:
            response = requests.post(self.endpoint, json=data).json()
            design_spec = response.get('response', '')
            enhanced_message = f"{message_str}\n\n{design_spec}"
            
            return {
                'message': enhanced_message,

            }
        except Exception as e:
            print(f"Error in ExpandAgent: {str(e)}")
            return {
                'message': message_str,

            }
