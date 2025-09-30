from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, Any
from .base import AIService

class HuggingFaceService(AIService):
    """Implementation of Hugging Face model service."""
    
    def __init__(self):
        self.model_name = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    
    async def generate_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate code completion using Hugging Face model."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=kwargs.get("max_tokens", 2048),
                temperature=kwargs.get("temperature", 0.7),
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"choices": [{"text": response}]}
    
    async def generate_chat_response(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Generate chat response using Hugging Face model."""
        # Convert chat messages to a prompt format
        prompt = self._format_chat_messages(messages)
        return await self.generate_completion(prompt, **kwargs)
    
    def _format_chat_messages(self, messages: list) -> str:
        """Format chat messages into a prompt for the model."""
        formatted_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                formatted_messages.append(f"System: {content}")
            elif role == "user":
                formatted_messages.append(f"User: {content}")
            elif role == "assistant":
                formatted_messages.append(f"Assistant: {content}")
        return "\n".join(formatted_messages)