  # AI Agent Instructions

## Project Overview

This repository contains a Computer Use Agent (CUA) implementation that enables automated computer interactions through browser or VM environments. The proje### Development & Deployment Guide

### 1. Environment Configuration

1. Environment Configuration

   ```bash
   # Frontend (.env)
   VITE_API_URL=http://localhost:8000  # Backend API address
   VITE_SANDBOX_URL=http://localhost:8001  # Sandbox service URL

   # Backend (.env)
   MONGODB_URI=mongodb://localhost:27017/ai-agent  # Database URL
   REDIS_URL=redis://localhost:6379  # Cache and pubsub
   OPENAI_API_KEY=your_key_here  # AI service auth
   SANDBOX_URL=http://localhost:8001  # Sandbox service
   PORT=8000  # API port
   NODE_ENV=development  # Environment name
   LOG_LEVEL=debug  # Logging verbosity

   # Sandbox (.env)
   CHROME_PORT=9222  # DevTools debugging
   VNC_PORT=5900  # Remote access
   MAX_PROCESSES=10  # Process limit
   TIMEOUT_MINUTES=60  # Session timeout
   DOCKER_HOST=unix:///var/run/docker.sock  # Docker socket
   SANDBOX_ROOT=/sandbox  # Container root
   ```

   ```bash
   # Production overrides
   NODE_ENV=production
   LOG_LEVEL=info
   MONGODB_URI=${RAILWAY_MONGO_URL}
   REDIS_URL=${RAILWAY_REDIS_URL}
   ```

2. Production (Railway)
   ```bash
   # Deploy with Railway CLI
   railway up --service frontend
   railway up --service backend
   railway up --service sandbox
   ```

### 2. Inter-Service Communication

1. Service Architecture
   ```
   Frontend <-> Backend <-> Sandbox
       |         |          |
       |         v          v
       +---> MongoDB    Docker API
             Redis
   ```

2. Communication Patterns
   - Frontend → Backend: REST API + SSE
   - Backend → Sandbox: REST API
   - Sandbox → Container: Docker API
   - Real-time Updates: Redis pubsub

### 3. Common Issues & Solutions

1. Connection Issues
   ```
   Issue: Backend can't connect to MongoDB/Redis
   Fix: Check MONGODB_URI and REDIS_URL in .env
   ```

   ```
   Issue: Sandbox container not starting
   Fix: Check Docker daemon and port conflicts
   ```

   ```
   Issue: VNC connection refused
   Fix: Verify ports 5900/9222 not in use
   ```

2. Performance Issues
   ```
   Issue: Slow API responses
   Fix: Enable Redis caching, check MongoDB indexes
   ```

   ```
   Issue: High memory usage in sandbox
   Fix: Adjust MAX_PROCESSES in sandbox config
   ```

3. Security Issues
   ```
   Issue: Exposed API endpoints
   Fix: Enable authentication, use API keys
   ```

   ```
   Issue: Container escape concerns
   Fix: Review Docker security settings
   ```

### 4. Development Workflow

1. Adding New Features
   - Define in domain layer
   - Implement interfaces
   - Add API endpoints
   - Update frontend components

2. Testing
   - Unit tests per component
   - Integration tests for APIs
   - E2E tests for critical flows
   - Security scans

3. Deployment

#### Railway Deployment

1. Monorepo Configuration
   ```bash
   # Project structure setup
   frontend/               # Root directory for frontend service
   ├── package.json
   ├── vite.config.js
   └── src/
   
   backend/                # Root directory for backend service
   ├── app/
   └── main.py
   
   sandbox/                # Root directory for sandbox service
   ├── Dockerfile
   └── app/
   ```

2. Service Setup
   ```bash
   # Frontend service settings
   ROOT_DIRECTORY=/frontend
   VITE_BACKEND_HOST=${{Backend.RAILWAY_PUBLIC_DOMAIN}}
   
   # Backend service settings
   ROOT_DIRECTORY=/backend
   ALLOWED_ORIGINS=${{Frontend.RAILWAY_PUBLIC_DOMAIN}}
   
   # Sandbox service settings
   ROOT_DIRECTORY=/sandbox
   ```

3. Build Configuration
   ```json
   // railway.json
   {
     "builder": "RAILPACK",
     "buildCommand": "npm run build",
     "startCommand": "npm start",
     "rootDirectory": "./frontend",
     "watchPatterns": [
       "/frontend/**/*.{js,ts,vue}",
       "/backend/**/*.py",
       "/sandbox/**/*"
     ]
   }
   ```

4. Deployment States
   - **Initializing**: Initial state when deployment starts
   - **Building**: Creating Docker image
   - **Deploying**: Launching container
   - **Active**: Successfully running
   - **Failed**: Build/deploy error
   - **Crashed**: Runtime failure
   - **Removed**: Deployment cleaned up

5. Resource Management
   - 10GB ephemeral storage per deployment
   - Configurable overlap period (`RAILWAY_DEPLOYMENT_OVERLAP_SECONDS`)
   - Graceful shutdown window (`RAILWAY_DEPLOYMENT_DRAINING_SECONDS`)
   - Auto-scaling based on load

6. Railway API Integration

   ```bash
   # GraphQL API endpoint
   https://backboard.railway.com/graphql/v2
   
   # Authentication (Choose one)
   Authorization: Bearer <API_TOKEN>     # Personal/Team token
   Project-Access-Token: <PROJECT_TOKEN> # Project-specific token
   
   # Rate Limits
   Free: 100 RPH
   Hobby: 1000 RPH, 10 RPS
   Pro: 10000 RPH, 50 RPS
   ```

7. Template Management
   ```bash
   # Deploy template
   railway template deploy <template-name>
   
   # Create template
   railway template create
   
   # Publish template
   railway template publish
   ```

8. MCP Server Integration
   ```json
   // .vscode/mcp.json
   {
     "servers": {
       "Railway": {
         "type": "stdio",
         "command": "npx",
         "args": ["-y", "@railway/mcp-server"]
       }
     }
   }
   ```

   Available MCP Tools:
   - Project Management (create, list)
   - Service Management (deploy, link)
   - Environment Management (create, link)
   - Configuration & Variables
   - Monitoring & Logs

9. Environment Management
   ```bash
   # Development environment
   railway link --project $PROJECT_ID
   railway environment new development
   
   # PR environments
   railway environment new pr-$PR_NUMBER --copy production
   
   # Production deployment
   railway up --service all
   ``` on secure, sandboxed automation of UI interactions with robust safety controls.

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