import os
import logging
from dotenv import load_dotenv
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Retrieve Anthropic API key
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    logger.error("ANTHROPIC_API_KEY not found in .env file")
    raise ValueError("ANTHROPIC_API_KEY must be set in .env file")

class DevAssistant:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = """You are an expert AI software development assistant.
- Provide clear, concise, and actionable advice.
- Use markdown for code formatting.
- Help with coding, debugging, and software design.
- Break down complex topics into easy-to-understand explanations."""

    def run(self, query):
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error in agent interaction: {e}")
            raise

def main():
    try:
        # Create development assistant
        dev_assistant = DevAssistant(ANTHROPIC_API_KEY)
        
        # Direct interaction with the agent
        print("Anthropic Claude Agent Interaction Demo")
        print("------------------------------")
        
        # Example query
        query = "Explain the concept of dependency injection in Python"
        print(f"\nQuery: {query}\n")
        
        # Run the query through the agent
        response = dev_assistant.run(query)
        
        print("Agent Response:")
        print("-" * 20)
        print(response)
    
    except Exception as e:
        logger.error(f"Agent interaction failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
