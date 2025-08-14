from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaLLM
from ..config.model_config import model_config
import json

class RouterNode:
    def __init__(self):
        # Use configured router model
        self.model_name = model_config.get_model("router")
        self.llm = OllamaLLM(model=self.model_name)
        print(f"Router initialized with model: {self.model_name}")
    
    def route_query(self, state):
        """Route query to appropriate expert(s)"""
        query = state["user_message"]
        
        # Enhanced routing logic with LLM-based classification
        routing_prompt = f"""
        Analyze this query and determine which expert(s) should handle it.
        
        Query: {query}
        
        Available experts:
        - finance_expert: For finance, investment, stock market, economics, business questions
        - technical_expert: For programming, technology, software, coding, technical questions
        - general_expert: For general knowledge, creative writing, casual conversation
        
        Respond with a JSON object containing:
        {{
            "route_to": ["list", "of", "expert", "names"],
            "reasoning": "brief explanation of routing decision"
        }}
        
        Only include relevant experts. If unsure, default to general_expert.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=routing_prompt)])
            # Try to parse JSON response
            try:
                routing_data = json.loads(response.content)
                return {
                    "route_to": routing_data.get("route_to", ["general_expert"]),
                    "routing_reason": routing_data.get("reasoning", "Default routing")
                }
            except json.JSONDecodeError:
                # Fallback to simple keyword-based routing
                return self._fallback_routing(query)
        except Exception as e:
            print(f"Routing error: {e}")
            return self._fallback_routing(query)
    
    def _fallback_routing(self, query):
        """Fallback routing based on keywords"""
        query_lower = query.lower()
        
        finance_keywords = ["finance", "stock", "market", "investment", "money", "trading", "economy", "business", "financial"]
        technical_keywords = ["programming", "code", "software", "technology", "python", "javascript", "algorithm", "database", "api"]
        
        experts = []
        
        if any(word in query_lower for word in finance_keywords):
            experts.append("finance_expert")
        
        if any(word in query_lower for word in technical_keywords):
            experts.append("technical_expert")
        
        if not experts:
            experts.append("general_expert")
        
        return {
            "route_to": experts,
            "routing_reason": "Keyword-based fallback routing"
        } 