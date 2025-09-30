 # AI Agent Instructions

## Project Overview

This repository contains a Computer Use Agent (CUA) implementation that enables automated computer interactions through browser or VM environments. The proje### Developer Guide

1. Adding New Tools
   - Define interface in `domain/external`
   - Implement in infrastructure layer
   - Integrate in `application/services`
   - Add API routes in `interfaces/api`

2. Debugging
   - Browser: Chrome DevTools at `localhost:9222`
   - VNC: Connect to `localhost:5900`
   - API: Use SSE for real-time monitoring
   - Logs: Check supervisor and service logs

3. Environment Requirements
   - Python 3.9+
   - Docker 20.10+
   - MongoDB 4.4+
   - Redis 6.0+
   - Node.js 20.18.0

4. Error Handling
   - Use unified response format
   - Handle common error codes (400, 404, 500)
   - Implement proper validation
   - Add error monitoring

5. Testing
   - Run in headless mode for CI
   - Use safety check suite
   - Test SSE streams
   - Validate sandbox isolation on secure, sandboxed automation of UI interactions with robust safety controls.

## Key Components

### 1. Environment Options

- **Browser Automation**: Uses Playwright for web interactions
- **Virtual Machine**: Uses Docker + Xfce for full system control

### 2. Project Structure

This project consists of three independent sub-projects:

```
├── Frontend (Vue 3 + TypeScript)
│   ├── src/
│   │   ├── assets/          # Static resources and CSS
│   │   ├── components/      # Reusable Vue components
│   │   │   ├── ChatInput.vue    # Chat input handling
│   │   │   ├── ChatMessage.vue  # Message display
│   │   │   ├── Sidebar.vue      # Navigation sidebar
│   │   │   ├── ToolPanel.vue    # Tool controls
│   │   │   └── ui/             # Shared UI components
│   │   ├── pages/           # Page components
│   │   │   ├── ChatPage.vue    # Main chat interface
│   │   │   └── HomePage.vue    # Landing page
│   │   ├── App.vue         # Root component
│   │   └── main.ts        # Entry point
│
├── Backend (DDD Architecture)
│   ├── app/                # Main application directory
│   │   ├── domain/          # Domain layer
│   │   │   ├── models/      # Domain models
│   │   │   ├── services/    # Domain services
│   │   │   ├── external/    # External interfaces
│   │   │   └── prompts/     # Prompt templates
│   │   ├── application/     # Application layer
│   │   │   ├── services/    # App services
│   │   │   └── schemas/     # Data schemas
│   │   ├── interfaces/      # Interface layer
│   │   │   └── api/        # API routes
│   │   │       └── v1/     # API version v1
│   │   ├── infrastructure/ # Infrastructure layer
│   │   └── main.py        # Entry point
│
└── Sandbox (Automation Environment)
    ├── app/               # Sandbox service
    │   ├── api/           # API interfaces
    │   │   └── v1/        # API version v1
    │   │       ├── shell.py      # Command execution
    │   │       ├── file.py       # File operations
    │   │       └── supervisor.py  # Process management
    │   ├── services/     # Service implementations
    │   ├── schemas/      # FastAPI models
    │   └── main.py      # Entry point
    ├── Browser Implementation
    │   ├── Playwright setup
    │   └── Action handlers
    └── VM Implementation
        ├── Docker container (Ubuntu + Xfce)
        └── X11 automation (xdotool)
```

### 3. Core Features & API Endpoints

1. Session Management (`/api/v1/sessions`)
   - Create/Get/List/Delete sessions
   - Real-time conversation via SSE
   - Session state management
   - Conversation history tracking

2. Command Execution (`/api/v1/shell/*`)
   - Execute shell commands
   - View session output
   - Process control (wait/kill)
   - Input handling
   - Session-based history

3. File Operations (`/api/v1/file/*`)
   - Read/write files
   - Search content (regex)
   - Replace strings
   - Find files by pattern
   - Path security validation

4. Process Management (`/api/v1/supervisor/*`)
   - Service status monitoring
   - Start/Stop/Restart services
   - Timeout management
   - Health checks

5. Browser Environment
   - Chrome DevTools Protocol
   - Remote debugging (port 9222)
   - Playwright automation
   - Screenshot capture

6. VNC Access
   - WebSocket-based remote desktop
   - Secure connection handling
   - Real-time visualization
   - Port 5900 access

7. Conversation Features
   - Streaming responses (SSE)
   - Tool invocations
   - Plan execution
   - Error handling
   - Progress tracking

## Development Workflows

### Frontend Development

1. Configure Environment:
   ```bash
   # .env file
   VITE_API_URL=http://127.0.0.1:8000  # Backend API address
   ```

2. Install and Run:
   ```bash
   # Install dependencies
   npm install

   # Development mode
   npm run dev

   # Production build
   npm run build
   ```

3. Docker Deployment:
   ```bash
   # Build image
   docker build -t ai-chatbot-vue .

   # Run container
   docker run -d -p 8080:80 ai-chatbot-vue
   ```

### Component Patterns

1. Chat Components
   - `ChatInput.vue`: Handles user input and command processing
   - `ChatMessage.vue`: Displays AI and user messages with proper formatting
   - `ToolPanel.vue`: Manages available tool integrations

2. State Management
   - Use Vue 3 Composition API for complex state
   - Implement proper error boundaries
   - Handle async operations with loading states

### Project Setup

1. Frontend (Vue.js):
   ```bash
   cd frontend
   npm install
   # Development
   npm run dev
   # Production
   npm run build
   ```

2. Backend (FastAPI):
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m app.main
   ```

3. Sandbox:
   ```bash
   cd sandbox
   # Build container
   docker build -t sandbox-env .
   # Run with ports for VNC (5900) and DevTools (9222)
   docker run --rm -it -p 5900:5900 -p 9222:9222 sandbox-env
   ```

## Project Conventions

### Security First
- ALL automation MUST run in sandboxed environments
- NO direct system access from automation code
- ALWAYS use empty environment variables
- MANDATORY security checks before executing actions

### Action Handling Pattern
When implementing new actions:
1. Add handler to appropriate environment class
2. Include safety validation
3. Ensure screenshot capture after action
4. Add error handling with retries

## Integration Points

1. OpenAI API Integration
   - Uses computer-use-preview model
   - Requires proper API authentication
   - Handles safety check responses

2. Environment Communication
   - Browser: Direct Playwright API calls
   - VM: Docker exec commands through `dockerExec` helper

## Common Pitfalls

1. Screenshot Handling
   - Always verify screenshot capture success
   - Handle potential timing issues
   - Consider viewport limitations

2. Safety Checks
   - Never bypass pending safety checks
   - Always implement all required validations
   - Monitor for malicious instructions

## Developer Tools

1. Debugging
   - Browser: Use Playwright Inspector
   - VM: VNC viewer for visual debugging (port 5900)

2. Testing
   - Run in headless mode for CI
   - Use safety check test suite
   - Validate environment isolation

## Secure Credential Management

### API Key Handling
1. Local Development
   - Store API keys in `.env` file (never commit to repo)
   - Use environment variables for all credentials
   ```bash
   # .env example
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=...
   ```

2. Production Environment
   - Use secret management service (e.g., Docker secrets, Kubernetes secrets)
   - Rotate credentials regularly
   - Use separate API keys for different environments

3. CI/CD Pipeline
   - Store secrets in secure CI variables
   - Never log or expose credentials in build outputs
   - Use temporary credentials when possible

### API Client Integration

1. Google API Client
   ```python
   # Bad - Never hardcode credentials
   api_key = "AIzaXXX..."  # ❌
   
   # Good - Load from environment
   import os
   from dotenv import load_dotenv
   
   load_dotenv()  # Load .env file
   api_key = os.getenv("GOOGLE_API_KEY")  # ✅
   
   if not api_key:
       raise ValueError("Missing GOOGLE_API_KEY environment variable")
   ```

2. OpenAI Client
   ```python
   # Good - Use environment variables
   from openai import OpenAI
   
   client = OpenAI()  # Automatically loads from OPENAI_API_KEY env var
   ```

### Security Best Practices

1. Access Control
   - Use principle of least privilege
   - Create separate API keys for different services
   - Implement API key scoping when available

2. Monitoring & Auditing
   - Log API key usage (but never the keys themselves)
   - Monitor for unusual activity
   - Set up alerts for credential misuse

3. Key Rotation
   - Rotate credentials on schedule
   - Immediate rotation if exposure suspected
   - Use key rotation automation when possible


   ## System Capabilities

   - **General-Purpose AI Agent**: Supports running a wide range of tools and operations in isolated sandboxes.
   - **Deployment**: Minimal deployment requires only an LLM service (no external dependencies). Supports Docker-based and (planned) K8s/Swarm multi-cluster deployments.
   - **Tools**: Terminal, Browser, File, Web Search, and messaging tools with real-time viewing and user takeover. External MCP tool integration supported.
   - **Sandboxing**: Each task runs in a separate local Docker sandbox for security and isolation.
   - **Task Sessions**: Session history managed via MongoDB/Redis, supporting background and interruptible tasks.
   - **Conversations**: File upload/download, session stop/interrupt, and persistent chat history.
   - **Multilingual**: Full support for both Chinese and English.
   - **Authentication**: User login and authentication required for access.

   ## Development Roadmap

   - **Tools**: Add support for Deploy & Expose operations.
   - **Sandbox**: Extend sandbox access to mobile and Windows computers.
   - **Deployment**: Add support for Kubernetes and Docker Swarm multi-cluster deployments.