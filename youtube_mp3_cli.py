#!/usr/bin/env python3
"""
YouTube to MP3 Converter - Command Line Version
Downloads audio from YouTube/YouTube Music and converts to MP3
"""

import os
import sys
import subprocess
from pathlib import Path


def find_node_executable():
    """Find Node.js executable on the system"""
    # First, try to find node in PATH using 'which'
    try:
        result = subprocess.run(['which', 'node'], capture_output=True, text=True, check=True)
        node_path = result.stdout.strip()
        if node_path and os.path.isfile(node_path):
            return node_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # If not found in PATH, check common installation locations
    common_paths = [
        '/usr/local/bin/node',
        '/opt/homebrew/bin/node',
        os.path.expanduser('~/.nvm/current/bin/node'),
    ]
    for node_path in common_paths:
        if os.path.isfile(node_path):
            return node_path

    return None


def is_playlist(url):
    """Check if URL is a playlist"""
    return 'list=' in url or '/playlist' in url


def get_playlist_count(url):
    """Get the total number of videos in a playlist"""
    try:
        cmd = ['yt-dlp', '--flat-playlist', '--print', 'playlist_count', url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
        # Get the first line which should be the count
        lines = result.stdout.strip().split('\n')
        if lines and lines[0].isdigit():
            return int(lines[0])
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError):
        pass
    return None


def download_audio(url, output_path, playlist_start=None, playlist_end=None):
    """Download and convert YouTube audio to MP3 using yt-dlp CLI"""

    node_executable = find_node_executable()

    print(f"\nDownloading from: {url}")
    print(f"Saving to: {output_path}\n")

    # Build yt-dlp command using Android client (most reliable)
    cmd = [
        'yt-dlp',
        '--format', 'bestaudio[ext=m4a]/bestaudio/best',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '192K',
        '--output', os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
        '--no-check-certificate',
        '--no-write-thumbnail',
        '--remote-components', 'ejs:github',
        '--extractor-args', 'youtube:player_client=android,web',
        '--ignore-errors',  # Continue on download errors
    ]

    # Add playlist range if specified
    if playlist_start:
        cmd.extend(['--playlist-start', str(playlist_start)])
    if playlist_end:
        cmd.extend(['--playlist-end', str(playlist_end)])

    # Add Node.js runtime if found
    if node_executable:
        cmd.extend(['--js-runtimes', f'node:{node_executable}'])
        print(f"Using Node.js runtime: {node_executable}\n")

    cmd.append(url)

    try:
        # Run yt-dlp command
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)

        print(f"\n✓ Successfully downloaded and converted")
        print(f"✓ Saved to: {output_path}\n")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Download failed\n")
        return False
    except FileNotFoundError:
        print("\n✗ Error: yt-dlp not found. Please install it with: pip install yt-dlp\n")
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
        url = input("\nEnter YouTube URL (single video or playlist): ").strip()

    if not url:
        print("Error: No URL provided")
        sys.exit(1)

    # Check if it's a playlist
    playlist_start = None
    playlist_end = None

    if is_playlist(url):
        print("\n📋 Playlist detected!")
        print("\nOptions:")
        print("  1. Download all videos")
        print("  2. Download the first N videos")
        print("  3. Download the last N videos")
        print("  4. Download a range (e.g., videos 10-20)")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == '2':
            count = input("How many videos from the start? ").strip()
            try:
                playlist_end = int(count)
                print(f"\nWill download first {playlist_end} videos")
            except ValueError:
                print("Invalid number, downloading all videos")

        elif choice == '3':
            count = input("How many videos from the end? ").strip()
            try:
                count = int(count)
                print(f"\n⏳ Getting playlist info...")
                total = get_playlist_count(url)

                if total:
                    print(f"📊 Playlist has {total} videos total")
                    playlist_start = max(1, total - count + 1)
                    playlist_end = total
                    print(f"Will download videos {playlist_start} to {playlist_end} (last {count} videos)")
                else:
                    print("⚠️  Could not determine playlist size")
                    print("Please use option 4 and manually enter the range")
                    print("Example: If playlist has 200 videos and you want last 50, enter: 151-200")
                    return
            except ValueError:
                print("Invalid number, downloading all videos")

        elif choice == '4':
            range_input = input("Enter range (e.g., 10-20 or 151-200): ").strip()
            try:
                if '-' in range_input:
                    start, end = range_input.split('-')
                    playlist_start = int(start.strip())
                    playlist_end = int(end.strip())
                    print(f"\nWill download videos {playlist_start} to {playlist_end}")
                else:
                    print("Invalid range format, downloading all videos")
            except ValueError:
                print("Invalid range, downloading all videos")

    # Ask for custom path or use default
    custom_path = input(f"\nDownload folder (press Enter for default):\n[{default_path}]: ").strip()
    output_path = custom_path if custom_path else default_path

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Download
    success = download_audio(url, output_path, playlist_start, playlist_end)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
