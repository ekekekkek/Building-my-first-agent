from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage
from ..config.model_config import model_config

class AggregatorNode:
    def __init__(self):
        # Use configured aggregator model
        self.model_name = model_config.get_model("aggregator")
        self.llm = OllamaLLM(model=self.model_name)
        print(f"Aggregator initialized with model: {self.model_name}")
    
    def synthesize(self, state):
        """Combine expert responses into coherent answer"""
        user_message = state.get("user_message", "")
        finance_response = state.get("finance_response", "")
        technical_response = state.get("technical_response", "")
        general_response = state.get("general_response", "")
        routing_reason = state.get("routing_reason", "")
        
        # Collect all available responses
        expert_responses = []
        if finance_response:
            expert_responses.append(f"Finance Expert: {finance_response}")
        if technical_response:
            expert_responses.append(f"Technical Expert: {technical_response}")
        if general_response:
            expert_responses.append(f"General Expert: {general_response}")
        
        if len(expert_responses) > 1:
            # Multiple experts - synthesize their responses
            synthesis_prompt = f"""
            You are an expert synthesizer. Combine the following expert responses into a coherent, comprehensive answer.
            
            Original Question: {user_message}
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
        elif len(expert_responses) == 1:
            # Single expert - enhance and structure the response
            synthesis_prompt = f"""
            You are an expert editor. Take this expert response and enhance it to be more comprehensive and well-structured.
            
            Original Question: {user_message}
            Expert Response: {expert_responses[0]}
            
            Enhance the response by:
            1. Ensuring it directly answers the user's question
            2. Adding relevant context or background information
            3. Structuring it in a clear, logical flow
            4. Making it more engaging and informative
            
            Provide an enhanced version that maintains the expert's authority while improving clarity and completeness.
            """
        else:
            # No expert responses - provide a fallback
            return {"final_response": "I apologize, but I was unable to process your question through our expert system. Please try rephrasing your question or contact support if the issue persists."}
        
        try:
            response = self.llm.invoke([HumanMessage(content=synthesis_prompt)])
            return {"final_response": response.content}
        except Exception as e:
            print(f"Aggregator error: {e}")
            # Fallback: combine responses manually
            if len(expert_responses) > 1:
                fallback_response = f"""
                Based on our expert analysis of your question: "{user_message}"

                {chr(10).join(expert_responses)}

                This response combines insights from multiple specialized experts to provide you with comprehensive information.
                """
            else:
                fallback_response = expert_responses[0] if expert_responses else "I apologize, but I was unable to process your question."
            
            return {"final_response": fallback_response} 