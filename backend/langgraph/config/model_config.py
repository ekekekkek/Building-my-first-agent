import os
from typing import Dict, Optional

class ModelConfig:
    """Configuration for different Ollama models used by experts"""
    
    def __init__(self):
        # Default models - can be overridden by environment variables
        self.models = {
            "router": os.getenv("ROUTER_MODEL", "mistral:7b"),
            "finance": os.getenv("FINANCE_MODEL", "mistral:7b"),
            "technical": os.getenv("TECHNICAL_MODEL", "mistral:7b"),
            "general": os.getenv("GENERAL_MODEL", "mistral:7b"),
            "aggregator": os.getenv("AGGREGATOR_MODEL", "mistral:7b")
        }
        
        # Model descriptions for logging
        self.model_descriptions = {
            "router": "Intelligent routing and classification",
            "finance": "Financial expertise and analysis",
            "technical": "Technical and programming knowledge",
            "general": "General knowledge and conversation",
            "aggregator": "Response synthesis and enhancement"
        }
    
    def get_model(self, model_type: str) -> str:
        """Get model name for a specific type"""
        return self.models.get(model_type, "mistral:7b")
    
    def update_model(self, model_type: str, model_name: str):
        """Update model for a specific type"""
        if model_type in self.models:
            self.models[model_type] = model_name
            print(f"Updated {model_type} model to: {model_name}")
        else:
            print(f"Unknown model type: {model_type}")
    
    def get_all_models(self) -> Dict[str, str]:
        """Get all configured models"""
        return self.models.copy()
    
    def get_model_description(self, model_type: str) -> str:
        """Get description for a model type"""
        return self.model_descriptions.get(model_type, "Unknown model type")
    
    def validate_models(self) -> bool:
        """Validate that all models are properly configured"""
        for model_type, model_name in self.models.items():
            if not model_name or model_name.strip() == "":
                print(f"Warning: {model_type} model is not configured")
                return False
        return True

# Global configuration instance
model_config = ModelConfig() 