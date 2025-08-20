import os
import re
from fuzzywuzzy import fuzz, process
from flashcard_data import flashcards

# Flatten all signals for fuzzy matching
all_signals = [signal for card in flashcards for signal in card["signals"]]

def clean_text(text):
    """Normalize text by converting to lowercase and removing punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def recommend_patterns(description):
    """Recommend ALL patterns based on a problem description."""
    cleaned_desc = clean_text(description)
    
    matches = []
    desc_words = set(cleaned_desc.split())
    
    # Check for both full and partial fuzzy matches across all cards.
    for card in flashcards:
        card_signals_str = " ".join(card['signals'])
        
        # Check for direct keyword matches
        if any(word in desc_words for word in card_signals_str.split()):
            matches.append(card)
            continue
            
        # Check for broad fuzzy matches
        if fuzz.token_set_ratio(cleaned_desc, card_signals_str) > 60:
            matches.append(card)
            continue
            
        # Check for partial fuzzy matches
        if any(fuzz.partial_ratio(signal, cleaned_desc) > 80 for signal in card['signals']):
            matches.append(card)
    
    # Deduplicate the list to avoid showing the same card multiple times.
    unique_matches = []
    seen = set()
    for card in matches:
        if card['problem_type'] not in seen:
            unique_matches.append(card)
            seen.add(card['problem_type'])
            
    return unique_matches

def display_card(card):
    """Prints a single flashcard in a readable format, including Java code if available."""
    print(f"---")
    print(f"🧩 Problem Type: {card['problem_type']}")
    print(f"🔍 Signals: {', '.join(card['signals'])}")
    print(f"🧠 Patterns to Apply: {', '.join(card['patterns'])}")
    print(f"📌 Why It Works: {card['why']}")


def display_all():
    """Prints all flashcards in the database."""
    print("📋 All Available Patterns:")
    for card in flashcards:
        display_card(card)
        print("---")
