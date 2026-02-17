"""
Main entry point for Bible AI Assistant
CLI interface with multi-turn conversation support
"""
import sys
from chatbot import BibleAIChatbot


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("  ✨ Jesus is ALWAYS the answer! ✨")
    print("="*60)
    print("\n  What's on your mind?\n")
    print("  ('help' for commands • 'quit' to exit)")
    print("\n" + "-"*60 + "\n")


def print_help():
    """Print help menu"""
    help_text = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AVAILABLE COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  help     - Show this help menu
  history  - View conversation history
  clear    - Clear conversation history
  quit     - Exit the application

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  EXAMPLE QUESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • "How can I find peace in difficult times?"
  • "What does the Bible say about forgiveness?"
  • "How should I handle anxiety?"
  • "What is God's purpose for my life?"
  • "How do I strengthen my faith?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  JESUS IS ALWAYS THE ANSWER! ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(help_text)


def format_response(response: str) -> str:
    """Format response with visual treatment"""
    lines = response.split('\n')
    formatted = "\n"
    for line in lines:
        if line.strip():
            formatted += f"  {line}\n"
        else:
            formatted += "\n"
    return formatted


def main():
    """Main conversation loop"""
    # Initialize chatbot
    chatbot = BibleAIChatbot()
    
    # Print welcome message
    print_welcome()
    
    conversation_count = 0
    
    try:
        while True:
            # Get user input
            user_input = input("What's good? (Nothing but God) ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                print("\n✨ Thank you for choosing Jesus! Goodbye! ✨\n")
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'history':
                print(chatbot.get_conversation_summary())
                continue
            
            elif user_input.lower() == 'clear':
                chatbot.reset_conversation()
                print("\n✅ Conversation history cleared.")
                continue
            
            # Process question
            print("\n⏳ Processing your question...")
            response = chatbot.answer_question(user_input)
            
            if response:
                print("\n" + format_response(response))
                print("-" * 60)
                conversation_count += 1
            else:
                print("\n❌ Unable to process your question. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Conversation interrupted.")
        print("✨ Thank you for choosing Jesus! Goodbye! ✨\n")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Please check your API keys and internet connection.")
        sys.exit(1)


if __name__ == "__main__":
    main()
