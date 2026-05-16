# YouTube to MP3 Converter for macOS

A simple command-line tool that downloads audio from YouTube and YouTube Music and converts to MP3 format.

## Features

- Simple command-line interface
- Download from YouTube and YouTube Music
- Automatic conversion to MP3 (192kbps quality)
- Real-time download progress
- Configurable download location
- Pass URL as argument for quick downloads

## Quick Start

For experienced users who already have Homebrew, Python 3.8+, FFmpeg, and Node.js installed:

```bash
cd youtube-mp3-converter
pip3 install --break-system-packages -r requirements.txt
python3 youtube_mp3_cli.py
```

---

## Complete Setup Guide (New Mac)

### 1. Install Homebrew

Open Terminal (`Command + Space`, type "Terminal"):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Important:** After installation, follow the on-screen instructions to add Homebrew to your PATH. You'll need to run two commands that look like:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Close and reopen Terminal, then verify:

```bash
brew --version
```

### 2. Install Required Tools

```bash
brew install python3 ffmpeg node
```

Verify installations:

```bash
python3 --version  # Should be 3.8 or higher
node --version     # Should be v14 or higher
```

### 3. Install Python Dependencies

Navigate to the project folder:

```bash
cd /path/to/youtube-mp3-converter
```

Install yt-dlp:

```bash
pip3 install --break-system-packages -r requirements.txt
```

---

## Usage

### Interactive Mode

```bash
python3 youtube_mp3_cli.py
```

You'll be prompted for:
1. YouTube URL
2. Download location (press Enter for default: `~/Music/YouTube Downloads`)

### Quick Mode (URL as Argument)

```bash
python3 youtube_mp3_cli.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Example Session

```bash
$ python3 youtube_mp3_cli.py
============================================================
YouTube to MP3 Converter (Command Line)
============================================================

Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Download folder (press Enter for default):
[/Users/yourname/Music/YouTube Downloads]:

Downloading from: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Saving to: /Users/yourname/Music/YouTube Downloads

[download] 100% of 3.50MiB in 00:02
[ffmpeg] Correcting container in "Rick Astley - Never Gonna Give You Up.webm"
[ffmpeg] Destination: Rick Astley - Never Gonna Give You Up.mp3

✓ Successfully downloaded and converted: Rick Astley - Never Gonna Give You Up
✓ Saved to: /Users/yourname/Music/YouTube Downloads
```

---

## Configuration

- **Default download location:** `~/Music/YouTube Downloads`
- **MP3 quality:** 192kbps (good balance of quality and file size)
- **Output filename:** Based on video title

---

## Troubleshooting

### Installation Issues

**"externally-managed-environment" error**
```bash
pip3 install --break-system-packages -r requirements.txt
```
This is a modern macOS security feature. The flag is safe for installing app dependencies.

**"brew: command not found"**
- Homebrew isn't installed or not in PATH
- Install Homebrew (see Step 1)
- Make sure you ran the PATH commands after installation

**"pip3: command not found"**
```bash
brew install python3
```
Close and reopen Terminal after installation.

**"Could not find a version that satisfies the requirement yt-dlp"**
- Your Python version is too old (need 3.8+)
- Upgrade Python: `brew upgrade python3`
- Verify: `python3 --version`

### Runtime Issues

**"No module named 'yt_dlp'"**
```bash
pip3 install --break-system-packages yt-dlp
```

**"FFmpeg not found"**
```bash
brew install ffmpeg
```

**"Node.js runtime not found" or "n challenge solving failed"**
```bash
brew install node
```
Node.js is required to bypass YouTube's anti-bot protections.

**Download fails or video unavailable**
- Verify the URL is correct
- Check your internet connection
- Some videos may be age-restricted or region-locked
- Try updating yt-dlp: `pip3 install --break-system-packages --upgrade yt-dlp`
- Ensure Node.js is installed: `node --version`

---

## Legal Notice

This tool is for personal use only. Respect copyright laws and YouTube's Terms of Service. Only download content you have permission to download or that is in the public domain.

---

## Project Structure

```
youtube-mp3-converter/
├── youtube_mp3_cli.py      # Main application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```
