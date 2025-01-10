# Project Management System

## Overview
This project management system provides a comprehensive solution for tracking project progress, logging meetings, requirements, and milestones.

## Features
- 📅 Meeting Logging
- 📋 Requirement Tracking
- 🏁 Milestone Management
- 📊 Project Summary Generation
- 📁 Report Export

## Endpoints

### 1. Log a Meeting
**Endpoint**: `/log_meeting`
**Method**: POST
**Payload Example**:
```json
{
    "participants": ["Project Lead", "Developer"],
    "key_discussions": ["Project Architecture"],
    "action_items": ["Finalize design"],
    "decisions": ["Use local encryption"],
    "next_steps": ["Create technical specification"]
}
```

### 2. Log Requirement Change
**Endpoint**: `/log_requirement`
**Method**: POST
**Payload Example**:
```json
{
    "category": "Technical Requirements",
    "changes": ["Added offline functionality"],
    "rationale": "Ensure data privacy",
    "impact": ["Increased local processing"],
    "proposed_by": "Security Team"
}
```

### 3. Log Milestone
**Endpoint**: `/log_milestone`
**Method**: POST
**Payload Example**:
```json
{
    "name": "Architecture Design",
    "description": "Complete system design",
    "status": "Completed",
    "completion_date": "2025-01-10",
    "key_achievements": ["Defined memory storage", "Security mechanisms"]
}
```

### 4. Get Project Summary
**Endpoint**: `/project_summary`
**Method**: GET
**Query Parameter**: 
- `days` (optional, default: 30): Number of days to include in summary

### 5. Export Project Report
**Endpoint**: `/export_project_report`
**Method**: GET
**Query Parameter**:
- `days` (optional, default: 30): Number of days to include in report

## Usage Examples

### Python Requests
```python
import requests

# Log a meeting
requests.post('http://localhost:8000/log_meeting', json={
    'participants': ['You', 'Team Lead'],
    'key_discussions': ['Memory storage architecture']
})

# Get project summary
summary = requests.get('http://localhost:8000/project_summary').json()
print(summary)
```

### Command Line Demo
Run the interactive demo:
```bash
python project_management_demo.py
```

## Project Storage
- Meetings stored in: `.project_management/meetings/`
- Requirements stored in: `.project_management/requirements/`
- Milestones stored in: `.project_management/logs/`
- Reports exported to: `.project_management/reports/`

## Best Practices
1. Log meetings immediately after they occur
2. Update requirements as they evolve
3. Mark milestones when significant progress is made
4. Regularly review project summaries

## Security
- All project data is stored locally
- JSON format for easy human and machine readability
- Unique identifiers for each log entry
