from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from typing import Dict, List
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Agent MVP", version="0.1.0")

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
    """Stream response from Ollama model"""
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
    return {"message": "AI Agent MVP - Backend Running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": DEFAULT_MODEL}

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
                    "content": "Processing your request...",
                    "timestamp": asyncio.get_event_loop().time()
                }),
                websocket
            )
            
            # Stream response from Ollama
            full_response = ""
            async for chunk in stream_ollama_response(user_message):
                full_response += chunk
                # Send chunk to client
                await manager.send_personal_message(
                    json.dumps({
                        "type": "chunk",
                        "content": chunk,
                        "timestamp": asyncio.get_event_loop().time()
                    }),
                    websocket
                )
                # Small delay to make streaming visible
                await asyncio.sleep(0.01)
            
            # Send completion signal
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