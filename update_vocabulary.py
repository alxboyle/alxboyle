#!/usr/bin/env python3

import re
from pathlib import Path
import anki
from anki.collection import Collection
from datetime import datetime, timedelta


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


def get_current_streak():
    col_path = Path.home() / "AppData/Roaming/Anki2/User 1/collection.anki2"
    if not col_path.exists():
        col_path = Path.home() / ".local/share/Anki2/User 1/collection.anki2"
    if not col_path.exists():
        col_path = Path.home() / "Library/Application Support/Anki2/User 1/collection.anki2"
    
    if not col_path.exists():
        raise FileNotFoundError("Anki collection not found")
    
    col = Collection(str(col_path))
    
    # Get review history (revlog table contains review timestamps)
    query = """
    SELECT DISTINCT date(id/1000, 'unixepoch', 'localtime') as review_date
    FROM revlog 
    ORDER BY review_date DESC
    """
    
    rows = col.db.all(query)
    col.close()
    
    if not rows:
        return 0
    
    # Convert to datetime objects and check for consecutive days
    today = datetime.now().date()
    streak = 0
    
    for i, (date_str,) in enumerate(rows):
        review_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        expected_date = today - timedelta(days=i)
        
        if review_date == expected_date:
            streak += 1
        else:
            break
    
    return streak


def update_readme_badge(word_count, streak):
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding='utf-8')
    
    # Create badges
    vocab_badge_url = f"https://img.shields.io/badge/Anki%20Chinese%20Cards-{word_count}-blue"
    vocab_badge_markdown = f"![Anki Chinese Cards]({vocab_badge_url})"
    
    streak_badge_url = f"https://img.shields.io/badge/Day%20Streak-{streak}-orange"
    streak_badge_markdown = f"![Day Streak]({streak_badge_url})"
    
    # Patterns for existing badges
    vocab_pattern = r'!\[.*?\]\(https://img\.shields\.io/badge/(?:词汇|Anki%20Chinese%20Cards)-\d+-blue\)'
    streak_pattern = r'!\[Day Streak\]\(https://img\.shields\.io/badge/Day%20Streak-\d+-orange\)'
    
    # Update or add vocabulary badge
    if re.search(vocab_pattern, content):
        content = re.sub(vocab_pattern, vocab_badge_markdown, content)
    else:
        lines = content.split('\n')
        lines.insert(1, '')
        lines.insert(2, vocab_badge_markdown)
        content = '\n'.join(lines)
    
    # Update or add streak badge
    if re.search(streak_pattern, content):
        content = re.sub(streak_pattern, streak_badge_markdown, content)
    else:
        lines = content.split('\n')
        # Find where to insert the streak badge (after the vocab badge)
        for i, line in enumerate(lines):
            if 'Anki Chinese Cards' in line or '词汇' in line:
                lines.insert(i + 1, streak_badge_markdown)
                break
        content = '\n'.join(lines)
    
    readme_path.write_text(content, encoding='utf-8')


def main():
    try:
        word_count = get_seen_words_count()
        streak = get_current_streak()
        update_readme_badge(word_count, streak)
        print(f"Updated badges: {word_count} Anki Chinese cards, {streak} day streak")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
