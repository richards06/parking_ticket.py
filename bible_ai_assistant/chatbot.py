"""
Bible AI Chatbot - Main orchestrator
Coordinates scripture search, LLM generation, and conversation management
"""
from typing import Optional
from search_engine import ScriptureSearchEngine
from llm_handler import LLMHandler
from security import SecurityManager


class BibleAIChatbot:
    """
    Main Bible AI Assistant
    Handles user questions by retrieving relevant scripture
    and generating conversational responses with LLM
    """
    
    def __init__(self):
        self.search_engine = ScriptureSearchEngine()
        self.llm_handler = LLMHandler()
        self.security = SecurityManager()
        self.last_passages = []  # Track previous search results for follow-ups
    
    def answer_question(self, user_input: str) -> Optional[str]:
        """
        Process user question and generate Bible-grounded response
        
        Complete pipeline:
        1. Sanitize input (security)
        2. Check if this is a follow-up formatting request (list, table, etc.)
        3. Search for relevant scripture
        4. Generate conversational response with LLM
        5. Filter response (security)
        
        Args:
            user_input: User's question
        
        Returns:
            Professional, conversational response with scripture references
            Returns None if input is invalid/unsafe
        """
        # 1. SECURITY: Sanitize input
        sanitized_input = self.security.sanitize_input(user_input)
        
        if not sanitized_input:
            return "I'm unable to process that request. Please ask a clear question about Bible topics."
        
        # Add to conversation context
        self.llm_handler.add_conversation_context(sanitized_input)
        
        # 2. CHECK FOR FOLLOW-UP FORMATTING REQUESTS
        # If user asks for list/table/format of "them", reuse last results
        is_follow_up = self._is_formatting_request(sanitized_input)
        if is_follow_up and self.last_passages:
            print("\n🔄 Reformatting previous results...", flush=True)
            passages = self.last_passages
        else:
            # 3. SEARCH: Find relevant scripture passages
            print("\n🔍 Searching scripture...", end=" ", flush=True)
            passages = self.search_engine.search_for_guidance(sanitized_input)
            print(f"Found {len(passages)} passages")
            self.last_passages = passages  # Save for potential follow-ups
        
        # 4. GENERATE: Create conversational response
        print("💭 Generating response...", end=" ", flush=True)
        if is_follow_up:
            response = self._format_passages_as_list(passages, sanitized_input)
        else:
            response = self.llm_handler.generate_response(sanitized_input, passages)
        print("Done")
        
        # 5. SECURITY: Filter response
        final_response = self.security.filter_response(response)
        
        return final_response
    
    def _is_formatting_request(self, query: str) -> bool:
        """
        Detect if this is a follow-up request for reformatting previous results
        Examples: "put them in a list", "make it a table", "order them", "organize it"
        """
        query_lower = query.lower()
        formatting_keywords = [
            'list', 'table', 'order', 'organize', 'sort', 'arrange',
            'put them', 'make it', 'format', 'reformat', 'them in',
            'numbered', 'separate', 'break down', 'breakdown'
        ]
        
        return any(keyword in query_lower for keyword in formatting_keywords)
    
    def _format_passages_as_list(self, passages: list, user_request: str) -> str:
        """Format scripture passages as an ordered or bulleted list"""
        if not passages:
            return "No passages to format."
        
        # Check if user wants numbered list
        query_lower = user_request.lower()
        is_numbered = any(word in query_lower for word in ['number', 'order', 'list', 'commandments'])
        
        result = "Based on scripture:\n\n"
        
        # Format as numbered list for commandments or ordered lists
        if is_numbered or len(passages) > 3:
            for i, passage in enumerate(passages, 1):
                reference = passage.get("reference", "Unknown")
                text = passage.get("text", "")
                result += f"{i}. {reference}\n"
                result += f"   \"{text}\"\n\n"
        else:
            # Bulleted list
            for passage in passages:
                reference = passage.get("reference", "Unknown")
                text = passage.get("text", "")
                result += f"• {reference}\n"
                result += f"  \"{text}\"\n\n"
        
        return result
    
    def get_conversation_summary(self) -> str:
        """Get summary of conversation so far"""
        history = self.llm_handler.get_history()
        
        if not history:
            return "No conversation history yet."
        
        summary = f"\n📜 Conversation History ({len(history)} messages):\n"
        summary += "-" * 50 + "\n"
        
        for msg in history:
            role = "You" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary += f"{role}: {content}\n"
        
        return summary
    
    def reset_conversation(self) -> None:
        """Clear conversation history for new session"""
        self.llm_handler.clear_history()
    
    def get_info(self) -> str:
        """Get information about the Bible AI Assistant"""
        info = """
╔══════════════════════════════════════════════════════════════╗
║          BIBLE KNOWLEDGE ASSISTANT v1.0                      ║
║                                                              ║
║ A conversational AI that answers questions using Biblical    ║
║ guidance. All responses are rooted in scripture passages.    ║
║                                                              ║
║ Features:                                                    ║
║  • Real-time scripture search and retrieval                  ║
║  • AI-powered conversational responses                       ║
║  • Multi-turn conversation support                           ║
║  • Security protection against prompt injection              ║
║  • Professional, respectful communication                    ║
║                                                              ║
║ Usage: Ask any question and receive Bible-grounded answers  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        return info
