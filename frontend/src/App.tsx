import React, { useState, useEffect, useRef } from 'react'
import './App.css'

interface Message {
  id: string
  content: string
  isUser: boolean
  timestamp: Date
  isStreaming?: boolean
}

interface WebSocketMessage {
  type: 'status' | 'chunk' | 'complete' | 'error'
  content: string
  timestamp: number
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws/chat')
      
      ws.onopen = () => {
        setIsConnected(true)
        console.log('WebSocket connected')
      }

      ws.onmessage = (event) => {
        try {
          const data: WebSocketMessage = JSON.parse(event.data)
          
          switch (data.type) {
            case 'status':
              setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: data.content,
                isUser: false,
                timestamp: new Date(data.timestamp * 1000),
                isStreaming: true
              }])
              break
              
            case 'chunk':
              setMessages(prev => {
                const lastMessage = prev[prev.length - 1]
                if (lastMessage && lastMessage.isStreaming) {
                  return prev.map((msg, index) => 
                    index === prev.length - 1 
                      ? { ...msg, content: msg.content + data.content }
                      : msg
                  )
                }
                return prev
              })
              break
              
            case 'complete':
              setMessages(prev => prev.map((msg, index) => 
                index === prev.length - 1 
                  ? { ...msg, isStreaming: false }
                  : msg
              ))
              setIsProcessing(false)
              break
              
            case 'error':
              setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content: `Error: ${data.content}`,
                isUser: false,
                timestamp: new Date(data.timestamp * 1000)
              }])
              setIsProcessing(false)
              break
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      ws.onclose = () => {
        setIsConnected(false)
        console.log('WebSocket disconnected')
        // Reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000)
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      }

      wsRef.current = ws
    }

    connectWebSocket()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const sendMessage = () => {
    if (!inputValue.trim() || !isConnected || isProcessing) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isUser: true,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsProcessing(true)

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        message: inputValue
      }))
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 AI Agent MVP</h1>
        <div className="connection-status">
          <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
          {isConnected ? 'Connected' : 'Disconnected'}
        </div>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h3>Welcome to AI Agent MVP!</h3>
              <p>This is a simple streaming chat interface that connects to a single Ollama model.</p>
              <p>Ask me anything and watch the response stream in real-time!</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.isUser ? 'user' : 'assistant'}`}
              >
                <div className="message-content">
                  {message.content}
                  {message.isStreaming && <span className="streaming-indicator">▋</span>}
                </div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            disabled={!isConnected || isProcessing}
            rows={3}
          />
          <button
            onClick={sendMessage}
            disabled={!inputValue.trim() || !isConnected || isProcessing}
            className="send-button"
          >
            {isProcessing ? 'Processing...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default App 