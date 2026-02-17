"""
Bible API module for retrieving scripture passages
Uses api.scripture.api.bible and includes fallback to comprehensive local database
"""
import requests
import json
from typing import Dict, List, Optional
from pathlib import Path
from config import BIBLE_API_KEY, BIBLE_API_URL


class BibleAPI:
    """Interface to Bible API for retrieving scripture passages"""
    
    # Common Bible translations (bible_id for api.scripture.api.bible)
    VERSIONS = {
        "KJV": "9879dbb7cfe39e4d-06",  # King James Version
        "NIV": "e4310ba60672e1ff-02",  # New International Version
        "ESV": "9879dbb7cfe39e4d-04",  # English Standard Version
        "NRSV": "9879dbb7cfe39e4d-05",  # New Revised Standard Version
    }
    
    def __init__(self):
        self.headers = {
            "api-key": BIBLE_API_KEY if BIBLE_API_KEY else "demo",  # demo key available
        }
        self.session = requests.Session()
    
    def search_passages(self, query: str, version: str = "KJV") -> List[Dict]:
        """
        Search for passages matching a query using the Bible API
        
        Args:
            query: Search term or topic
            version: Bible version (default: KJV)
        
        Returns:
            List of matching passages with text and reference
        """
        if not BIBLE_API_KEY:
            # Fallback to local database
            return self._search_local_database(query)
        
        try:
            bible_id = self.VERSIONS.get(version, self.VERSIONS["KJV"])
            
            # Search endpoint
            url = f"{BIBLE_API_URL}/bibles/{bible_id}/search"
            params = {"query": query, "limit": 5}
            
            response = self.session.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code != 200:
                return self._search_local_database(query)
            
            data = response.json()
            passages = []
            
            for verse in data.get("verses", []):
                passages.append({
                    "reference": verse.get("reference", "Unknown"),
                    "text": verse.get("text", ""),
                    "version": version
                })
            
            return passages
        
        except Exception as e:
            print(f"API Error: {e}")
            return self._search_local_database(query)
    
    def get_verse(self, reference: str, version: str = "KJV") -> Optional[Dict]:
        """
        Get a specific verse by reference (e.g., "John 3:16")
        
        Args:
            reference: Scripture reference (e.g., "John 3:16")
            version: Bible version
        
        Returns:
            Dictionary with verse reference and text, or None if not found
        """
        if not BIBLE_API_KEY:
            return self._get_verse_local(reference)
        
        try:
            bible_id = self.VERSIONS.get(version, self.VERSIONS["KJV"])
            
            # Get verse endpoint
            url = f"{BIBLE_API_URL}/bibles/{bible_id}/chapters"
            params = {"query": reference}
            
            response = self.session.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code != 200:
                return self._get_verse_local(reference)
            
            data = response.json()
            if data.get("data"):
                verse_data = data["data"][0]
                return {
                    "reference": verse_data.get("reference", reference),
                    "text": verse_data.get("content", ""),
                    "version": version
                }
        
        except Exception as e:
            print(f"API Error: {e}")
            return self._get_verse_local(reference)
        
        return None
    
    def _search_local_database(self, query: str) -> List[Dict]:
        """
        Search local Bible database
        First tries to load complete database (bible_database.json)
        Falls back to curated verses if complete database not available
        """
        # Try to load comprehensive database first
        db_file = Path("bible_database.json")
        if db_file.exists():
            try:
                with open(db_file, 'r', encoding='utf-8') as f:
                    verses = json.load(f)
            except Exception as e:
                print(f"Error loading bible_database.json: {e}")
                verses = self._get_local_database()
        else:
            # Fall back to curated database
            verses = self._get_local_database()
        
        results = []
        query_lower = query.lower()
        query_words = set(word for word in query_lower.split() if len(word) > 2)
        
        for verse in verses:
            text_lower = verse.get("text", "").lower()
            reference_lower = verse.get("reference", "").lower()
            
            # Score based on relevance
            score = 0
            
            # Exact match in text
            if query_lower in text_lower:
                score += 100
            
            # Word matches in text
            matching_words = sum(1 for word in query_words if word in text_lower)
            score += matching_words * 25
            
            # Match in reference
            if any(word in reference_lower for word in query_words):
                score += 15
            
            # Book match (if asking about a specific book)
            if "reference" in verse and any(word in verse.get("book", "").lower() for word in query_words):
                score += 10
            
            if score > 0:
                results.append((score, verse))
        
        # Sort by relevance score
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [verse for score, verse in results[:10]]  # Return top 10 most relevant
    
    def _get_verse_local(self, reference: str) -> Optional[Dict]:
        """Retrieve verse from local database by reference"""
        # Try comprehensive database first
        db_file = Path("bible_database.json")
        if db_file.exists():
            try:
                with open(db_file, 'r', encoding='utf-8') as f:
                    verses = json.load(f)
                    
                    ref_lower = reference.lower().strip()
                    for verse in verses:
                        if verse.get("reference", "").lower() == ref_lower:
                            return verse
            except Exception as e:
                pass  # Fall through to curated database
        
        # Fall back to curated database
        local_db = self._get_local_database()
        reference_normalized = reference.strip().lower()
        
        for passage in local_db:
            if passage["reference"].lower() == reference_normalized:
                return passage
        
        return None
    
    @staticmethod
    def _get_local_database() -> List[Dict]:
        """
        Local database of common Bible passages (fallback when API unavailable)
        Comprehensive collection organized by topic for better relevance
        """
        return [
            # Love
            {"reference": "John 3:16", "text": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.", "version": "NIV"},
            {"reference": "1 John 4:7-8", "text": "Dear friends, let us love one another, for love comes from God. Everyone who loves has been born of God and knows God. Whoever does not love does not know God, because God is love.", "version": "NIV"},
            {"reference": "1 Corinthians 13:4-7", "text": "Love is patient, love is kind. It does not envy, it does not boast, it is not proud. It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs. Love does not delight in evil but rejoices with the truth. It always protects, always trusts, always hopes, always perseveres.", "version": "NIV"},
            
            # Peace
            {"reference": "John 14:27", "text": "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid.", "version": "NIV"},
            {"reference": "Philippians 4:6-7", "text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", "version": "NIV"},
            {"reference": "Isaiah 26:3", "text": "You will keep in perfect peace those whose minds are steadfast, because they trust in you.", "version": "NIV"},
            
            # Faith
            {"reference": "Hebrews 11:1", "text": "Now faith is confidence in what we hope for and assurance about what we do not see.", "version": "NIV"},
            {"reference": "Romans 3:28", "text": "For we maintain that a person is justified by faith apart from the works of the law.", "version": "NIV"},
            {"reference": "Mark 11:24", "text": "Therefore I tell you, whatever you ask for in prayer, believe that you have received it, and it will be yours.", "version": "NIV"},
            
            # Guidance & Purpose
            {"reference": "Proverbs 3:5-6", "text": "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.", "version": "NIV"},
            {"reference": "Jeremiah 29:11", "text": "For I know the plans I have for you, declares the Lord, plans for welfare and not for evil, to give you a future and a hope.", "version": "ESV"},
            {"reference": "Psalm 25:4-5", "text": "Show me your ways, Lord, teach me your paths. Guide me in your truth and teach me, for you are God my Savior, and my hope is in you all day long.", "version": "NIV"},
            
            # Forgiveness
            {"reference": "Colossians 3:13", "text": "Bear with each other and forgive one another if any of you has a grievance against someone. Forgive as the Lord forgave you.", "version": "NIV"},
            {"reference": "Matthew 6:14-15", "text": "For if you forgive other people when they sin against you, your heavenly Father will also forgive you. But if you do not forgive others their sins, your Father will not forgive your sins.", "version": "NIV"},
            {"reference": "Psalm 103:12", "text": "As far as the east is from the west, so far has he removed our transgressions from us.", "version": "NIV"},
            
            # Strength
            {"reference": "Psalm 27:1", "text": "The Lord is my light and my salvation—whom shall I fear? The Lord is the stronghold of my life—of whom shall I be afraid?", "version": "NIV"},
            {"reference": "Philippians 4:13", "text": "I can do all this through him who gives me strength.", "version": "NIV"},
            {"reference": "2 Timothy 1:7", "text": "For the Spirit God gave us does not make us timid, but gives us power, love and a sound mind.", "version": "NIV"},
            
            # Anxiety & Worry
            {"reference": "Matthew 6:25-26", "text": "Therefore I tell you, do not worry about your life, what you will eat or drink; or about your body, what you will wear. Is not life more than clothes, and the body more than clothes? Look at the birds of the air; they do not sow or reap or store away in barns, and yet your heavenly Father feeds them. Are you not much more valuable than they?", "version": "NIV"},
            {"reference": "1 Peter 5:7", "text": "Cast all your anxiety on him because he cares for you.", "version": "NIV"},
            {"reference": "Proverbs 12:25", "text": "Anxiety weighs down the heart, but a kind word cheers it up.", "version": "NIV"},
            
            # Fasting
            {"reference": "Isaiah 58:6-7", "text": "Is not this the kind of fasting I have chosen: to loose the chains of injustice and untie the cords of the yoke, to set the oppressed free and break every yoke? Is it not to share your food with the hungry and to provide the poor wanderer with shelter—when you see the naked, to clothe them, and not to turn away from your own flesh and blood?", "version": "NIV"},
            {"reference": "Matthew 6:16-18", "text": "When you fast, do not look somber as the hypocrites do, for they disfigure their faces to show others they are fasting. Truly I tell you, they have received their reward in full. But when you fast, put oil on your head and wash your face, to show others that you are fasting, but only to your Father, who is unseen; and your Father, who sees what is done in secret, will reward you.", "version": "NIV"},
            {"reference": "Joel 2:12-13", "text": "Even now, declares the Lord, return to me with all your heart, with fasting and weeping and mourning. Rend your heart and not your garments. Return to the Lord your God, for he is gracious and compassionate, slow to anger and abounding in love, and he relents from sending calamity.", "version": "NIV"},
            
            # Wisdom
            {"reference": "Proverbs 1:7", "text": "The fear of the Lord is the beginning of knowledge, but fools despise wisdom and instruction.", "version": "NIV"},
            {"reference": "James 1:5", "text": "If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault, and it will be given to you.", "version": "NIV"},
            {"reference": "Proverbs 3:13-14", "text": "Blessed are those who find wisdom, those who gain understanding, for she is more profitable than silver and yields better returns than gold.", "version": "NIV"},
            
            # Hope
            {"reference": "Romans 15:13", "text": "May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit.", "version": "NIV"},
            {"reference": "Proverbs 23:18", "text": "There is surely a future hope for you, and your hope will not be cut off.", "version": "NIV"},
            {"reference": "Hebrews 6:19", "text": "We have this hope as an anchor for the soul, firm and secure. It enters the inner sanctuary behind the curtain.", "version": "NIV"},
            
            # Prayer
            {"reference": "Matthew 6:6", "text": "But when you pray, go into your room, close the door and pray to your Father, who is unseen. Then your Father, who sees what is done in secret, will reward you.", "version": "NIV"},
            {"reference": "1 Thessalonians 5:17", "text": "Pray without ceasing.", "version": "NIV"},
            {"reference": "James 5:16", "text": "Therefore confess your sins to each other and pray for each other so that you may be healed. The prayer of a righteous person is powerful and effective.", "version": "NIV"},
            
            # Healing
            {"reference": "Isaiah 53:5", "text": "But he was pierced for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was on him, and by his wounds we are healed.", "version": "NIV"},
            {"reference": "Psalm 6:2", "text": "Have mercy on me, Lord, for I am faint; heal me, Lord, for my bones are in agony.", "version": "NIV"},
            {"reference": "3 John 1:2", "text": "Dear friend, I pray that you may enjoy good health and that all may go well with you, even as your soul is getting along well.", "version": "NIV"},
            
            # Encouragement
            {"reference": "Psalm 23:1", "text": "The Lord is my shepherd, I lack nothing.", "version": "NIV"},
            {"reference": "Romans 8:28", "text": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.", "version": "NIV"},
            {"reference": "Philippians 4:8", "text": "Finally, brothers and sisters, whatever is true, whatever is noble, whatever is right, whatever is pure, whatever is lovely, whatever is admirable—if anything is excellent or praiseworthy—think about such things.", "version": "NIV"},
        ]
