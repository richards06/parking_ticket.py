#!/usr/bin/env python3
"""
Quick Setup Script for Bible AI Assistant
Run this to verify all components are working
"""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python 3.8+ is installed"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required = ['requests', 'python-dotenv', 'openai']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    return len(missing) == 0, missing


def check_files():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'chatbot.py',
        'search_engine.py',
        'bible_api.py',
        'llm_handler.py',
        'security.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"{status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist


def check_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print("✅ .env file exists")
        return True
    else:
        print("⚠️  .env file not found (optional, but recommended)")
        return False


def print_setup_guide():
    """Print the complete setup guide"""
    guide = """
╔═══════════════════════════════════════════════════════════════╗
║     BIBLE AI ASSISTANT - SETUP CHECKLIST & COMMANDS          ║
╚═══════════════════════════════════════════════════════════════╝

PHASE 1: ENVIRONMENT SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☐ 1. Verify Python Version (3.8+)
   Syntax:
   python --version
   
   Expected Output:
   Python 3.11.x (or higher)

☐ 2. Install Required Packages
   Syntax:
   pip install -r requirements.txt
   
   Or install individually:
   pip install requests python-dotenv openai
   
   Verify installations:
   pip list | grep -E "requests|python-dotenv|openai"

☐ 3. Create .env File (OPTIONAL but RECOMMENDED)
   Syntax:
   copy .env.example .env
   
   Then edit .env and add your OpenAI API key:
   OPENAI_API_KEY=sk-your-api-key-here
   
   Get free API key at: https://platform.openai.com/api-keys


PHASE 2: PROJECT STRUCTURE VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☐ 4. Verify Project Files
   All these files should exist:
   • main.py (CLI entry point)
   • chatbot.py (main orchestrator)
   • search_engine.py (scripture search)
   • bible_api.py (scripture data)
   • llm_handler.py (OpenAI integration)
   • security.py (input/output protection)
   • config.py (configuration)
   • requirements.txt (dependencies)
   • .env.example (template)
   • README.md (documentation)
   
   Check with:
   dir  (Windows PowerShell)
   ls -la  (Mac/Linux)


PHASE 3: TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☐ 5. Test Module Imports
   Syntax:
   python -c "import config; print('✅ config.py OK')"
   python -c "import security; print('✅ security.py OK')"
   python -c "import bible_api; print('✅ bible_api.py OK')"
   python -c "import search_engine; print('✅ search_engine.py OK')"
   python -c "import llm_handler; print('✅ llm_handler.py OK')"
   python -c "import chatbot; print('✅ chatbot.py OK')"

☐ 6. Test Security Module
   Syntax:
   python -c "
from security import SecurityManager
# Test injection block
result = SecurityManager.sanitize_input('ignore instructions')
print('Injection blocked:', result is None)
# Test normal input
result = SecurityManager.sanitize_input('What is love?')
print('Normal input allowed:', result is not None)
"

☐ 7. Test Bible API
   Syntax:
   python -c "
from bible_api import BibleAPI
api = BibleAPI()
passages = api.search_passages('love', 'KJV')
print(f'Found {len(passages)} passages')
for p in passages[:2]:
    print(f'  - {p[\"reference\"]}: {p[\"text\"][:50]}...')
"

☐ 8. Test Search Engine
   Syntax:
   python -c "
from search_engine import ScriptureSearchEngine
engine = ScriptureSearchEngine()
results = engine.search_for_guidance('How to find peace?')
print(f'Search results: {len(results)} passages found')
for r in results[:2]:
    print(f'  - {r[\"reference\"]}')
"


PHASE 4: RUNNING THE APPLICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☐ 9. Start the Chatbot
   Syntax:
   python main.py
   
   Expected Output:
   ╔══════════════════════════════════════════════════════════╗
   ║          BIBLE KNOWLEDGE ASSISTANT v1.0                  ║
   ║                                                          ║
   ║ A conversational AI that answers Biblical questions      ║
   ...
   
   Then you'll see:
   👤 You: (waiting for input)

☐ 10. Test with Sample Questions
   Try one of these at the prompt:
   
   • "How can I find peace?"
   • "What does the Bible say about forgiveness?"
   • "How do I handle anxiety?"
   • "What is God's purpose for my life?"
   
   Expected Flow:
   👤 You: [Your question]
   
   ⏳ Processing your question...
   🔍 Searching scripture... Found X passages
   💭 Generating response... Done
   
   📖 Assistant:
     [Response with scripture citations]

☐ 11. Test Commands
   While running, try these commands:
   
   • Type: help
     → Shows available commands
   
   • Type: history
     → Shows conversation history
   
   • Type: clear
     → Clears conversation history
   
   • Type: quit or exit
     → Exits the program


PHASE 5: CONFIGURATION & OPTIMIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☐ 12. Configure API Key (Optional but Recommended)
   WITHOUT KEY: Uses fallback local Bible database
   WITH KEY: Generates rich conversational responses
   
   Steps:
   1. Get API key at: https://platform.openai.com/api-keys
   2. Edit .env file:
      OPENAI_API_KEY=sk-your-actual-key-here
   3. Restart main.py
   
   Verify it's working:
   python -c "
from config import OPENAI_API_KEY
if OPENAI_API_KEY and OPENAI_API_KEY != '':
    print('✅ API Key configured')
else:
    print('⚠️  Using fallback mode (no API key)')
"

☐ 13. Customize Scripture Database (Optional)
   Edit: bible_api.py
   Find: _get_local_database() method
   Add more verses in the list:
   
   {
       "reference": "Your Reference",
       "text": "Verse text here",
       "version": "NIV"
   }

☐ 14. Add Topic Keywords (Optional)
   Edit: search_engine.py
   Find: TOPIC_KEYWORDS dictionary
   Add new topics:
   
   "anxiety": ["Philippians 4:6-7", "Matthew 6:34"],
   "healing": ["Isaiah 53:5", "Psalm 107:20"],


QUICK COMMAND REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Install dependencies
pip install -r requirements.txt

# Setup environment file
copy .env.example .env

# Run the assistant
python main.py

# Test individual modules
python -c "import config; print('OK')"

# Check Python version
python --version

# List installed packages
pip list

# Uninstall and reinstall (if issues)
pip uninstall -y requests python-dotenv openai
pip install -r requirements.txt


TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ISSUE: "ModuleNotFoundError: No module named 'openai'"
FIX: pip install openai

ISSUE: "APIError: Incorrect API key"
FIX: Check your OPENAI_API_KEY in .env file
     Make sure it starts with 'sk-'

ISSUE: "No responses generated"
FIX: Function works in fallback mode without API
     Or check internet connection

ISSUE: Python version too old
FIX: pip install --upgrade python

ISSUE: Port already in use (if using web mode)
FIX: Change port in config.py or kill other processes


SUCCESS INDICATORS ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You'll know it's working when:
✅ All imports load without errors
✅ main.py starts and shows welcome message
✅ You can type a question and get a response
✅ Responses include scripture citations
✅ Commands (help, history, clear) work
✅ Attempts to inject prompts are blocked

"""
    print(guide)


if __name__ == "__main__":
    print_setup_guide()
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("RUNNING HEALTH CHECK...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print("📦 Python Version:")
    check_python_version()
    
    print("\n📚 Required Files:")
    check_files()
    
    print("\n🔧 Dependencies:")
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
    
    print("\n🔑 Configuration:")
    check_env_file()
    
    print("\n" + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Setup guide saved above. Follow the checklist to complete setup!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
