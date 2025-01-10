import requests
import json

# Base URL for the project management API
BASE_URL = "http://localhost:8000"

def log_meeting():
    """Demonstrate logging a project meeting"""
    meeting_data = {
        'participants': ['Project Lead', 'AI Assistant', 'Developer'],
        'key_discussions': [
            'Confidant Project Memory Storage Architecture',
            'Privacy and Security Mechanisms'
        ],
        'action_items': [
            'Finalize local encryption strategy',
            'Design access control mechanism',
            'Create detailed security requirements document'
        ],
        'decisions': [
            'Use end-to-end local encryption',
            'Implement multi-tier access control'
        ],
        'next_steps': [
            'Draft technical specification',
            'Create proof-of-concept encryption module'
        ]
    }
    
    response = requests.post(f"{BASE_URL}/log_meeting", json=meeting_data)
    print("Meeting Logging Response:")
    print(json.dumps(response.json(), indent=2))

def log_requirement_change():
    """Demonstrate logging a requirement change"""
    requirement_data = {
        'category': 'Technical Requirements',
        'changes': [
            'Added offline functionality specification',
            'Enhanced local data privacy requirements'
        ],
        'rationale': 'Ensure complete user data protection and system independence',
        'impact': [
            'Requires additional local processing capabilities',
            'Increases system complexity',
            'Improves overall security posture'
        ],
        'proposed_by': 'Project Security Team'
    }
    
    response = requests.post(f"{BASE_URL}/log_requirement", json=requirement_data)
    print("\nRequirement Change Logging Response:")
    print(json.dumps(response.json(), indent=2))

def log_milestone():
    """Demonstrate logging a project milestone"""
    milestone_data = {
        'name': 'Initial Architecture Design',
        'description': 'Complete high-level system design for Confidant project',
        'status': 'Completed',
        'completion_date': '2025-01-10',
        'key_achievements': [
            'Defined memory storage approach',
            'Outlined security mechanisms',
            'Created initial system architecture diagram',
            'Identified key technological components'
        ]
    }
    
    response = requests.post(f"{BASE_URL}/log_milestone", json=milestone_data)
    print("\nMilestone Logging Response:")
    print(json.dumps(response.json(), indent=2))

def get_project_summary():
    """Retrieve and display project summary"""
    response = requests.get(f"{BASE_URL}/project_summary")
    print("\nProject Summary:")
    print(json.dumps(response.json(), indent=2))

def export_project_report():
    """Export a comprehensive project report"""
    response = requests.get(f"{BASE_URL}/export_project_report")
    print("\nProject Report Export:")
    print(json.dumps(response.json(), indent=2))

def interactive_project_management_demo():
    """Interactive demonstration of project management features"""
    print("🚀 Confidant Project Management Demo 🚀")
    
    # Simulate project management workflow
    input("Press Enter to log a project meeting...")
    log_meeting()
    
    input("\nPress Enter to log a requirement change...")
    log_requirement_change()
    
    input("\nPress Enter to log a project milestone...")
    log_milestone()
    
    input("\nPress Enter to retrieve project summary...")
    get_project_summary()
    
    input("\nPress Enter to export project report...")
    export_project_report()
    
    print("\n🎉 Project Management Demo Complete! 🎉")

if __name__ == "__main__":
    interactive_project_management_demo()
