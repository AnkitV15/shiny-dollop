#!/usr/bin/env python3

import sys
from pattern_finder import recommend_patterns, display_card

def main():
    """Main function to run the command-line tool."""
    
    if "--list-all" in sys.argv or "-l" in sys.argv:
        from pattern_finder import display_all
        display_all()
        sys.exit(0)

    

    if len(sys.argv) < 2:
        print("❗ Usage: pattern \"problem description\" [--java|-j]")
        print("💡 Use '--list-all' or '-l' to see all patterns.")
        sys.exit(1)
    
    # Filter out the optional flags to get the clean description
    desc_args = [arg for arg in sys.argv[1:] if arg not in ["--java", "-j"]]
    desc = " ".join(desc_args)

    results = recommend_patterns(desc)

    if results:
        for card in results:
            display_card(card)
    else:
        print("❌ No matching patterns found. Try rephrasing your description or use more specific keywords.")

if __name__ == "__main__":
    main()
