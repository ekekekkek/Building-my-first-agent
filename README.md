# Multi-LLM Chatbot Agent

A sophisticated chatbot system that orchestrates multiple LLM models using LangGraph for intelligent response synthesis.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Python Backend │    │  LangGraph Core │
│                 │◄──►│                 │◄──►│                 │
│  - Chat UI      │    │  - FastAPI      │    │  - Workflow     │
│  - State Mgmt   │    │  - WebSocket    │    │  - Node Graph   │
│  - Real-time    │    │  - Auth         │    │  - LLM Routing  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                │                       │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Ollama Models │    │  Response       │
                       │                 │    │  Synthesis      │
                       │                 │    │                 │
                       │  Router         │───►│  Aggregator    │
                       │  (mistral:7b)   │    │  (mistral:7b)  │
                       │                 │    │                 │
                       │  Expert A       │    │  - Combine      │
                       │  (finance-llama)│    │  - Refine       │
                       │                 │    │  - Structure    │
                       │  Expert B       │    │                 │
                       │  (llama3.1:8b)  │    │                 │
                       └─────────────────┘    └─────────────────┘
```

## 🔧 Technology Stack

### Frontend
- **React 18** - Modern UI framework with hooks
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **React Query** - Server state management
- **WebSocket** - Real-time communication

### Backend
- **Python 3.11+** - Core backend language
- **FastAPI** - High-performance async web framework
- **Pydantic** - Data validation and serialization
- **WebSocket** - Real-time bidirectional communication
- **SQLAlchemy** - Database ORM (if needed)

### AI/ML Layer
- **LangGraph** - Multi-LLM orchestration and workflow management
- **Ollama** - CPU-optimized local LLM inference
- **Custom Workflows** - Intelligent routing and synthesis

## 🚀 Core Workflow

1. **User Input** → React frontend captures user query
2. **Backend Processing** → Python backend receives and validates request
3. **Router Decision** → mistral:7b analyzes query and routes to appropriate expert(s)
4. **Expert Processing** → Specialized models process query in parallel:
   - **Expert A** (finance-llama-8b): Handles finance fundamentals, sentiment, sector context
   - **Expert B** (llama3.1:8b): Manages mathematical reasoning, coding snippets, explanations
5. **Response Aggregation** → mistral:7b combines expert responses into structured answer
6. **Final Output** → Synthesized, coherent response returned to user

## 🧠 Model Architecture

### Router (mistral:7b)
- **Purpose**: Query classification and routing
- **Function**: Determines if query is "finance-specific" vs "general"
- **Speed**: Fast inference for quick routing decisions
- **Output**: Routing decision to appropriate expert(s)

### Expert A (martain7r/finance-llama-8b)
- **Specialization**: Finance domain expertise
- **Capabilities**: 
  - Financial fundamentals and concepts
  - Market sentiment analysis
  - Sector-specific context and insights
  - Investment terminology and explanations
- **Use Cases**: Stock analysis, market trends, financial planning

### Expert B (llama3.1:8b)
- **Specialization**: General reasoning and technical tasks
- **Capabilities**:
  - Mathematical reasoning and calculations
  - Code generation (especially pandas, data analysis)
  - Logical explanations and step-by-step reasoning
  - General knowledge and problem-solving
- **Use Cases**: Data analysis, coding help, mathematical problems

### Aggregator (mistral:7b)
- **Purpose**: Response synthesis and refinement
- **Function**: Combines expert outputs into coherent, structured answer
- **Capabilities**:
  - Eliminates redundancy and contradictions
  - Ensures logical flow and consistency
  - Formats response for optimal user experience
  - Maintains context and relevance

## 📁 Project Structure

```
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API communication
│   │   ├── types/          # TypeScript definitions
│   │   └── utils/          # Helper functions
│   ├── public/             # Static assets
│   └── package.json        # Dependencies
│
├── backend/                 # Python backend
│   ├── app/
│   │   ├── api/            # FastAPI routes
│   │   ├── core/           # Configuration and settings
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper functions
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # Application entry point
│
├── langgraph/              # LangGraph workflows
│   ├── workflows/          # LLM orchestration flows
│   ├── nodes/             # Individual workflow nodes
│   └── config/            # Model configurations
│
├── docker/                 # Containerization
├── docs/                  # Documentation
└── README.md              # This file
```

## 🎯 Development Phases

### Phase 1: Foundation Setup
- [ ] Project structure initialization
- [ ] Basic React frontend with chat interface
- [ ] FastAPI backend with WebSocket support
- [ ] Ollama installation and model setup
- [ ] Basic LangGraph workflow structure

### Phase 2: Core LLM Integration
- [ ] Implement two specialized LLM models
- [ ] Create LangGraph workflow for model routing
- [ ] Develop response synthesis logic
- [ ] Basic error handling and fallbacks

### Phase 3: Advanced Features
- [ ] Real-time streaming responses
- [ ] Conversation memory and context
- [ ] Model performance monitoring
- [ ] Advanced error handling and retry logic

### Phase 4: Production Ready
- [ ] Authentication and authorization
- [ ] Rate limiting and security
- [ ] Performance optimization
- [ ] Comprehensive testing
- [ ] Deployment configuration

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Ollama installed and running
- Docker (optional)

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd multi-llm-chatbot

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup
cd ../frontend
npm install
npm run dev

# Start Ollama models
ollama run mistral:7b          # Router and Aggregator
ollama run martain7r/finance-llama-8b  # Expert A (Finance)
ollama run llama3.1:8b         # Expert B (General/Technical)
```

## 🔍 Key Features

- **Multi-Model Processing**: Leverage different LLM strengths
- **Real-time Responses**: WebSocket-based live communication
- **Intelligent Synthesis**: Smart combination of multiple responses
- **CPU-Optimized**: Local inference with Ollama
- **Scalable Architecture**: Modular design for easy expansion
- **Type Safety**: Full-stack TypeScript and Python typing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

[Add your license here]

## 🆘 Support

For questions and support, please open an issue in the repository.
