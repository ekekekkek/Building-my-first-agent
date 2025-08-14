#!/bin/bash

# 🚀 Enhanced MVP Startup Script - Multi-Model System
# This script starts the enhanced MVP with multi-model orchestration

echo "🚀 Starting Enhanced MVP - Multi-Model System"
echo "=============================================="

# Check if Ollama is running
echo "🔍 Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    echo ""
    echo "Then pull the required models:"
    echo "   ollama pull mistral:7b"
    echo "   ollama pull llama3.1:8b"
    echo "   ollama pull martain7r/finance-llama-8b"
    exit 1
fi

echo "✅ Ollama is running"

# Check if required models are available
echo "🔍 Checking available models..."
available_models=$(ollama list | grep -E "(mistral:7b|llama3.1:8b|finance-llama)" || echo "")

if [[ -z "$available_models" ]]; then
    echo "⚠️  No specialized models found. Using default models."
    echo "   To enhance performance, consider pulling specialized models:"
    echo "   ollama pull llama3.1:8b"
    echo "   ollama pull martain7r/finance-llama-8b"
else
    echo "✅ Available models:"
    echo "$available_models"
fi

# Check Python dependencies
echo "🔍 Checking Python dependencies..."
if ! python3 -c "import langchain_ollama, langchain_core" 2>/dev/null; then
    echo "❌ Missing dependencies. Installing..."
    pip3 install -r requirements.txt
fi

echo "✅ Dependencies are ready"

# Test the multi-model system
echo "🧪 Testing multi-model system..."
if python3 test_multi_model.py > /dev/null 2>&1; then
    echo "✅ Multi-model system test passed"
else
    echo "❌ Multi-model system test failed. Check the logs above."
    exit 1
fi

# Start the backend
echo "🚀 Starting Enhanced MVP Backend..."
echo "   Multi-Model System: ✅ Active"
echo "   Intelligent Routing: ✅ Active"
echo "   Expert Aggregation: ✅ Active"
echo "   Fallback System: ✅ Active"
echo ""
echo "🌐 Backend will be available at: http://localhost:8000"
echo "📡 WebSocket endpoint: ws://localhost:8000/ws/chat"
echo "📊 Health check: http://localhost:8000/health"
echo ""
echo "💡 Try asking questions like:"
echo "   - 'What are the best investment strategies for 2024?'"
echo "   - 'How do I implement a binary search tree in Python?'"
echo "   - 'Tell me a joke about programming'"
echo ""
echo "🔄 The system will automatically route to appropriate experts and synthesize responses!"
echo ""

cd backend
python3 main.py 