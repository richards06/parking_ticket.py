"""
Scripture search and relevance scoring module
"""
from typing import List, Dict
import re
from bible_api import BibleAPI


class ScriptureSearchEngine:
    """
    Searches for relevant scriptures based on user input
    and ranks them by relevance
    """
    
    # Topic to scripture mappings for better context
    TOPIC_KEYWORDS = {
        "love": ["1 John 4:7", "1 Corinthians 13", "John 13:34", "Romans 13:8"],
        "peace": ["John 14:27", "Philippians 4:6-7", "2 Timothy 1:7", "Psalm 29:11"],
        "faith": ["Hebrews 11:1", "Romans 3:28", "James 2:26", "Proverbs 3:5-6"],
        "hope": ["Romans 15:13", "1 Thessalonians 5:8", "Proverbs 23:18", "Jeremiah 29:11"],
        "forgiveness": ["Colossians 3:13", "Matthew 6:14-15", "Ezra 9:6-7", "Psalm 103:12"],
        "strength": ["Psalm 27:1", "Philippians 4:13", "Isaiah 40:31", "2 Timothy 1:7"],
        "guidance": ["Proverbs 3:5-6", "Psalm 25:4-5", "Isaiah 48:17", "John 16:13"],
        "wisdom": ["Proverbs 1:7", "James 1:5", "Proverbs 3:13", "Colossians 1:9-10"],
        "purpose": ["Jeremiah 29:11", "Ecclesiastes 12:13", "1 Peter 4:10", "2 Timothy 1:9"],
        "prayer": ["Matthew 6:6", "Philippians 4:6-7", "1 Thessalonians 5:17", "James 5:16"],
        "fasting": ["Isaiah 58:6-7", "Matthew 6:16-18", "Matthew 9:14-15", "Daniel 10:2-3", "Joel 2:12-13"],
        "fast": ["Isaiah 58:6-7", "Matthew 6:16-18", "Matthew 9:14-15", "Daniel 10:2-3"],
        "commandments": ["Exodus 20:1-17", "Deuteronomy 6:4", "Matthew 22:37-40", "Leviticus 19:18"],
        "ten commandments": ["Exodus 20:1-17", "Deuteronomy 5:4-21"],
        "exodus": ["Exodus 3:14", "Exodus 20:1-17"],
        "psalms": ["Psalm 23:1-6", "Psalm 27:1", "Psalm 42:5"],
        "jesus": ["John 3:16", "John 14:6", "Matthew 1:23"],
        "god": ["John 3:16", "Romans 3:23", "Jeremiah 29:11"],
    }
    
    def __init__(self):
        self.bible_api = BibleAPI()
    
    def search_for_guidance(self, user_query: str) -> List[Dict]:
        """
        Search for scripture passages relevant to user's question
        
        Args:
            user_query: User's question or topic
        
        Returns:
            List of relevant scripture passages ranked by relevance
        """
        passages = []
        
        # 1. Try topic-based lookup (pre-curated relevant verses)
        topic_passages = self._search_by_topic(user_query)
        
        # 2. Try API search (broader search)
        api_passages = self.bible_api.search_passages(user_query)
        
        # Remove duplicates (topic matches first since they're pre-curated)
        unique_passages = self._deduplicate_passages(topic_passages + api_passages)
        
        # Rank by relevance, boosting topic matches
        ranked_passages = self._rank_by_relevance(unique_passages, user_query, topic_passages)
        
        return ranked_passages[:5]  # Return top 5 most relevant
    
    def _search_by_topic(self, query: str) -> List[Dict]:
        """Search predefined topic keywords for relevant scriptures"""
        passages = []
        query_lower = query.lower()
        query_words = set(word.rstrip('s') for word in query_lower.split())  # Include singular forms
        
        for topic, references in self.TOPIC_KEYWORDS.items():
            topic_singular = topic.rstrip('s')
            # Match if topic or its singular form is in query
            if topic in query_lower or topic_singular in query_lower or topic in query_words or topic_singular in query_words:
                for reference in references:
                    verse = self.bible_api.get_verse(reference)
                    if verse:
                        passages.append(verse)
        
        return passages
    
    def _deduplicate_passages(self, passages: List[Dict]) -> List[Dict]:
        """Remove duplicate passages by reference"""
        seen = set()
        unique = []
        
        for passage in passages:
            ref = passage.get("reference", "").lower()
            if ref and ref not in seen:
                seen.add(ref)
                unique.append(passage)
        
        return unique
    
    def _rank_by_relevance(self, passages: List[Dict], query: str, topic_passages: List[Dict] = None) -> List[Dict]:
        """
        Rank passages by relevance score using multiple factors
        Higher score = more relevant
        Prioritizes exact keyword matches heavily and topic-matched verses
        """
        query_lower = query.lower()
        query_words = [word for word in query_lower.split() if len(word) > 2]  # Filter short words
        # Also include singular forms for better matching
        query_words_with_singular = set(query_words + [word.rstrip('s') for word in query_words])
        
        # Create set of topic passage references for quick lookup
        topic_refs = set()
        if topic_passages:
            topic_refs = {p.get('reference', '').lower() for p in topic_passages}
        
        scored_passages = []
        
        for passage in passages:
            score = 0
            text_lower = passage.get("text", "").lower()
            reference_lower = passage.get("reference", "").lower()
            
            # BOOST: Topic-matched passages get 200 point boost
            if reference_lower in topic_refs:
                score += 200
            
            # HIGHEST PRIORITY: Exact word match in text (70 points per word)
            for word in query_words_with_singular:
                if word in text_lower:
                    # Extra boost if word appears early in text
                    if text_lower.startswith(word) or f" {word} " in text_lower:
                        score += 70
                    else:
                        score += 40
            
            # HIGH PRIORITY: Exact phrase match (150 points)
            if query_lower in text_lower:
                score += 150
            
            # MEDIUM PRIORITY: Match in reference/book name (25 points)
            for word in query_words_with_singular:
                if word in reference_lower:
                    score += 25
            
            # Check how many different query words matched
            matching_word_count = sum(1 for word in query_words_with_singular if word in text_lower)
            if matching_word_count >= 2:
                score += 50  # Increased bonus for multiple word matches
            if matching_word_count >= 3:
                score += 100  # Extra bonus for 3+ word matches (high specificity)
            
            # Prefer verses that are specific (not too generic)
            text_length = len(passage.get("text", "").split())
            if 15 < text_length < 150:  # Good length for specific content
                score += 10
            
            scored_passages.append((score, passage))
        
        # Sort by score (highest first), then by length (longer verses for more detail)
        scored_passages.sort(key=lambda x: (-x[0], -len(x[1].get("text", ""))))
        
        # Return only relevant matches (score > 10 to filter out weak matches)
        return [passage for score, passage in scored_passages if score > 10]
    
    def get_multiple_perspectives(self, query: str) -> Dict[str, List[Dict]]:
        """
        Get scriptures organized by theme for different perspectives
        Useful for complex questions with multiple dimensions
        """
        perspectives = {}
        
        # Get general guidance
        perspectives["general"] = self.search_for_guidance(query)
        
        # Get related topics
        for topic in self.TOPIC_KEYWORDS.keys():
            combined_query = f"{query} {topic}"
            perspectives[topic] = self.search_for_guidance(combined_query)[:2]
        
        return perspectives
