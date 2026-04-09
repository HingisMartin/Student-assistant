# AiDemy Bootstrap

AiDemy is a demo showcasing multi-tool calling and multi-agent workflows within Google Cloud and using Gemini models. It provides a comprehensive example of building complex AI applications by orchestrating multiple agents and tools to achieve educational goals.

## Project Structure

### Portal (`/portal`)
The main interface for students and educators:
- Course content delivery and management
- Interactive quiz system
- Answer evaluation
- Teaching plan generation and management
- Built with Flask, includes templates for web interface

### Planner (`/planner`)
Intelligent curriculum planning service:
- Curriculum generation and management
- Book recommendation system
- Search functionality for educational content
- AI-powered learning path creation

### Courses (`/courses`)
Course content management system:
- Course material storage
- Curriculum organization
- Learning resource management

### Assignment (`/assignment`)
Assignment handling system:
- Assignment creation and distribution
- Student submission management
- Grading and feedback system

### Book Provider (`/bookprovider`)
Book recommendation and management service:
- Book catalog management
- Reading recommendations
- Integration with curriculum planning

### Setup (`/setup`)
Contains initialization and configuration scripts for the platform.

## Dependencies

Each service manages its own dependencies through individual `requirements.txt` files. Core services are built with:
- Python Flask for web services
- Docker for containerization
- Langchain for agent orchestration
- Google Vertex AI (including Gemini models)
- Deepseek
- Ollama integrations for LLMs

## Architecture

The platform follows a multi-agent architecture where each component (portal, planner, courses, etc.) operates independently but communicates with others to fullfill the use cases
