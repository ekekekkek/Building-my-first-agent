from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage
from ..config.model_config import model_config

class FinanceExpert:
    def __init__(self):
        # Use configured finance model
        self.model_name = model_config.get_model("finance")
        self.llm = OllamaLLM(model=self.model_name)
        print(f"Finance Expert initialized with model: {self.model_name}")
    
    def process(self, state):
        """Process finance-related queries"""
        query = state["user_message"]
        
        # Enhanced finance prompt with context
        finance_prompt = f"""
        You are a financial expert. Answer the following question with professional financial advice:
        
        Question: {query}
        
        Provide a comprehensive, well-structured response that includes:
        - Clear explanation of the financial concept
        - Relevant examples or data points
        - Practical implications or recommendations
        - Risk considerations where applicable
        
        Keep your response informative but accessible to a general audience.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=finance_prompt)])
            return {"finance_response": response.content}
        except Exception as e:
            print(f"Finance expert error: {e}")
            return {"finance_response": f"I apologize, but I encountered an error processing your financial question: {str(e)}"}

class TechnicalExpert:
    def __init__(self):
        # Use configured technical model
        self.model_name = model_config.get_model("technical")
        self.llm = OllamaLLM(model=self.model_name)
        print(f"Technical Expert initialized with model: {self.model_name}")
    
    def process(self, state):
        """Process technical/programming queries"""
        query = state["user_message"]
        
        # Enhanced technical prompt with context
        technical_prompt = f"""
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
        
        try:
            response = self.llm.invoke([HumanMessage(content=technical_prompt)])
            return {"technical_response": response.content}
        except Exception as e:
            print(f"Technical expert error: {e}")
            return {"technical_response": f"I apologize, but I encountered an error processing your technical question: {str(e)}"}

class GeneralExpert:
    def __init__(self):
        # Use configured general model
        self.model_name = model_config.get_model("general")
        self.llm = OllamaLLM(model=self.model_name)
        print(f"General Expert initialized with model: {self.model_name}")
    
    def process(self, state):
        """Process general queries"""
        query = state["user_message"]
        
        # Enhanced general prompt with context
        general_prompt = f"""
        You are a knowledgeable and helpful AI assistant. Answer the following question thoughtfully:
        
        Question: {query}
        
        Provide a comprehensive, well-structured response that:
        - Addresses the question directly and completely
        - Provides relevant context and background information
        - Offers practical insights or examples where applicable
        - Maintains a helpful and engaging tone
        
        Be informative, accurate, and helpful in your response.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=general_prompt)])
            return {"general_response": response.content}
        except Exception as e:
            print(f"General expert error: {e}")
            return {"general_response": f"I apologize, but I encountered an error processing your question: {str(e)}"} 