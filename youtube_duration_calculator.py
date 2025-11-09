#!/usr/bin/env python3
"""
YouTube Video Duration Calculator
Calculates total duration of YouTube videos from a CSV file for language immersion tracking.
"""

import csv
import sys
import yt_dlp


def extract_video_id(url: str) -> str | None:
    """Extract video ID from various YouTube URL formats."""
    # Handle different YouTube URL formats
    if "youtu.be/" in url:
        # Format: https://youtu.be/VIDEO_ID or https://youtu.be/VIDEO_ID?si=XXXX
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    elif "youtube.com/watch" in url:
        # Format: https://www.youtube.com/watch?v=VIDEO_ID
        if "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
        else:
            return None
    else:
        return None

    return video_id if video_id else None


def get_video_duration(url: str) -> int:
    """
    Fetch video duration in seconds using yt-dlp.
    Returns 0 if unable to fetch duration.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,  # Get full info including duration
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
            title = info.get('title', 'Unknown')
            print(f"  ✓ {title[:50]}{'...' if len(title) > 50 else ''} - {format_duration(duration)}")
            return duration
    except Exception as e:
        print(f"  ✗ Error fetching {url}: {str(e)[:50]}")
        return 0


def format_duration(seconds: int) -> str:
    """Format duration from seconds to human-readable format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def calculate_total_duration(csv_file: str) -> float:
    """
    Read CSV file and calculate total duration of all videos.
    Returns total hours as a decimal.
    """
    total_seconds = 0
    video_count = 0
    successful_count = 0

    print(f"\n📊 Processing YouTube videos from {csv_file}\n")
    print("=" * 60)

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            urls = [row['URL'] for row in reader if row.get('URL')]

            if not urls:
                print("No URLs found in CSV file")
                return 0

            print(f"Found {len(urls)} videos to process\n")

            for i, url in enumerate(urls, 1):
                url = url.strip()
                if not url:
                    continue

                print(f"[{i}/{len(urls)}] Processing: {url[:60]}{'...' if len(url) > 60 else ''}")
                video_count += 1

                duration = get_video_duration(url)
                if duration > 0:
                    total_seconds += duration
                    successful_count += 1

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found")
        return 0
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return 0

    total_hours = total_seconds / 3600

    print("\n" + "=" * 60)
    print(f"\n📈 Summary:")
    print(f"  • Videos processed: {video_count}")
    print(f"  • Successfully fetched: {successful_count}")
    print(f"  • Failed: {video_count - successful_count}")
    print(f"\n🎯 Total Duration: {format_duration(total_seconds)}")
    print(f"⏱️  Total Hours: {total_hours:.2f} hours\n")

    return total_hours


def main():
    """Main function to handle CSV input and calculate total duration."""
    # Create sample CSV if needed
    sample_csv = "youtube_urls.csv"

    # Check if CSV file exists, if not create it with the provided URLs
    try:
        with open(sample_csv, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"Creating sample CSV file: {sample_csv}")
        urls = [
            "https://www.youtube.com/watch?v=YVvJL3ib_HY",
            "https://www.youtube.com/watch?v=UFjrHbPoo1g",
            "https://youtu.be/zqtQDWmuoz4?si=SMrDHsgyrwglguK0",
            "https://youtu.be/YCIFNPMu0hs?si=rsNeslfqMONd7F8o",
            "https://youtu.be/JqSWv26ug8c?si=tOEzPBwn3Qrdf3zr",
            "https://youtu.be/MQj6NvHfwPY?si=WEfWBNXaK_WuUdzj",
            "https://youtu.be/aHstoEgsJjg?si=hXi-SBQgyasRbVIz",
            "https://youtu.be/FN6iUHwieho?si=2LQ2J3Oimt9TiXzO",
            "https://youtu.be/1NGlyvnzTsA?si=gd0WvQqubw4pnArb",
            "https://youtu.be/yIutQYuEodc?si=mv0H8V7AVyWlekHo",
            "https://youtu.be/EzsPRDDob5g?si=jwq7o5uLvpgZmQCM",
            "https://youtu.be/MvIGb0VFxmI?si=7imN4w9i4lEk_vTw",
            "https://youtu.be/2rMFeanbEaQ?si=vrOrYflPUQe8IF0c",
            "https://youtu.be/3_1oDBQq9Mo?si=k1D6w5ixI3eK7ARd",
            "https://youtu.be/MFHyPvev_n8?si=NP1c0TWGrJmGGfBx",
            "https://youtu.be/0sYCpR0gNDk?si=8b9sLvLlRZRIjUtK",
            "https://youtu.be/hZmrbNRWMpE?si=JXboBK6FcMOzHzVp",
            "https://youtu.be/NBsl6cHucZU?si=ZntKgj-jlpu6_0Ro",
            "https://youtu.be/J8UfXSOKa7Y?si=-g8a5xOSpd0S5fEH",
        ]

        with open(sample_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL'])
            for url in urls:
                writer.writerow([url])
        print(f"Sample CSV created with {len(urls)} URLs\n")

    # Allow command line argument for CSV file
    csv_file = sys.argv[1] if len(sys.argv) > 1 else sample_csv

    # Calculate total duration
    total_hours = calculate_total_duration(csv_file)

    return total_hours


if __name__ == "__main__":
    main()