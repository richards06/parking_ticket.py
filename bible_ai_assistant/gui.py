"""
Discord-style GUI for Bible AI Assistant
Modern chat interface with tkinter
"""
import tkinter as tk
from tkinter import scrolledtext, font
import threading
from chatbot import BibleAIChatbot


class BibleAIChatGUI:
    """Discord-style chat interface for Bible AI Assistant"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🙏 Jesus is ALWAYS the Answer!")
        self.root.geometry("800x700")
        self.root.configure(bg="#2C2F33")
        
        # Initialize chatbot
        self.chatbot = BibleAIChatbot()
        self.is_processing = False
        
        # Configure colors (Discord-inspired dark theme)
        self.BG_COLOR = "#2C2F33"
        self.FG_COLOR = "#FFFFFF"
        self.MESSAGE_BG = "#36393F"
        self.USER_COLOR = "#7289DA"
        self.BOT_COLOR = "#43B581"
        self.INPUT_BG = "#40444B"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.USER_COLOR)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text="✨ Jesus is ALWAYS the Answer! ✨",
            font=("Arial", 16, "bold"),
            bg=self.USER_COLOR,
            fg="white"
        )
        header_label.pack(pady=10)
        
        # Chat display area
        chat_frame = tk.Frame(self.root, bg=self.MESSAGE_BG)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg=self.MESSAGE_BG,
            fg=self.FG_COLOR,
            font=("Arial", 10),
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground=self.USER_COLOR, font=("Arial", 10, "bold"))
        self.chat_display.tag_config("bot", foreground=self.BOT_COLOR, font=("Arial", 10, "bold"))
        self.chat_display.tag_config("scripture", foreground="#FFD700", font=("Arial", 9, "italic"))
        self.chat_display.tag_config("normal", foreground=self.FG_COLOR)
        self.chat_display.tag_config("processing", foreground="#999999")
        
        # Welcome message
        self._display_message("Welcome to Bible AI Assistant!", "bot")
        self._display_message("Ask any question and receive Biblical guidance.\nType 'help' for commands.", "normal")
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.INPUT_BG)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Input label
        input_label = tk.Label(
            input_frame,
            text="What's good? (Nothing but God)",
            bg=self.INPUT_BG,
            fg=self.FG_COLOR,
            font=("Arial", 9)
        )
        input_label.pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        # Input box
        input_subframe = tk.Frame(input_frame, bg=self.INPUT_BG)
        input_subframe.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self.input_box = tk.Entry(
            input_subframe,
            bg="#36393F",
            fg=self.FG_COLOR,
            font=("Arial", 11),
            insertbackground=self.FG_COLOR,
            relief=tk.FLAT,
            borderwidth=2
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_box.bind("<Return>", self.on_send)
        
        # Send button
        self.send_button = tk.Button(
            input_subframe,
            text="Send",
            bg=self.USER_COLOR,
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.on_send,
            relief=tk.FLAT,
            padx=20,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.LEFT)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bg=self.BG_COLOR,
            fg="#999999",
            font=("Arial", 8)
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # Focus on input box
        self.input_box.focus()
    
    def _display_message(self, message: str, tag: str = "normal"):
        """Display a message in the chat window"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n\n", tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def on_send(self, event=None):
        """Handle send button click or Enter key"""
        user_input = self.input_box.get().strip()
        
        if not user_input:
            return
        
        # Display user message
        self._display_message(f"You: {user_input}", "user")
        self.input_box.delete(0, tk.END)
        
        # Handle commands
        if user_input.lower() == "help":
            self._show_help()
            return
        
        elif user_input.lower() == "clear":
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.chatbot.reset_conversation()
            self._display_message("Conversation cleared.", "bot")
            return
        
        elif user_input.lower() == "quit":
            self.root.quit()
            return
        
        # Process question in thread to prevent UI freeze
        self.is_processing = True
        self.send_button.config(state=tk.DISABLED)
        self.input_box.config(state=tk.DISABLED)
        self.status_label.config(text="Processing...")
        
        thread = threading.Thread(target=self._process_question, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def _process_question(self, user_input: str):
        """Process question in background thread"""
        try:
            response = self.chatbot.answer_question(user_input)
            
            # Re-enable UI after processing
            self.root.after(0, self._display_response, response)
        
        except Exception as e:
            self.root.after(0, self._display_response, f"Error: {str(e)}")
    
    def _display_response(self, response: str):
        """Display bot response (called from main thread)"""
        if response:
            # Format response with scripture highlighting
            self._display_message(f"Assistant:\n{response}", "bot")
        else:
            self._display_message(
                "Unable to process your question. Please try rephrasing it.",
                "bot"
            )
        
        # Re-enable UI
        self.is_processing = False
        self.send_button.config(state=tk.NORMAL)
        self.input_box.config(state=tk.NORMAL)
        self.input_box.focus()
        self.status_label.config(text="Ready")
    
    def _show_help(self):
        """Display help information"""
        help_text = """
═══════════════════════════════════════════════════════════
  AVAILABLE COMMANDS
═══════════════════════════════════════════════════════════

  help   - Show this help menu
  clear  - Clear conversation history
  quit   - Close the application

═══════════════════════════════════════════════════════════
  EXAMPLE QUESTIONS
═══════════════════════════════════════════════════════════

  • "How can I find peace in difficult times?"
  • "What does the Bible say about forgiveness?"
  • "What are the different types of fasts?"
  • "How do I handle anxiety?"
  • "What is God's purpose for my life?"
  • "How do I strengthen my faith?"

═══════════════════════════════════════════════════════════
  ✨ JESUS IS ALWAYS THE ANSWER! ✨
═══════════════════════════════════════════════════════════
"""
        self._display_message(help_text, "normal")


def run_gui():
    """Run the GUI application"""
    root = tk.Tk()
    app = BibleAIChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
