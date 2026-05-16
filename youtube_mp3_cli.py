#!/usr/bin/env python3
"""
YouTube to MP3 Converter - Command Line Version
Downloads audio from YouTube/YouTube Music and converts to MP3
"""

import os
import sys
import subprocess
from pathlib import Path


def download_audio(url, output_path):
    """Download and convert YouTube audio to MP3 using yt-dlp CLI"""

    # Find Node.js executable
    node_executable = None

    # First, try to find node in PATH using 'which'
    try:
        result = subprocess.run(['which', 'node'], capture_output=True, text=True, check=True)
        node_path = result.stdout.strip()
        if node_path and os.path.isfile(node_path):
            node_executable = node_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # If not found in PATH, check common installation locations
    if not node_executable:
        common_paths = [
            '/usr/local/bin/node',
            '/opt/homebrew/bin/node',
            os.path.expanduser('~/.nvm/current/bin/node'),
        ]
        for node_path in common_paths:
            if os.path.isfile(node_path):
                node_executable = node_path
                break

    print(f"\nDownloading from: {url}")
    print(f"Saving to: {output_path}\n")

    # Build yt-dlp command using Android client (most reliable)
    cmd = [
        'yt-dlp',
        '--format', 'bestaudio[ext=m4a]/bestaudio/best',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '192K',
        '--output', os.path.join(output_path, '%(title)s.%(ext)s'),
        '--no-check-certificate',
        '--no-write-thumbnail',
        '--remote-components', 'ejs:github',
        '--extractor-args', 'youtube:player_client=android,web',
    ]

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
