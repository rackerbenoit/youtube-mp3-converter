#!/usr/bin/env python3
"""
YouTube to MP3 Converter - Command Line Version
Downloads audio from YouTube/YouTube Music and converts to MP3
"""

import yt_dlp
import os
import sys
from pathlib import Path


def download_audio(url, output_path):
    """Download and convert YouTube audio to MP3"""

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }

    try:
        print(f"\nDownloading from: {url}")
        print(f"Saving to: {output_path}\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown')

        print(f"\n✓ Successfully downloaded and converted: {title}")
        print(f"✓ Saved to: {output_path}\n")
        return True

    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        return False


def main():
    print("=" * 60)
    print("YouTube to MP3 Converter (Command Line)")
    print("=" * 60)

    # Set default download location
    default_path = str(Path.home() / "Music" / "YouTube Downloads")
    os.makedirs(default_path, exist_ok=True)

    # Get URL from command line argument or prompt
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\nEnter YouTube URL: ").strip()

    if not url:
        print("Error: No URL provided")
        sys.exit(1)

    # Ask for custom path or use default
    custom_path = input(f"\nDownload folder (press Enter for default):\n[{default_path}]: ").strip()
    output_path = custom_path if custom_path else default_path

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Download
    success = download_audio(url, output_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
