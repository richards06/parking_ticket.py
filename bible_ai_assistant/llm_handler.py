"""
LLM (Language Model) handler for generating conversational responses
Uses OpenAI API with retrieved scripture as context
"""
from typing import Dict, List, Optional
from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL, MAX_TOKENS, SYSTEM_PROMPT
from security import SecurityManager


class LLMHandler:
    """
    Handles interaction with OpenAI API for generating responses
    Uses scripture passages as context for grounded answers
    """
    
    def __init__(self):
        if not OPENAI_API_KEY:
            print("\n⚠️  WARNING: OPENAI_API_KEY not set in environment")
            print("   Bible responses will be generated without LLM enhancement")
            print("   Set OPENAI_API_KEY=sk-... in your .env file")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.conversation_history = []
    
    def generate_response(self, user_query: str, scripture_passages: List[Dict]) -> str:
        """
        Generate a conversational response to user's question
        Uses retrieved scripture passages as context
        
        Args:
            user_query: User's original question
            scripture_passages: List of relevant scripture passages
        
        Returns:
            Professional, conversational response grounded in scripture
        """
        # If no LLM available, generate basic response
        if not self.client:
            return self._generate_fallback_response(user_query, scripture_passages)
        
        # Build context from scripture passages
        scripture_context = self._format_scripture_context(scripture_passages)
        
        # Build messages for conversation
        messages = self._build_messages(user_query, scripture_context)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=0.7,
            )
            
            assistant_message = response.choices[0].message.content
            
            # Filter response for safety
            filtered_response = SecurityManager.filter_response(assistant_message)
            
            # Add to conversation history
            self._add_to_history("assistant", filtered_response)
            
            return filtered_response
        
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._generate_fallback_response(user_query, scripture_passages)
    
    def _format_scripture_context(self, passages: List[Dict]) -> str:
        """Format scripture passages into context string"""
        if not passages:
            return "No scripture passages found for this query."
        
        context = "RELEVANT SCRIPTURE PASSAGES:\n"
        context += "-" * 50 + "\n"
        
        for i, passage in enumerate(passages, 1):
            reference = passage.get("reference", "Unknown")
            text = passage.get("text", "")
            version = passage.get("version", "")
            
            context += f"\n{i}. {reference} ({version}):\n"
            context += f"   \"{text}\"\n"
        
        return context
    
    def _build_messages(self, user_query: str, scripture_context: str) -> List[Dict]:
        """Build message list for OpenAI API call"""
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        
        # Add scripture context
        messages.append({
            "role": "user",
            "content": f"Please use only these scripture passages to answer the question below:\n\n{scripture_context}\n\nQUESTION: {user_query}"
        })
        
        return messages
    
    def _generate_fallback_response(self, user_query: str, scripture_passages: List[Dict]) -> str:
        """
        Generate response without LLM (fallback when API not available)
        """
        if not scripture_passages:
            return "I couldn't find relevant scripture passages for this question. Please try rephrasing your question."
        
        response = "Based on scripture, here's guidance:\n\n"
        
        for passage in scripture_passages[:3]:  # Use top 3 passages
            reference = passage.get("reference", "Unknown")
            text = passage.get("text", "")
            
            response += f"{reference}:\n"
            response += f"\"{text}\"\n\n"
        
        return response
    
    def add_conversation_context(self, user_message: str) -> None:
        """Add user message to conversation history"""
        self._add_to_history("user", user_message)
    
    def _add_to_history(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Keep history manageable (last 10 messages)
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def clear_history(self) -> None:
        """Clear conversation history for new session"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict]:
        """Get current conversation history"""
        return self.conversation_history.copy()
