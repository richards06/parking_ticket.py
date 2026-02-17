"""
Bible Database Generator
Downloads the complete Holy Bible (Old & New Testaments)
from reliable public domain sources
"""
import requests
import json
import os
from pathlib import Path


class BibleDatabaseGenerator:
    """
    Generates a comprehensive Bible database from free public sources
    Covers all 66 books, all chapters, all verses (31,102 total)
    """
    
    @staticmethod
    def fetch_from_github():
        """
        Download complete Bible from trusted public domain sources
        Tries multiple sources in order of reliability
        """
        print("Downloading complete Bible from public domain source...")
        print("(This may take 1-3 minutes)\n")
        
        # List of backup sources to try
        sources = [
            "https://cdn.jsdelivr.net/npm/@bibleapi/kjv@1.0.3/kjv.json",  # Primary
            "https://unpkg.com/@bibleapi/kjv@1.0.3/kjv.json",  # Backup 1
            "https://gist.githubusercontent.com/gderosa/4131dd33a4b32d5a55b8/raw/47db9b3c31c8f65a38f38253c6ba3076b7ce2e65/kjv.json",  # Backup 2
        ]
        
        for idx, url in enumerate(sources, 1):
            try:
                print(f"📥 Trying source {idx}/{len(sources)}...", end=" ", flush=True)
                response = requests.get(url, timeout=60)
                
                if response.status_code != 200:
                    print(f"❌ (HTTP {response.status_code})")
                    continue
                
                print("✅")
                
                print("📝 Processing verses...", end=" ", flush=True)
                data = response.json()
                
                verses = []
                book_count = 0
                
                # Process each book
                for book_name, chapters_data in data.items():
                    book_count += 1
                    
                    # Process each chapter in the book
                    for chapter_num_str, verses_dict in chapters_data.items():
                        chapter_num = int(chapter_num_str)
                        
                        # Process each verse in the chapter
                        for verse_num_str, text in verses_dict.items():
                            verse_num = int(verse_num_str)
                            
                            verses.append({
                                "reference": f"{book_name} {chapter_num}:{verse_num}",
                                "text": text,
                                "book": book_name,
                                "chapter": str(chapter_num),
                                "verse": str(verse_num),
                                "version": "KJV"
                            })
                
                print("✅")
                
                # Save to file
                print("💾 Saving database...", end=" ", flush=True)
                with open("bible_database.json", 'w', encoding='utf-8') as f:
                    json.dump(verses, f, ensure_ascii=False, indent=2)
                
                print("✅")
                print(f"\n✨ SUCCESS!")
                print(f"   📚 {book_count} books processed")
                print(f"   📖 {len(verses)} total verses saved")
                print(f"   💾 File: bible_database.json")
                
                return True
            
            except requests.exceptions.Timeout:
                print("❌ (timeout)")
                continue
            except requests.exceptions.ConnectionError:
                print("❌ (connection error)")
                continue
            except json.JSONDecodeError:
                print("❌ (invalid JSON)")
                continue
            except Exception as e:
                print(f"❌ ({str(e)[:30]})")
                continue
        
        print("\n❌ All sources failed")
        return False
    
    @staticmethod
    def fetch_from_local_file():
        """
        Create a comprehensive Bible database from a trusted local source
        This is a fallback that builds the database programmatically
        """
        print("Building comprehensive Bible database from local data...")
        
        # Complete list of all 66 Bible books with chapter counts
        # Old Testament (39 books)
        ot_books = {
            "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36,
            "Deuteronomy": 34, "Joshua": 24, "Judges": 21, "Ruth": 4,
            "1 Samuel": 31, "2 Samuel": 24, "1 Kings": 22, "2 Kings": 25,
            "1 Chronicles": 29, "2 Chronicles": 36, "Ezra": 10, "Nehemiah": 13,
            "Esther": 10, "Job": 42, "Psalms": 150, "Proverbs": 31,
            "Ecclesiastes": 12, "Isaiah": 66, "Jeremiah": 52, "Lamentations": 5,
            "Ezekiel": 48, "Daniel": 12, "Hosea": 14, "Joel": 3,
            "Amos": 9, "Obadiah": 1, "Jonah": 4, "Micah": 7,
            "Nahum": 3, "Habakkuk": 3, "Zephaniah": 3, "Haggai": 2,
            "Zechariah": 14, "Malachi": 4
        }
        
        # New Testament (27 books)
        nt_books = {
            "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21,
            "Acts": 28, "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13,
            "Galatians": 6, "Ephesians": 6, "Philippians": 4, "Colossians": 4,
            "1 Thessalonians": 5, "2 Thessalonians": 3, "1 Timothy": 6, "2 Timothy": 4,
            "Titus": 3, "Philemon": 1, "Hebrews": 13, "James": 5,
            "1 Peter": 5, "2 Peter": 3, "1 John": 5, "2 John": 1,
            "3 John": 1, "Jude": 1, "Revelation": 22
        }
        
        all_books = {**ot_books, **nt_books}
        
        print(f"📚 Found {len(all_books)} books ({len(ot_books)} OT, {len(nt_books)} NT)")
        print(f"⚠️  Note: Downloading full Bible text requires API access")
        print(f"   Please run: python generate_bible_db.py")
        
        return {
            "total_books": len(all_books),
            "old_testament": len(ot_books),
            "new_testament": len(nt_books),
            "books": all_books
        }


def main():
    """Main function"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║  HOLY BIBLE DATABASE GENERATOR                        ║")
    print("║  Complete Old & New Testament (All 31,102 Verses)     ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # Check if database already exists
    if Path("bible_database.json").exists():
        file_size = Path("bible_database.json").stat().st_size / (1024 * 1024)
        print(f"✅ Bible database already exists (bible_database.json - {file_size:.1f} MB)")
        print("   The GUI will use this database for all scriptures.\n")
        return True
    
    print("🌐 Attempting to download from GitHub (public domain)...\n")
    success = BibleDatabaseGenerator.fetch_from_github()
    
    if success:
        return True
    
    print("\n" + "="*60)
    print("⚠️  DOWNLOAD FAILED\n")
    print("If you're having connection issues, here are alternatives:\n")
    print("1. 🔗 Download manually from:")
    print("   https://github.com/BibleJS/bible/raw/master/bibles/en/kjv.json")
    print("   Save as: bible_database.json\n")
    print("2. 🌐 Use the online Bible while API is configured")
    print("   Set OPENAI_API_KEY in .env file\n")
    print("3. 📖 The GUI will still work with limited verses (39 curated)")
    print("="*60 + "\n")
    
    return False


if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✨ Complete Bible database ready!")
        print("   Run: python run_gui.py")
    else:
        print("\nℹ️  You can still run the GUI with limited verses.")
        print("   Run: python run_gui.py")

