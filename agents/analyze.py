import os
import requests
from utils.base_agent import BaseAgent

class AnalyzeAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.endpoint = "http://localhost:11434/api/generate"

    def process(self, message, code="", readme=""):
        # Convert message to string if it's a dict
        message_str = message if isinstance(message, str) else str(message)
        
        data = {
            "model": self.model,
            "prompt": f"""Using the following expanded analysis: {message_str} , Take those ideas and synthesize it and write a blog post from them as the output.""",
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
            print(f"Error in AnalyzeAgent: {str(e)}")
            return {
                'message': message_str,

            }
