"""
Simplified Multi-Model System
This demonstrates the multi-model concept without complex LangGraph dependencies
"""

import asyncio
import json
from typing import Dict, List
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage
import os

class SimpleMultiModelSystem:
    """Simplified multi-model system for demonstration"""
    
    def __init__(self):
        # Model configuration
        self.models = {
            "router": os.getenv("ROUTER_MODEL", "mistral:7b"),
            "finance": os.getenv("FINANCE_MODEL", "mistral:7b"),
            "technical": os.getenv("TECHNICAL_MODEL", "mistral:7b"),
            "general": os.getenv("GENERAL_MODEL", "mistral:7b"),
            "aggregator": os.getenv("AGGREGATOR_MODEL", "mistral:7b")
        }
        
        # Initialize LLMs
        self.router_llm = OllamaLLM(model=self.models["router"])
        self.finance_llm = OllamaLLM(model=self.models["finance"])
        self.technical_llm = OllamaLLM(model=self.models["technical"])
        self.general_llm = OllamaLLM(model=self.models["general"])
        self.aggregator_llm = OllamaLLM(model=self.models["aggregator"])
        
        print("🚀 Simple Multi-Model System Initialized")
        print(f"Router: {self.models['router']}")
        print(f"Finance: {self.models['finance']}")
        print(f"Technical: {self.models['technical']}")
        print(f"General: {self.models['general']}")
        print(f"Aggregator: {self.models['aggregator']}")
    
    def _extract_response_content(self, response) -> str:
        """Extract content from langchain response object"""
        try:
            # Try different response formats
            if hasattr(response, 'content'):
                return response.content
            elif hasattr(response, 'text'):
                return response.text
            elif isinstance(response, str):
                return response
            elif hasattr(response, 'message') and hasattr(response.message, 'content'):
                return response.message.content
            else:
                # Fallback: convert to string
                return str(response)
        except Exception as e:
            print(f"Error extracting response content: {e}")
            return str(response)
    
    async def route_query(self, query: str) -> Dict:
        """Route query to appropriate expert(s)"""
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
            response = self.router_llm.invoke([HumanMessage(content=routing_prompt)])
            response_content = self._extract_response_content(response)
            try:
                routing_data = json.loads(response_content)
                return {
                    "route_to": routing_data.get("route_to", ["general_expert"]),
                    "routing_reason": routing_data.get("reasoning", "Default routing")
                }
            except json.JSONDecodeError:
                return self._fallback_routing(query)
        except Exception as e:
            print(f"Routing error: {e}")
            return self._fallback_routing(query)
    
    def _fallback_routing(self, query: str) -> Dict:
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
    
    async def process_with_expert(self, query: str, expert_type: str) -> str:
        """Process query with a specific expert"""
        if expert_type == "finance_expert":
            prompt = f"""
            You are a financial expert. Answer the following question with professional financial advice:
            
            Question: {query}
            
            Provide a comprehensive, well-structured response that includes:
            - Clear explanation of the financial concept
            - Relevant examples or data points
            - Practical implications or recommendations
            - Risk considerations where applicable
            
            Keep your response informative but accessible to a general audience.
            """
            response = self.finance_llm.invoke([HumanMessage(content=prompt)])
            return self._extract_response_content(response)
            
        elif expert_type == "technical_expert":
            prompt = f"""
            You are a technical expert and software engineer. Answer the following question with professional technical guidance:
            
            Question: {query}
            
            Provide a comprehensive, well-structured response that includes:
            - Clear technical explanation
            - Code examples where relevant
            - Best practices and recommendations
            - Common pitfalls to avoid
            - Related concepts or technologies
            
            Keep your response technical but accessible to developers of varying skill levels.
            """
            response = self.technical_llm.invoke([HumanMessage(content=prompt)])
            return self._extract_response_content(response)
            
        else:  # general_expert
            prompt = f"""
            You are a knowledgeable and helpful AI assistant. Answer the following question thoughtfully:
            
            Question: {query}
            
            Provide a comprehensive, well-structured response that:
            - Addresses the question directly and completely
            - Provides relevant context and background information
            - Offers practical insights or examples where applicable
            - Maintains a helpful and engaging tone
            
            Be informative, accurate, and helpful in your response.
            """
            response = self.general_llm.invoke([HumanMessage(content=prompt)])
            return self._extract_response_content(response)
    
    async def aggregate_responses(self, query: str, responses: Dict[str, str], routing_reason: str) -> str:
        """Aggregate expert responses into a coherent answer"""
        if not responses:
            return "I apologize, but I was unable to process your question through our expert system."
        
        if len(responses) == 1:
            # Single expert - enhance the response
            expert_type, response = list(responses.items())[0]
            synthesis_prompt = f"""
            You are an expert editor. Take this expert response and enhance it to be more comprehensive and well-structured.
            
            Original Question: {query}
            Expert Response: {response}
            
            Enhance the response by:
            1. Ensuring it directly answers the user's question
            2. Adding relevant context or background information
            3. Structuring it in a clear, logical flow
            4. Making it more engaging and informative
            
            Provide an enhanced version that maintains the expert's authority while improving clarity and completeness.
            """
        else:
            # Multiple experts - synthesize their responses
            expert_responses = [f"{expert_type}: {response}" for expert_type, response in responses.items()]
            synthesis_prompt = f"""
            You are an expert synthesizer. Combine the following expert responses into a coherent, comprehensive answer.
            
            Original Question: {query}
            Routing Decision: {routing_reason}
            
            Expert Responses:
            {chr(10).join(expert_responses)}
            
            Your task is to:
            1. Identify the key insights from each expert
            2. Eliminate redundancy while preserving important information
            3. Create a well-structured, flowing response
            4. Ensure the final answer directly addresses the user's question
            5. Maintain the expertise and authority of the original responses
            
            Provide a comprehensive, well-organized answer that synthesizes all expert perspectives.
            """
        
        try:
            response = self.aggregator_llm.invoke([HumanMessage(content=synthesis_prompt)])
            return self._extract_response_content(response)
        except Exception as e:
            print(f"Aggregation error: {e}")
            # Fallback: combine responses manually
            if len(responses) > 1:
                expert_responses = [f"{expert_type}: {response}" for expert_type, response in responses.items()]
                return f"""
                Based on our expert analysis of your question: "{query}"

                {chr(10).join(expert_responses)}

                This response combines insights from multiple specialized experts to provide you with comprehensive information.
                """
            else:
                return list(responses.values())[0]
    
    async def process_query(self, query: str) -> Dict:
        """Main method to process a query through the multi-model system"""
        print(f"\n🔍 Processing query: {query}")
        
        # Step 1: Route the query
        routing_result = await self.route_query(query)
        route_to = routing_result["route_to"]
        routing_reason = routing_result["routing_reason"]
        
        print(f"🔄 Routing decision: {route_to}")
        print(f"💭 Reasoning: {routing_reason}")
        
        # Step 2: Process with experts
        responses = {}
        for expert_type in route_to:
            print(f"🧠 Processing with {expert_type}...")
            try:
                response = await self.process_with_expert(query, expert_type)
                responses[expert_type] = response
                print(f"✅ {expert_type} completed")
            except Exception as e:
                print(f"❌ {expert_type} error: {e}")
                responses[expert_type] = f"Error processing with {expert_type}: {str(e)}"
        
        # Step 3: Aggregate responses
        print("🔗 Aggregating expert responses...")
        final_response = await self.aggregate_responses(query, responses, routing_reason)
        print("✅ Aggregation completed")
        
        return {
            "user_message": query,
            "route_to": route_to,
            "routing_reason": routing_reason,
            "expert_responses": responses,
            "final_response": final_response
        }

# Global instance
multi_model_system = SimpleMultiModelSystem()

async def run_multi_model_query(query: str) -> Dict:
    """Convenience function to run a query through the multi-model system"""
    return await multi_model_system.process_query(query) 