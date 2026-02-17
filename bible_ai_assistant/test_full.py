from chatbot import BibleAIChatbot

bot = BibleAIChatbot()

queries = [
    "what are the ten commandments?",
    "put them into a list in order for me"
]

for query in queries:
    print(f"\n{'='*70}")
    print(f"QUERY: {query}")
    print('='*70)
    response = bot.answer_question(query)
    print(response)
