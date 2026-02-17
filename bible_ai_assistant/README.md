# Bible Knowledge Assistant 📖

A conversational AI system that answers any question based on Biblical guidance. The assistant retrieves relevant scripture passages and uses an LLM to provide professional, respectful, and conversational responses.

## Features ✨

- **Real-Time Scripture Retrieval**: Searches and retrieves relevant Bible passages based on user questions
- **AI-Powered Responses**: Uses OpenAI's GPT to generate natural, conversational answers grounded in scripture
- **Multi-Turn Conversations**: Maintains context across multiple questions in a session
- **Security Protection**: Built-in defenses against prompt injection attacks and malicious input
- **Professional Communication**: All responses maintain respectful, appropriate tone
- **Fallback Support**: Works without LLM API (uses local Bible database) for demo purposes

## Project Structure 📁

```
bible_ai_assistant/
├── main.py                 # CLI entry point with conversation loop
├── chatbot.py              # Main orchestrator / coordinator
├── search_engine.py        # Scripture search and relevance ranking
├── bible_api.py            # Bible data retrieval (API + fallback)
├── llm_handler.py          # OpenAI integration
├── security.py             # Input/output sanitization & injection protection
├── config.py               # Configuration and constants
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md              # This file
```

## How It Works 🔄

1. **User Input** → Question or topic about life/faith
2. **Security Check** → Input validated for safety, injection attempts blocked
3. **Scripture Search** → Relevant passages retrieved and ranked by relevance
4. **LLM Generation** → AI generates conversational response with scripture context
5. **Response Filter** → Output checked for safety
6. **Display** → Professional response with scripture citations shown to user

### Data Flow

```
User Question
    ↓
Sanitize Input (Security)
    ↓
Search Scripture Database
    ↓
Rank by Relevance
    ↓
Format Scripture Context
    ↓
Send to OpenAI with System Prompt
    ↓
Generate Conversational Response
    ↓
Filter Response (Security)
    ↓
Display to User
```

## Setup & Installation 🚀

### Prerequisites
- Python 3.8+
- OpenAI API Key (optional, for full LLM functionality)

### 1. Clone/Download Repository
```bash
cd bible_ai_assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional but Recommended)
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...

# Get a free API key at: https://platform.openai.com/api-keys
```

### 4. Run the Assistant
```bash
python main.py
```

## Usage Examples 💬

### Basic Conversation
```
👤 You: How can I find peace?

⏳ Processing your question...
🔍 Searching scripture... Found 5 passages

📖 Assistant:
  In times of worry and uncertainty, scripture offers comfort.
  
  John 14:27 (NIV):
  "Peace I leave with you; my peace I give you. I do not 
   give to you as the world gives. Do not let your hearts 
   be troubled and do not be afraid."
  
  Philippians 4:6-7 (NIV):
  "Do not be anxious about anything, but in every situation, 
   by prayer and petition, with thanksgiving, present your 
   requests to God. And the peace of God, which transcends 
   all understanding, will guard your hearts and your minds 
   in Christ Jesus."
```

### Available Commands
- `help` - Show all commands
- `history` - View conversation history
- `clear` - Clear history for new session
- `info` - About the assistant
- `quit` or `exit` - End conversation

## Security Features 🔒

### Prompt Injection Protection
The system actively prevents prompt injection attacks by:
- Detecting common injection patterns (e.g., "ignore instructions", "jailbreak")
- Limiting input length and controlling special characters
- Validating scripture references
- Filtering LLM output for malicious content

### Input Validation
```python
# Blocked patterns examples:
- "ignore previous instructions"
- "system prompt"
- "pretend you are"
- "developer mode"
- "bypass these rules"
```

### Response Filtering
- Prevents leaking API keys, passwords, or sensitive data
- Ensures responses stay within Bible assistance scope
- Validates no system access attempts in output

### Conversation Context
- Maintains conversation history for coherent responses
- Auto-limits history to prevent context confusion attacks
- Clears session when requested

## Configuration ⚙️

### Environment Variables (.env)
```
OPENAI_API_KEY=sk-...              # Your OpenAI API key
BIBLE_API_KEY=...                  # Optional Bible API key
LLM_MODEL=gpt-3.5-turbo           # Model to use
```

### Key Configuration (config.py)
- `MAX_INPUT_LENGTH`: Maximum user input length (default: 1000)
- `MAX_CONVERSATION_HISTORY`: Messages to keep (default: 10)
- `MAX_TOKENS`: Max response length (default: 500)
- `SYSTEM_PROMPT`: Core instructions for the AI

## Limitations & Notes ⚠️

1. **Without OpenAI Key**: Assistant will work but without LLM enhancements (uses fallback responses)
2. **Scripture Database**: Currently includes ~10 common verses for demo; can be expanded
3. **Language**: English language support
4. **Interpretation**: Provides guidance but not theological debate resolution
5. **Privacy**: User questions sent to OpenAI if API is configured

## Extending the System 🛠️

### Add More Scripture (local_database in bible_api.py)
```python
{"reference": "Isaiah 41:10", "text": "...", "version": "NIV"}
```

### Add Topic Keywords (search_engine.py)
```python
"anxiety": ["Philippians 4:6-7", "Matthew 6:34", "1 Peter 5:7"]
```

### Integrate Real Bible API
```python
# Replace BIBLE_API_KEY with actual key from scripture.api.bible
# Modify bible_api.py to use full API endpoints
```

## Troubleshooting 🐛

### "APIError: Incorrect API key provided"
- Verify OPENAI_API_KEY is set correctly in .env
- Ensure key has permissions enabled
- Check at: https://platform.openai.com/account/api-keys

### "No responses generated"
- Check internet connection
- Verify Bible API fallback is working
- Review local database has content (bible_api.py)

### Slow responses
- First call may be slower (API startup)
- Network latency with OpenAI
- Try simpler questions first

## Getting API Keys 🔑

### OpenAI API
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API keys section
4. Create new secret key
5. Copy and paste into `.env` file as `OPENAI_API_KEY=sk-...`

**Free Trial**: OpenAI provides $5-18 free credits for 3 months

## Example Topics ❓

The assistant excels at:
- ✅ Finding Bible verses about specific topics
- ✅ Understanding Biblical guidance on life questions
- ✅ Discussing faith, purpose, and values
- ✅ Providing comfort and encouragement
- ✅ Explaining scripture passages

## Architecture Highlights 🏗️

### Modular Design
- Each component has single responsibility
- Easy to test and extend
- Clear separation of concerns

### Security-First Approach
- Input validation before processing
- Output filtering before display
- System prompt prevents jailbreaking
- Conversation limits prevent context confusion

### Graceful Degradation
- Works without LLM API (fallback mode)
- Uses local database if API unavailable
- Provides warnings for missing keys

## Future Enhancements 🔮

- [ ] Multiple language support
- [ ] Persistent conversation storage
- [ ] Advanced relevance ranking (semantic search)
- [ ] Audio input/output
- [ ] Web interface
- [ ] Larger scripture database (full Bible)
- [ ] Multi-version scripture support
- [ ] User preference tracking

## License 📜

This is an educational project. Scripture passages are public domain.

## Support & Feedback 💬

For issues or suggestions, please review:
- Documentation in code comments
- Security guidelines in security.py
- Configuration options in config.py

---

**Happy exploring the Word! May this tool help deepen your understanding of Scripture.** 📖✨
