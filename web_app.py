import os
import logging
from typing import List, Dict, Any

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

import anthropic

# Import project management
from project_management import ProjectManager

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

# Initialize project managers for different projects
confidant_project = ProjectManager(
    project_root="F:/Git Hub Projects/Confidant", 
    project_name="Confidant"
)

# Initialize FastAPI and Jinja2 Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Global conversation history with improved management
class ConversationManager:
    def __init__(self, max_history_length=20):
        self.history: List[Dict[str, str]] = []
        self.max_history_length = max_history_length

    def add_message(self, role: str, content: str):
        # Trim history if it exceeds max length
        if len(self.history) >= self.max_history_length:
            self.history.pop(0)
        self.history.append({"role": role, "content": content})

    def get_context_messages(self):
        # Return messages in a format suitable for Claude
        return [
            {"role": msg["role"], "content": msg["content"]} 
            for msg in self.history
        ]

    def reset(self):
        self.history.clear()

# Global conversation manager
conversation_manager = ConversationManager()

class DevAssistant:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        
    def run(self, query):
        try:
            # Retrieve recent project context
            try:
                project_context = confidant_project.get_recent_context()
            except Exception as context_error:
                logger.warning(f"Could not retrieve project context: {context_error}")
                project_context = """Default Project Context:
Confidant is a privacy-focused, locally-run AI agent designed to preserve personal memories 
and provide secure, confidential data storage with robust access control mechanisms."""
            
            # Add user message to conversation history
            conversation_manager.add_message("user", query)

            # Prepare messages with conversation context
            messages = conversation_manager.get_context_messages()

            # Call Claude API with full conversation context and project context
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                system=f"""You are an expert AI assistant helping with the Confidant project.

Project Context:
{project_context}

Your responsibilities:
- Provide clear, concise, and actionable advice
- Use markdown for code formatting
- Help with project development, design, and strategy
- Break down complex topics into easy-to-understand explanations
- Maintain and build upon the project's context and progress
- Offer strategic insights based on the project's current state""",
                messages=messages
            )
            
            # Extract and add AI response to conversation history
            ai_response = response.content[0].text
            conversation_manager.add_message("assistant", ai_response)

            # Log the session (optional, but recommended)
            try:
                confidant_project.log_meeting({
                    'participants': ['User', 'AI Assistant'],
                    'key_discussions': [query],
                    'action_items': [ai_response[:200] + '...']
                })
            except Exception as log_error:
                logger.warning(f"Could not log meeting: {log_error}")

            return ai_response
        
        except Exception as e:
            logger.error(f"Error in agent interaction: {e}")
            return f"An error occurred while processing your request. Please try again. Error details: {str(e)}"

# Initialize assistant
dev_assistant = DevAssistant(ANTHROPIC_API_KEY)

class ProjectAssistant(DevAssistant):
    def __init__(self, api_key, project_manager):
        super().__init__(api_key)
        self.project_manager = project_manager
    
    def generate_system_prompt(self, project_context: str = "") -> str:
        """
        Generate a dynamic system prompt that includes project context and management insights
        
        Args:
            project_context: Recent project context to include in the prompt
        
        Returns:
            Comprehensive system prompt
        """
        return f"""You are an AI Project Management Assistant helping to guide and document a complex software project.

Project Context:
{project_context}

Your responsibilities:
- Provide strategic guidance for project development
- Help document meetings, requirements, and milestones
- Offer insights into project progress and potential challenges
- Use markdown for clear, structured communication
- Break down complex project management tasks
- Suggest best practices for software development
- Maintain a forward-looking perspective on project goals

Communication Guidelines:
- Be concise and actionable
- Highlight potential risks and opportunities
- Provide constructive recommendations
- Ensure all suggestions are aligned with the project's core objectives"""

    def run(self, query: str, project_context: str = "") -> str:
        """
        Enhanced run method that incorporates project management capabilities
        
        Args:
            query: User's input query
            project_context: Optional additional context
        
        Returns:
            AI-generated response
        """
        try:
            # Retrieve recent project context
            recent_summary = self.project_manager.generate_project_summary(days=30)
            
            # Combine recent summary with any additional context
            full_context = f"""Recent Project Summary:
Meetings: {len(recent_summary['meetings'])}
Requirement Changes: {len(recent_summary['requirement_changes'])}
Milestones: {len(recent_summary['milestones'])}

{project_context}"""
            
            # Call Claude API with project context
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                system=self.generate_system_prompt(full_context),
                messages=[{"role": "user", "content": query}]
            )
            
            # Extract AI response
            ai_response = response.content[0].text
            
            # Optionally log the interaction if it seems like a project management task
            self._log_project_interaction(query, ai_response)
            
            return ai_response
        
        except Exception as e:
            logger.error(f"Error in project assistant interaction: {e}")
            return f"An error occurred: {str(e)}"
    
    def _log_project_interaction(self, query: str, response: str):
        """
        Determine if the interaction warrants logging in project management
        
        Args:
            query: User's input query
            response: AI's response
        """
        # Keywords that might indicate a project management interaction
        pm_keywords = [
            'meeting', 'milestone', 'requirement', 'progress', 
            'task', 'action item', 'decision', 'strategy'
        ]
        
        # Check if query contains project management keywords
        if any(keyword in query.lower() for keyword in pm_keywords):
            try:
                self.project_manager.log_meeting({
                    'participants': ['AI Assistant', 'User'],
                    'key_discussions': [query],
                    'action_items': [response],
                    'decisions': ['Recorded AI-assisted project management interaction']
                })
            except Exception as log_error:
                logger.error(f"Could not log project interaction: {log_error}")

# Initialize project assistant
project_assistant = ProjectAssistant(ANTHROPIC_API_KEY, confidant_project)

# Project Management Endpoints
@app.post("/log_meeting")
async def log_meeting(request: Request):
    """Log a project meeting"""
    try:
        meeting_data = await request.json()
        confidant_project.log_meeting(meeting_data)
        return {"status": "success", "message": "Meeting logged successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/log_requirement")
async def log_requirement(request: Request):
    """Log a requirement change"""
    try:
        req_data = await request.json()
        confidant_project.log_requirement_change(req_data)
        return {"status": "success", "message": "Requirement change logged successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/log_milestone")
async def log_milestone(request: Request):
    """Log a project milestone"""
    try:
        milestone_data = await request.json()
        confidant_project.log_milestone(milestone_data)
        return {"status": "success", "message": "Milestone logged successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/project_summary")
async def get_project_summary(days: int = 30):
    """Retrieve project summary"""
    try:
        summary = confidant_project.generate_project_summary(days)
        return summary
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/export_project_report")
async def export_project_report(days: int = 30):
    """Export a comprehensive project report"""
    try:
        report_path = confidant_project.export_project_report(days)
        return {"status": "success", "report_path": report_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main chat interface"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "messages": conversation_manager.history}
    )

@app.post("/")
async def chat_endpoint(request: Request):
    try:
        # Get form data
        form = await request.form()
        query = form.get('query', '')

        if not query:
            return JSONResponse(content={"error": "No query provided"}, status_code=400)

        # Run the AI assistant
        try:
            response = dev_assistant.run(query)
        except Exception as e:
            logger.error(f"Error in AI processing: {e}")
            response = f"An error occurred: {str(e)}"

        # Return response to browser
        return JSONResponse(content={"response": response})

    except Exception as e:
        logger.error(f"Endpoint error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/reset", response_class=HTMLResponse)
async def reset_conversation(request: Request):
    """Reset the conversation history"""
    conversation_manager.reset()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "messages": []}
    )

@app.post("/project_context", response_class=HTMLResponse)
async def get_project_context(request: Request, category: str = Form(None)):
    """Retrieve project context"""
    if category:
        context = confidant_project.get_category_summary(category)
    else:
        # If no category specified, get recent context
        context = confidant_project.get_recent_context()
    
    return context

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
