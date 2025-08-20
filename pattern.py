#!/usr/bin/env python3

import difflib
import re
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

flashcards = [
    {
        "problem_type": "Array Manipulation",
        "signals": ["sliding window", "max subarray", "window", "range", "contiguous"],
        "patterns": ["Sliding Window", "Prefix Sum", "Two Pointers"],
        "why": "Optimize over contiguous segments",
    },
    {
        "problem_type": "Searching in Arrays",
        "signals": ["target", "sorted", "find", "position", "search"],
        "patterns": ["Binary Search", "Two Pointers"],
        "why": "Fast lookup in sorted data",
    },
    {
        "problem_type": "Pairing / Matching",
        "signals": ["two sum", "closest pair", "grouping", "pair", "match"],
        "patterns": ["Hashing", "Sorting + Greedy", "Two Pointers"],
        "why": "Efficient pairing via structure",
    },
    {
        "problem_type": "Subsets / Combinations",
        "signals": ["all combinations", "subsets", "permutations", "generate", "explore"],
        "patterns": ["Backtracking", "Recursion"],
        "why": "Explore all possibilities",
    },
    {
        "problem_type": "Dynamic Decisions",
        "signals": ["max profit", "min cost", "choices", "states", "optimal substructure"],
        "patterns": ["Dynamic Programming (DP)"],
        "why": "Optimal substructure, overlapping subproblems",
    },
    {
        "problem_type": "Graph Traversal",
        "signals": ["connected", "path", "cycle", "reachability", "graph", "edge", "node"],
        "patterns": ["BFS", "DFS", "Union-Find"],
        "why": "Explore relationships and connectivity",
    },
    {
        "problem_type": "Tree Problems",
        "signals": ["traverse", "depth", "ancestor", "balanced", "tree", "root", "leaf"],
        "patterns": ["DFS", "Recursion", "Binary Search Tree (BST)"],
        "why": "Hierarchical structure traversal",
    },
    {
        "problem_type": "Greedy Optimization",
        "signals": ["maximize", "minimize", "locally optimal", "greedy"],
        "patterns": ["Greedy"],
        "why": "Local choices lead to global optimum",
    },
    {
        "problem_type": "Interval Scheduling",
        "signals": ["overlap", "merge", "meeting rooms", "range", "intervals"],
        "patterns": ["Sorting + Greedy", "Sweep Line"],
        "why": "Sort and process events efficiently",
    },
    {
        "problem_type": "String Matching / Parsing",
        "signals": ["substring", "pattern", "anagram", "valid", "string", "parse"],
        "patterns": ["Hashing", "Sliding Window", "Stack"],
        "why": "Track frequency, structure, or balance",
    },
    {
        "problem_type": "Monotonic Behavior",
        "signals": ["next greater", "increasing", "stock span", "monotonic"],
        "patterns": ["Monotonic Stack / Queue"],
        "why": "Track trends with efficient memory",
    },
    {
        "problem_type": "Heap / Priority Scheduling",
        "signals": ["kth largest", "top k", "merge sorted", "heap", "priority queue"],
        "patterns": ["Min/Max Heap", "Priority Queue"],
        "why": "Efficient selection from dynamic data",
    },
    {
        "problem_type": "Bit Manipulation",
        "signals": ["xor", "parity", "toggle", "mask", "bit", "manipulation", "masking", "bits"],
        "patterns": ["Bitmasking", "XOR tricks"],
        "why": "Constant-time operations on bits",
    },
    {
        "problem_type": "Math / Number Theory",
        "signals": ["gcd", "modulo", "prime", "divisible", "math", "number theory"],
        "patterns": ["Euclidean Algorithm", "Sieve", "Modular Arithmetic"],
        "why": "Mathematical properties for optimization",
    },
    {
        "problem_type": "Game Theory / Strategy",
        "signals": ["win", "lose", "turns", "optimal play", "game theory"],
        "patterns": ["DP + Minimax", "Grundy Numbers"],
        "why": "Strategic decision-making under constraints",
    },
]

def clean_text(text):
    """Normalize text by converting to lowercase and removing punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def find_best_match(description):
    """Find the best matching flashcard based on fuzzy string matching."""
    best_match = None
    best_score = 0
    
    # Create a flattened list of all signals with their parent flashcard index
    all_signals_with_indices = []
    for i, card in enumerate(flashcards):
        for signal in card['signals']:
            all_signals_with_indices.append((signal, i))
    
    # Use fuzzywuzzy to find the best matching signal
    match = process.extractOne(description, [s[0] for s in all_signals_with_indices], scorer=fuzz.token_sort_ratio)
    
    if match and match[1] > 60: # Threshold for a good match
        matched_signal = match[0]
        # Find the card that contains the matched signal
        for card in flashcards:
            if matched_signal in card['signals']:
                return card
    
    return None

def recommend_patterns(description):
    """Recommend patterns based on a problem description."""
    cleaned_desc = clean_text(description)
    
    # Try a broad fuzzy match first
    matched_card = find_best_match(cleaned_desc)
    if matched_card:
        return [matched_card]
    
    # If a broad match fails, check for token-based matches
    matches = []
    desc_words = set(cleaned_desc.split())
    for card in flashcards:
        if any(signal in desc_words or any(fuzz.partial_ratio(signal, cleaned_desc) > 80 for signal in card['signals']) for signal in card['signals']):
            matches.append(card)
    
    # Use fuzzy matching as a fallback for the entire description
    if not matches:
        for card in flashcards:
            if fuzz.token_set_ratio(cleaned_desc, " ".join(card['signals'])) > 60:
                matches.append(card)

    return matches

def display_card(card):
    """Prints a single flashcard in a readable format."""
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

def main():
    """Main function to run the command-line tool."""
    if "--list-all" in sys.argv or "-l" in sys.argv:
        display_all()
        sys.exit(0)

    if len(sys.argv) < 2:
        print("❗ Usage: pattern \"problem description\"")
        print("💡 Use '--list-all' or '-l' to see all patterns.")
        sys.exit(1)
    
    desc = " ".join(sys.argv[1:])
    results = recommend_patterns(desc)

    if results:
        for card in results:
            display_card(card)
    else:
        print("❌ No matching patterns found. Try rephrasing your description or use more specific keywords.")

if __name__ == "__main__":
    main()