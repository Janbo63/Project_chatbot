# Confidant Project Chatbot

## Overview
A privacy-focused, AI-powered project management and assistant tool designed to help manage the Confidant project with advanced memory and context preservation capabilities.

## Features
- AI-driven project management
- Context-aware conversation tracking
- Secure, local data storage
- Meeting and requirement logging
- Project summary generation

## Prerequisites
- Python 3.8+
- Anthropic API Key

## Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/project-chatbot.git
cd project-chatbot
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
- Create a `.env` file
- Add your Anthropic API key: `ANTHROPIC_API_KEY=your_key_here`

## Running the Application
```bash
uvicorn web_app:app --reload
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
[Specify your license here]

## Contact
[Your contact information]
