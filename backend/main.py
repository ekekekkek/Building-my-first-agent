from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from typing import Dict, List
import httpx
import os
from dotenv import load_dotenv

# Import simplified multi-model system
from simple_multi_model import run_multi_model_query

load_dotenv()

app = FastAPI(title="AI Agent MVP - Multi-Model Enhanced", version="0.2.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

# Ollama API configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistral:7b")

async def stream_ollama_response(prompt: str, model: str = DEFAULT_MODEL):
    """Stream response from Ollama model (fallback)"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            },
            timeout=60.0
        )
        
        async for line in response.aiter_lines():
            if line.strip():
                try:
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue

@app.get("/")
async def root():
    return {"message": "AI Agent MVP - Multi-Model Enhanced Backend Running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": DEFAULT_MODEL, "system": "multi-model"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
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
            
            # Run multi-model system
            try:
                # Execute multi-model processing
                result = await run_multi_model_query(user_message)
                
                # Stream the final response
                final_response = result.get("final_response", "No response generated")
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
                
                # Send completion signal
                await manager.send_personal_message(
                    json.dumps({
                        "type": "complete",
                        "content": final_response,
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
                
            except Exception as e:
                print(f"Multi-model system error: {e}")
                # Fallback to simple streaming
                await manager.send_personal_message(
                    json.dumps({
                        "type": "status",
                        "content": "Falling back to single model...",
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
                
                # Fallback streaming
                full_response = ""
                async for chunk in stream_ollama_response(user_message):
                    full_response += chunk
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "chunk",
                            "content": chunk,
                            "timestamp": asyncio.get_event_loop().time()
                        }),
                        websocket
                    )
                    await asyncio.sleep(0.01)
                
                # Send completion
                await manager.send_personal_message(
                    json.dumps({
                        "type": "complete",
                        "content": full_response,
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_personal_message(
            json.dumps({
                "type": "error",
                "content": f"Error: {str(e)}",
                "timestamp": asyncio.get_event_loop().time()
            }),
            websocket
        )
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 