#!/usr/bin/env python3

import re
from pathlib import Path
import anki
from anki.collection import Collection


def get_seen_words_count():
    col_path = Path.home() / "AppData/Roaming/Anki2/User 1/collection.anki2"
    if not col_path.exists():
        col_path = Path.home() / ".local/share/Anki2/User 1/collection.anki2"
    if not col_path.exists():
        col_path = Path.home() / "Library/Application Support/Anki2/User 1/collection.anki2"
    
    if not col_path.exists():
        raise FileNotFoundError("Anki collection not found")
    
    col = Collection(str(col_path))
    deck_id = col.decks.id("Mandarin: Vocabulary")
    
    if not deck_id:
        raise ValueError("Deck 'Mandarin: Vocabulary' not found")
    
    card_ids = col.decks.cids(deck_id, children=True)
    seen_count = 0
    
    for card_id in card_ids:
        card = col.get_card(card_id)
        if card.reps > 0:
            seen_count += 1
    
    col.close()
    return seen_count


def update_readme_badge(word_count):
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding='utf-8')
    
    badge_url = f"https://img.shields.io/badge/词汇-{word_count}-blue"
    badge_markdown = f"![Chinese Vocabulary]({badge_url})"
    
    badge_pattern = r'!\[Chinese Vocabulary\]\(https://img\.shields\.io/badge/词汇-\d+-blue\)'
    
    if re.search(badge_pattern, content):
        content = re.sub(badge_pattern, badge_markdown, content)
    else:
        lines = content.split('\n')
        lines.insert(1, '')
        lines.insert(2, badge_markdown)
        content = '\n'.join(lines)
    
    readme_path.write_text(content, encoding='utf-8')


def main():
    try:
        word_count = get_seen_words_count()
        update_readme_badge(word_count)
        print(f"Updated vocabulary badge with {word_count} seen words")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
