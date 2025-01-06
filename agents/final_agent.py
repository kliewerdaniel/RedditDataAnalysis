import os
import requests
from utils.base_agent import BaseAgent

class FinalAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.endpoint = "http://localhost:11434/api/generate"

    def process(self, prompt):
        message = prompt.get('message', '')
        message_str = message if isinstance(message, str) else str(message)
        data = {
            "model": self.model,
            "prompt": f"""Based on the following post: {message_str} , Ensure that the final blog post is professional and expand on the points further. """,
            "stream": False
        }
        
        try:
            response = requests.post(self.endpoint, json=data).json()
            result = response.get('response', '')
            enhanced_message = f"{message_str}\n\n{result}"
            
            return {
                'message': enhanced_message,
            }
        except Exception as e:
            print(f"Error in FinalAgent: {str(e)}")
            return {
                'message': message_str,
            }
