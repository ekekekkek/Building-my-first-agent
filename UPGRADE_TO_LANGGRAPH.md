# 🚀 Upgrading MVP to LangGraph Multi-Model System

This guide shows you how to evolve your simple streaming MVP into a sophisticated multi-model orchestration system using LangGraph.

## 🔄 Evolution Path

```
MVP (Current)                    →    LangGraph System
┌─────────────┐                        ┌─────────────┐
│ Single Model│                        │Multi-Models│
│ Streaming   │                        │Orchestration│
└─────────────┘                        └─────────────┘
```

## 📦 Step 1: Add LangGraph Dependencies

```bash
# Install LangGraph and related packages
pip install langgraph langchain-ollama langchain-core

# Update requirements.txt
echo "langgraph==0.0.20" >> requirements.txt
echo "langchain-ollama==0.1.0" >> requirements.txt
echo "langchain-core==0.1.0" >> requirements.txt
```

## 🏗️ Step 2: Create LangGraph Workflow Structure

### 2.1 Create Workflow Directory
```bash
mkdir -p langgraph/workflows
mkdir -p langgraph/nodes
mkdir -p langgraph/config
```

### 2.2 Define Workflow Nodes

Create `langgraph/nodes/router.py`:
```python
from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaLLM

class RouterNode:
    def __init__(self):
        self.llm = OllamaLLM(model="mistral:7b")
    
    def route_query(self, state):
        """Route query to appropriate expert(s)"""
        query = state["user_message"]
        
        # Simple routing logic (can be enhanced)
        if any(word in query.lower() for word in ["finance", "stock", "market", "investment"]):
            return {"route_to": ["finance_expert", "general_expert"]}
        else:
            return {"route_to": ["general_expert"]}
```

Create `langgraph/nodes/experts.py`:
```python
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage

class FinanceExpert:
    def __init__(self):
        self.llm = OllamaLLM(model="martain7r/finance-llama-8b")
    
    def process(self, state):
        """Process finance-related queries"""
        query = state["user_message"]
        response = self.llm.invoke([HumanMessage(content=query)])
        return {"finance_response": response.content}

class GeneralExpert:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.1:8b")
    
    def process(self, state):
        """Process general queries"""
        query = state["user_message"]
        response = self.llm.invoke([HumanMessage(content=query)])
        return {"general_response": response.content}
```

Create `langgraph/nodes/aggregator.py`:
```python
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage

class AggregatorNode:
    def __init__(self):
        self.llm = OllamaLLM(model="mistral:7b")
    
    def synthesize(self, state):
        """Combine expert responses into coherent answer"""
        finance_response = state.get("finance_response", "")
        general_response = state.get("general_response", "")
        
        if finance_response and general_response:
            prompt = f"""
            Combine these expert responses into a coherent answer:
            
            Finance Expert: {finance_response}
            General Expert: {general_response}
            
            Original Question: {state['user_message']}
            
            Provide a well-structured, comprehensive response that synthesizes both perspectives.
            """
        else:
            prompt = f"Provide a comprehensive answer to: {state['user_message']}"
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {"final_response": response.content}
```

### 2.3 Create Main Workflow

Create `langgraph/workflows/main_workflow.py`:
```python
from langgraph.graph import StateGraph, END
from langgraph.nodes import add_messages
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage

# State definition
class AgentState(TypedDict):
    user_message: str
    route_to: list
    finance_response: str
    general_response: str
    final_response: str
    messages: Annotated[list, add_messages]

def create_workflow():
    """Create the main workflow graph"""
    
    # Import nodes
    from ..nodes.router import RouterNode
    from ..nodes.experts import FinanceExpert, GeneralExpert
    from ..nodes.aggregator import AggregatorNode
    
    router = RouterNode()
    finance_expert = FinanceExpert()
    general_expert = GeneralExpert()
    aggregator = AggregatorNode()
    
    # Create workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router.route_query)
    workflow.add_node("finance_expert", finance_expert.process)
    workflow.add_node("general_expert", general_expert.process)
    workflow.add_node("aggregator", aggregator.synthesize)
    
    # Define edges
    workflow.add_edge("router", "finance_expert")
    workflow.add_edge("router", "general_expert")
    workflow.add_edge("finance_expert", "aggregator")
    workflow.add_edge("general_expert", "aggregator")
    workflow.add_edge("aggregator", END)
    
    # Compile workflow
    return workflow.compile()

# Usage
workflow = create_workflow()
```

## 🔄 Step 3: Update Backend to Use LangGraph

Modify `backend/main.py` to integrate LangGraph:

```python
# Add imports
from langgraph.workflows.main_workflow import workflow
from langgraph.prebuilt import ToolNode

# Update WebSocket endpoint
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            # Send acknowledgment
            await manager.send_personal_message(
                json.dumps({
                    "type": "status",
                    "content": "Processing with multi-model system...",
                    "timestamp": asyncio.get_event_loop().time()
                }),
                websocket
            )
            
            # Run LangGraph workflow
            try:
                # Initialize state
                initial_state = {
                    "user_message": user_message,
                    "messages": [HumanMessage(content=user_message)]
                }
                
                # Execute workflow
                result = await workflow.ainvoke(initial_state)
                
                # Stream the final response
                final_response = result["final_response"]
                words = final_response.split()
                
                for word in words:
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "chunk",
                            "content": word + " ",
                            "timestamp": asyncio.get_event_loop().time()
                        }),
                        websocket
                    )
                    await asyncio.sleep(0.05)  # Slower streaming for readability
                
                # Send completion
                await manager.send_personal_message(
                    json.dumps({
                        "type": "complete",
                        "content": final_response,
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
                
            except Exception as e:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "content": f"Workflow error: {str(e)}",
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

## 🎯 Step 4: Enhanced Features

### 4.1 Add Model Management
```python
# backend/models/model_manager.py
class ModelManager:
    def __init__(self):
        self.models = {
            "router": "mistral:7b",
            "finance": "martain7r/finance-llama-8b",
            "general": "llama3.1:8b",
            "aggregator": "mistral:7b"
        }
    
    def get_model(self, model_type):
        return self.models.get(model_type, "mistral:7b")
    
    def update_model(self, model_type, model_name):
        self.models[model_type] = model_name
```

### 4.2 Add Performance Monitoring
```python
# backend/monitoring/performance.py
import time
from typing import Dict

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, operation: str):
        self.metrics[operation] = {"start": time.time()}
    
    def end_timer(self, operation: str):
        if operation in self.metrics:
            self.metrics[operation]["duration"] = time.time() - self.metrics[operation]["start"]
    
    def get_metrics(self) -> Dict:
        return self.metrics
```

### 4.3 Add Error Handling and Fallbacks
```python
# backend/error_handling/fallbacks.py
class FallbackHandler:
    def __init__(self):
        self.fallback_model = "mistral:7b"
    
    async def handle_fallback(self, error: Exception, query: str):
        """Handle errors by falling back to single model"""
        # Log error
        print(f"Error in workflow: {error}")
        
        # Fallback to simple streaming
        return await stream_ollama_response(query, self.fallback_model)
```

## 🚀 Step 5: Production Enhancements

### 5.1 Add Authentication
```python
# backend/auth/jwt_handler.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 5.2 Add Rate Limiting
```python
# backend/middleware/rate_limiter.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.websocket("/ws/chat")
@limiter.limit("10/minute")
async def websocket_endpoint(websocket: WebSocket):
    # ... existing code
```

### 5.3 Add Caching
```python
# backend/cache/redis_cache.py
import redis
import json

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    def get_cached_response(self, query_hash: str):
        return self.redis_client.get(query_hash)
    
    def cache_response(self, query_hash: str, response: str, ttl: int = 3600):
        self.redis_client.setex(query_hash, ttl, response)
```

## 📊 Step 6: Monitoring and Observability

### 6.1 Add Logging
```python
# backend/logging/logger.py
import logging
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
```

### 6.2 Add Metrics Collection
```python
# backend/metrics/prometheus.py
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter('ai_agent_requests_total', 'Total requests')
RESPONSE_TIME = Histogram('ai_agent_response_time_seconds', 'Response time')
MODEL_USAGE = Counter('ai_agent_model_usage_total', 'Model usage by type')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 🎉 Benefits of the Upgrade

1. **Intelligent Routing**: Automatically route queries to appropriate experts
2. **Parallel Processing**: Multiple models work simultaneously
3. **Response Synthesis**: Intelligent combination of expert responses
4. **Scalability**: Easy to add new models and experts
5. **Monitoring**: Full visibility into workflow performance
6. **Fallbacks**: Graceful degradation when models fail
7. **Production Ready**: Authentication, rate limiting, caching

## 🔧 Testing the Upgrade

```bash
# Test the new system
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the best investment strategies for 2024?"}'

# Check metrics
curl http://localhost:8000/metrics

# Monitor logs
tail -f logs/app_*.log
```

---

**Congratulations!** You've successfully evolved your MVP into a production-ready, multi-model AI orchestration system! 🚀

The system now intelligently routes queries, processes them with specialized models, and synthesizes comprehensive responses - all while maintaining the real-time streaming experience your users love. 