import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
import logging

logger = logging.getLogger(__name__)

class ProjectManager:
    def __init__(self, project_root: str, project_name: str):
        """
        Initialize comprehensive project management system
        
        Args:
            project_root: Root directory to store project management files
            project_name: Name of the project being managed
        """
        self.project_root = project_root
        self.project_name = project_name
        
        # Create project management directories
        self.base_dir = os.path.join(project_root, '.project_management')
        self.logs_dir = os.path.join(self.base_dir, 'logs')
        self.reports_dir = os.path.join(self.base_dir, 'reports')
        self.requirements_dir = os.path.join(self.base_dir, 'requirements')
        self.meetings_dir = os.path.join(self.base_dir, 'meetings')
        
        # Create necessary directories
        for dir_path in [self.base_dir, self.logs_dir, self.reports_dir, 
                         self.requirements_dir, self.meetings_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # Initialize project metadata
        self.project_metadata_path = os.path.join(self.base_dir, 'project_metadata.json')
        self._initialize_project_metadata()
        
        # Initialize project context
        self.initialize_project_context()

    def _initialize_project_metadata(self):
        """
        Initialize or load project metadata
        """
        if not os.path.exists(self.project_metadata_path):
            initial_metadata = {
                'project_name': self.project_name,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'status': 'Active',
                'milestones': [],
                'key_objectives': []
            }
            with open(self.project_metadata_path, 'w') as f:
                json.dump(initial_metadata, f, indent=4)

    def log_meeting(self, details: Dict[str, Any]):
        """
        Log a project meeting
        
        Args:
            details: Dictionary containing meeting details
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        meeting_id = f"meeting_{timestamp}_{uuid.uuid4().hex[:8]}"
        
        # Ensure required fields
        meeting_log = {
            'id': meeting_id,
            'timestamp': timestamp,
            'date': datetime.now().isoformat(),
            'participants': details.get('participants', []),
            'key_discussions': details.get('key_discussions', []),
            'action_items': details.get('action_items', []),
            'decisions': details.get('decisions', []),
            'next_steps': details.get('next_steps', [])
        }
        
        # Save meeting log
        meeting_file_path = os.path.join(self.meetings_dir, f"{meeting_id}.json")
        with open(meeting_file_path, 'w') as f:
            json.dump(meeting_log, f, indent=4)
        
        # Update project metadata
        self._update_project_metadata('meetings', meeting_id)

    def log_requirement_change(self, details: Dict[str, Any]):
        """
        Log changes to project requirements
        
        Args:
            details: Dictionary containing requirement change details
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        req_change_id = f"requirement_{timestamp}_{uuid.uuid4().hex[:8]}"
        
        requirement_log = {
            'id': req_change_id,
            'timestamp': timestamp,
            'date': datetime.now().isoformat(),
            'category': details.get('category', 'General'),
            'changes': details.get('changes', []),
            'rationale': details.get('rationale', ''),
            'impact': details.get('impact', []),
            'proposed_by': details.get('proposed_by', 'Unknown')
        }
        
        # Save requirement change log
        req_file_path = os.path.join(self.requirements_dir, f"{req_change_id}.json")
        with open(req_file_path, 'w') as f:
            json.dump(requirement_log, f, indent=4)
        
        # Update project metadata
        self._update_project_metadata('requirements', req_change_id)

    def log_milestone(self, details: Dict[str, Any]):
        """
        Log a project milestone
        
        Args:
            details: Dictionary containing milestone details
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        milestone_id = f"milestone_{timestamp}_{uuid.uuid4().hex[:8]}"
        
        milestone_log = {
            'id': milestone_id,
            'timestamp': timestamp,
            'date': datetime.now().isoformat(),
            'name': details.get('name', 'Unnamed Milestone'),
            'description': details.get('description', ''),
            'status': details.get('status', 'Pending'),
            'completion_date': details.get('completion_date'),
            'key_achievements': details.get('key_achievements', [])
        }
        
        # Save milestone log
        milestone_file_path = os.path.join(self.logs_dir, f"{milestone_id}.json")
        with open(milestone_file_path, 'w') as f:
            json.dump(milestone_log, f, indent=4)
        
        # Update project metadata
        self._update_project_metadata('milestones', milestone_id)

    def _update_project_metadata(self, section: str, new_item: str):
        """
        Update project metadata with new item
        
        Args:
            section: Metadata section to update
            new_item: New item to add to the section
        """
        with open(self.project_metadata_path, 'r+') as f:
            metadata = json.load(f)
            
            # Ensure the section exists
            if section not in metadata:
                metadata[section] = []
            
            # Add new item and update last updated time
            metadata[section].append(new_item)
            metadata['last_updated'] = datetime.now().isoformat()
            
            # Move file pointer to start and write updated metadata
            f.seek(0)
            json.dump(metadata, f, indent=4)
            f.truncate()

    def generate_project_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate a summary of project activities in the last specified days
        
        Args:
            days: Number of days to include in the summary
        
        Returns:
            Dictionary containing project summary
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        summary = {
            'project_name': self.project_name,
            'summary_period': f'Last {days} days',
            'meetings': [],
            'requirement_changes': [],
            'milestones': []
        }
        
        # Collect meetings
        for filename in os.listdir(self.meetings_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.meetings_dir, filename), 'r') as f:
                    meeting = json.load(f)
                    meeting_date = datetime.fromisoformat(meeting['date'])
                    if meeting_date > cutoff_date:
                        summary['meetings'].append(meeting)
        
        # Collect requirement changes
        for filename in os.listdir(self.requirements_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.requirements_dir, filename), 'r') as f:
                    req_change = json.load(f)
                    req_date = datetime.fromisoformat(req_change['date'])
                    if req_date > cutoff_date:
                        summary['requirement_changes'].append(req_change)
        
        # Collect milestones
        for filename in os.listdir(self.logs_dir):
            if filename.startswith('milestone_') and filename.endswith('.json'):
                with open(os.path.join(self.logs_dir, filename), 'r') as f:
                    milestone = json.load(f)
                    milestone_date = datetime.fromisoformat(milestone['date'])
                    if milestone_date > cutoff_date:
                        summary['milestones'].append(milestone)
        
        return summary

    def export_project_report(self, days: int = 30):
        """
        Export a comprehensive project report
        
        Args:
            days: Number of days to include in the report
        """
        summary = self.generate_project_summary(days)
        
        # Create reports directory if not exists
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Generate report filename
        report_filename = f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(self.reports_dir, report_filename)
        
        # Write report
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=4)
        
        return report_path

    def get_recent_context(self, category: str = None, days: int = 30) -> str:
        """
        Generate a recent context summary for the project
        
        Args:
            category: Optional category to filter context
            days: Number of days to include in context
        
        Returns:
            Formatted context string
        """
        try:
            # Generate project summary
            summary = self.generate_project_summary(days)
            
            # Format context string
            context = f"Recent Project Context (Last {days} days):\n\n"
            
            # Add meetings
            context += "Meetings:\n"
            for meeting in summary.get('meetings', []):
                context += f"- {meeting.get('date', 'Unknown Date')}: {', '.join(meeting.get('key_discussions', []))}\n"
            
            # Add requirement changes
            context += "\nRequirement Changes:\n"
            for req_change in summary.get('requirement_changes', []):
                context += f"- {req_change.get('date', 'Unknown Date')}: {', '.join(req_change.get('changes', []))}\n"
            
            # Add milestones
            context += "\nMilestones:\n"
            for milestone in summary.get('milestones', []):
                context += f"- {milestone.get('name', 'Unnamed Milestone')}: {milestone.get('status', 'No status')}\n"
            
            return context
        
        except Exception as e:
            logger.error(f"Error generating recent context: {e}")
            return f"Unable to generate project context. Error: {e}"

    def get_category_summary(self, category: str) -> Dict[str, Any]:
        """
        Retrieve summary for a specific category
        
        Args:
            category: Category to retrieve summary for
        
        Returns:
            Summary of the category or empty dict if not found
        """
        # Implement a basic category summary retrieval
        try:
            summary = self.generate_project_summary()
            
            # Filter summary based on category
            filtered_summary = {
                'meetings': [
                    meeting for meeting in summary.get('meetings', [])
                    if category.lower() in str(meeting).lower()
                ],
                'requirement_changes': [
                    req for req in summary.get('requirement_changes', [])
                    if category.lower() in str(req).lower()
                ],
                'milestones': [
                    milestone for milestone in summary.get('milestones', [])
                    if category.lower() in str(milestone).lower()
                ]
            }
            
            return filtered_summary
        except Exception as e:
            logger.error(f"Error retrieving category summary: {e}")
            return {}

    def initialize_project_context(self):
        """
        Pre-populate initial project context if no existing logs are found
        """
        try:
            # Check if any logs exist
            meetings_dir = os.path.join(self.meetings_dir)
            requirements_dir = os.path.join(self.requirements_dir)
            milestones_dir = os.path.join(self.logs_dir)

            # If no logs exist, create initial context
            if (not os.listdir(meetings_dir) and 
                not os.listdir(requirements_dir) and 
                not os.listdir(milestones_dir)):
                
                # Log initial project meeting
                self.log_meeting({
                    'participants': ['Project Lead', 'AI Assistant'],
                    'key_discussions': [
                        'Confidant Project Memory Storage Architecture', 
                        'Privacy and Security Mechanisms'
                    ],
                    'action_items': [
                        'Design local encryption strategy',
                        'Create security access control specification'
                    ],
                    'decisions': [
                        'Use end-to-end local encryption',
                        'Implement multi-tier access control'
                    ]
                })

                # Log initial requirement
                self.log_requirement_change({
                    'category': 'Technical Requirements',
                    'changes': [
                        'Added offline functionality specification',
                        'Enhanced local data privacy requirements'
                    ],
                    'rationale': 'Ensure complete user data protection and system independence',
                    'impact': [
                        'Requires additional local processing capabilities',
                        'Increases system security'
                    ]
                })

                # Log initial milestone
                self.log_milestone({
                    'name': 'Initial Architecture Design',
                    'description': 'Complete high-level system design for Confidant project',
                    'status': 'Completed',
                    'key_achievements': [
                        'Defined memory storage approach',
                        'Outlined security mechanisms',
                        'Created initial system architecture concept'
                    ]
                })

        except Exception as e:
            logger.error(f"Error initializing project context: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize for Confidant project
    project_manager = ProjectManager(
        project_root="F:/Git Hub Projects/Confidant", 
        project_name="Confidant"
    )
    
    # Log a meeting
    project_manager.log_meeting({
        'participants': ['Project Lead', 'Developer'],
        'key_discussions': ['Memory storage architecture', 'Privacy requirements'],
        'action_items': [
            'Finalize encryption strategy',
            'Draft security access control document'
        ],
        'decisions': ['Use local encryption for all stored memories']
    })
    
    # Log a requirement change
    project_manager.log_requirement_change({
        'category': 'Technical Requirements',
        'changes': ['Added offline functionality specification'],
        'rationale': 'Ensure complete local data privacy',
        'impact': ['Requires additional local processing capabilities']
    })
    
    # Log a milestone
    project_manager.log_milestone({
        'name': 'Initial Architecture Design',
        'description': 'Complete high-level system design',
        'status': 'Completed',
        'key_achievements': [
            'Defined memory storage approach',
            'Outlined security mechanisms'
        ]
    })
    
    # Generate and export project report
    report_path = project_manager.export_project_report()
    print(f"Project report generated: {report_path}")
