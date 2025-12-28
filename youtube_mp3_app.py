#!/usr/bin/env python3
"""
YouTube to MP3 Converter for macOS
Downloads audio from YouTube/YouTube Music and converts to MP3
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import threading
from pathlib import Path


class YouTubeMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to MP3 Converter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Set default download location to Music folder
        self.download_path = str(Path.home() / "Music" / "YouTube Downloads")
        os.makedirs(self.download_path, exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame,
            text="YouTube to MP3 Converter",
            font=("Helvetica", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # URL input
        url_label = ttk.Label(main_frame, text="YouTube URL:")
        url_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        # Download location
        location_label = ttk.Label(main_frame, text="Download Location:")
        location_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        location_frame = ttk.Frame(main_frame)
        location_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        self.location_label = ttk.Label(
            location_frame,
            text=self.download_path,
            relief="sunken",
            padding=5
        )
        self.location_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_btn = ttk.Button(
            location_frame,
            text="Browse...",
            command=self.browse_location
        )
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to download",
            foreground="gray"
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(0, 15))

        # Download button
        self.download_btn = ttk.Button(
            main_frame,
            text="Download & Convert to MP3",
            command=self.start_download
        )
        self.download_btn.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def browse_location(self):
        """Open dialog to select download location"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.location_label.config(text=folder)

    def progress_hook(self, d):
        """Callback for download progress"""
        if d['status'] == 'downloading':
            # Extract percentage from the progress string
            percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
            try:
                percent = float(percent_str)
                self.progress_var.set(percent)
                self.status_label.config(
                    text=f"Downloading: {percent:.1f}%",
                    foreground="blue"
                )
            except ValueError:
                pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_label.config(
                text="Converting to MP3...",
                foreground="green"
            )

    def download_audio(self):
        """Download and convert YouTube audio to MP3"""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        # Disable download button during download
        self.download_btn.config(state="disabled")
        self.progress_var.set(0)

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': False,
            'no_warnings': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_label.config(
                    text="Fetching video information...",
                    foreground="blue"
                )
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')

            self.progress_var.set(100)
            self.status_label.config(
                text=f"Successfully downloaded: {title}",
                foreground="green"
            )
            messagebox.showinfo(
                "Success",
                f"Successfully converted to MP3!\n\nSaved to:\n{self.download_path}"
            )

        except Exception as e:
            self.status_label.config(
                text="Download failed",
                foreground="red"
            )
            messagebox.showerror("Error", f"Failed to download:\n{str(e)}")

        finally:
            # Re-enable download button
            self.download_btn.config(state="normal")
            self.progress_var.set(0)

    def start_download(self):
        """Start download in a separate thread"""
        thread = threading.Thread(target=self.download_audio, daemon=True)
        thread.start()


def main():
    root = tk.Tk()
    app = YouTubeMP3Converter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
