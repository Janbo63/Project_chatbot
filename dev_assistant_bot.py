from phi.assistant import Assistant
from phi.llm.anthropic import Claude
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Anthropic API Key from environment
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Create a memory-enabled development assistant
dev_assistant = Assistant(
    name="DevAssistant",
    llm=Claude(
        model="claude-3-opus-20240229",  # Latest Anthropic model
        api_key=ANTHROPIC_API_KEY
    ),
    description="An AI assistant specialized in helping with development tasks, tracking project context, and providing coding assistance."
)

def main():
    # Check if API key is set
    if not ANTHROPIC_API_KEY:
        print("Error: Anthropic API Key is not set. Please add it to the .env file.")
        return

    # Example of interacting with the assistant
    print("DevAssistant is ready. Type 'exit' or 'quit' to end the conversation.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # Process the input and get response
            response = dev_assistant.run(user_input)
            print("Assistant:", response)
        except KeyboardInterrupt:
            print("\nAssistant stopped. Type 'exit' to quit.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
