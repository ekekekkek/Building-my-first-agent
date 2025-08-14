# AI Agent MVP - Getting Started

This is a minimal, runnable scaffold for your AI agent that streams responses from a single Ollama model. It's designed to be easily upgraded to use LangGraph for multi-model orchestration later.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama installed and running

### 2. Install Ollama Models
```bash
# Install the default model (mistral:7b)
ollama pull mistral:7b

# Or use any other model you prefer
ollama pull llama3.1:8b
```

### 3. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
cd backend
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the development server
npm run dev
```

### 5. Test the System
- Open http://localhost:3000 in your browser
- You should see the chat interface
- Type a message and watch it stream in real-time!

## 🏗️ Current Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Python Backend │    │   Ollama Model  │
│                 │◄──►│                 │◄──►│                 │
│  - Chat UI      │    │  - FastAPI      │    │  - mistral:7b   │
│  - WebSocket    │    │  - WebSocket    │    │  - Streaming    │
│  - Real-time    │    │  - Streaming    │    │  - Local        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Configuration

Copy `env.example` to `.env` and customize:

```bash
cp env.example .env
```

Key settings:
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)
- `DEFAULT_MODEL`: Model to use (default: mistral:7b)
- `BACKEND_PORT`: Backend server port (default: 8000)

## 📁 Project Structure

```
├── backend/
│   └── main.py              # FastAPI app with WebSocket streaming
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main chat component
│   │   ├── App.css          # Chat interface styles
│   │   └── main.tsx         # React entry point
│   ├── package.json         # Frontend dependencies
│   └── vite.config.ts       # Vite configuration
├── requirements.txt          # Python dependencies
├── env.example              # Environment configuration
└── MVP_README.md            # This file
```

## 🎯 Features

- **Real-time Streaming**: Watch responses appear word-by-word
- **WebSocket Communication**: Low-latency bidirectional chat
- **Responsive UI**: Modern chat interface with mobile support
- **Connection Status**: Visual indicator of backend connectivity
- **Auto-reconnect**: Automatically reconnects if connection drops

## 🔄 Next Steps: LangGraph Integration

Once you're comfortable with the MVP, you can upgrade to the full multi-model system:

1. **Add LangGraph Dependencies**
   ```bash
   pip install langgraph langchain-ollama
   ```

2. **Create Workflow Nodes**
   - Router node for query classification
   - Expert nodes for specialized processing
   - Aggregator node for response synthesis

3. **Implement Fan-out Pattern**
   - Route queries to appropriate experts
   - Process in parallel
   - Combine results intelligently

4. **Add Model Management**
   - Multiple Ollama models
   - Model selection logic
   - Fallback strategies

## 🐛 Troubleshooting

### Backend Issues
- Check if Ollama is running: `ollama list`
- Verify model is installed: `ollama run mistral:7b "Hello"`
- Check backend logs for errors

### Frontend Issues
- Ensure backend is running on port 8000
- Check browser console for WebSocket errors
- Verify CORS settings if using different ports

### Ollama Issues
- Restart Ollama service: `ollama serve`
- Check model availability: `ollama list`
- Verify API endpoint: `curl http://localhost:11434/api/tags`

## 🚀 Production Considerations

- Add authentication and rate limiting
- Implement proper error handling and logging
- Use environment variables for all configuration
- Add health checks and monitoring
- Consider using Redis for WebSocket state management
- Implement proper CORS policies

---

**Happy coding!** This MVP gives you a solid foundation to build upon. 🎉 