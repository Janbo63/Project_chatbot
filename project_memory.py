import os
import json
from datetime import datetime
from typing import Dict, List, Any

class ProjectMemory:
    def __init__(self, project_root: str):
        """
        Initialize project memory management system
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.memory_dir = os.path.join(project_root, '.project_memory')
        self.logs_dir = os.path.join(self.memory_dir, 'logs')
        self.summaries_dir = os.path.join(self.memory_dir, 'summaries')
        
        # Create necessary directories
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.summaries_dir, exist_ok=True)

    def log_session(self, category: str, details: Dict[str, Any]):
        """
        Log a session with detailed information
        
        Args:
            category: Category of the session (e.g., 'development', 'design', 'debugging')
            details: Dictionary of session details
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{timestamp}_{category}_log.json"
        log_path = os.path.join(self.logs_dir, log_filename)
        
        details['timestamp'] = timestamp
        details['category'] = category
        
        with open(log_path, 'w') as f:
            json.dump(details, f, indent=4)
        
        # Update category summary
        self.update_category_summary(category, details)

    def update_category_summary(self, category: str, session_details: Dict[str, Any]):
        """
        Update or create a summary for a specific category
        
        Args:
            category: Category to update
            session_details: Details of the latest session
        """
        summary_path = os.path.join(self.summaries_dir, f"{category}_summary.json")
        
        # Read existing summary or create new
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                summary = json.load(f)
        else:
            summary = {
                'category': category,
                'sessions': [],
                'key_milestones': [],
                'challenges': [],
                'todo': []
            }
        
        # Add new session to summary
        summary['sessions'].append({
            'timestamp': session_details.get('timestamp', datetime.now().strftime("%Y%m%d_%H%M%S")),
            'highlights': session_details.get('highlights', []),
            'progress': session_details.get('progress', 'No specific progress noted')
        })
        
        # Optional: Extract and update milestones, challenges, todo
        if 'milestones' in session_details:
            summary['key_milestones'].extend(session_details['milestones'])
        if 'challenges' in session_details:
            summary['challenges'].extend(session_details['challenges'])
        if 'todo' in session_details:
            summary['todo'].extend(session_details['todo'])
        
        # Write updated summary
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=4)

    def get_category_summary(self, category: str) -> Dict[str, Any]:
        """
        Retrieve summary for a specific category
        
        Args:
            category: Category to retrieve summary for
        
        Returns:
            Summary of the category or empty dict if not found
        """
        summary_path = os.path.join(self.summaries_dir, f"{category}_summary.json")
        
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                return json.load(f)
        return {}

    def get_recent_context(self, category: str = None, num_sessions: int = 3) -> str:
        """
        Generate a context string from recent sessions
        
        Args:
            category: Optional category to filter sessions
            num_sessions: Number of recent sessions to include
        
        Returns:
            Formatted context string
        """
        if category:
            summary = self.get_category_summary(category)
        else:
            # If no category, try to get summaries from all categories
            summary = {}
            for filename in os.listdir(self.summaries_dir):
                if filename.endswith('_summary.json'):
                    with open(os.path.join(self.summaries_dir, filename), 'r') as f:
                        category_summary = json.load(f)
                        summary.setdefault('sessions', []).extend(category_summary.get('sessions', []))
        
        # Sort sessions by timestamp and take recent ones
        recent_sessions = sorted(
            summary.get('sessions', []), 
            key=lambda x: x.get('timestamp', ''), 
            reverse=True
        )[:num_sessions]
        
        context = "Recent Project Context:\n"
        for session in recent_sessions:
            context += f"- {session.get('timestamp')}: {session.get('progress', 'No details')}\n"
        
        return context

# Example usage
if __name__ == "__main__":
    # Initialize for a specific project
    project_memory = ProjectMemory(r"f:/Git Hub Projects/Project_chatbot")
    
    # Log a development session
    project_memory.log_session('development', {
        'highlights': ['Implemented web interface', 'Added conversation memory'],
        'progress': 'Enhanced Claude AI assistant with context tracking',
        'challenges': ['Managing conversation history'],
        'todo': ['Implement persistent project memory']
    })
    
    # Retrieve context
    print(project_memory.get_recent_context('development'))
