from crewai import Agent, Task
from yt_dlp import YoutubeDL
from pathlib import Path
import logging


class PodcastDownloaderAgent:
    def __init__(self, download_dir: str):
        """Initialize the Podcast Downloader Agent"""
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

        # Initialize the Agent object
        self.agent = Agent(
            role="Podcast Downloader",
            goal="Download the podcast audio file from the provided link",
            backstory="Handles downloading from YouTube and direct links",
            llm="azure/gpt-4o",
            verbose=True
        )

    def _download_podcast(self, link: str) -> str:
        """Download podcast from YouTube or other supported links using yt-dlp"""
        logging.info(f"🌐 Downloading podcast from: {link}")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{self.download_dir}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'nocheckcertificate': True,  # Bypass SSL certificate checks
                'quiet': True,  # Enable verbose logs for debugging
                'no_warnings': True,  # Suppress warnings

            }
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                file_path = f"{self.download_dir}/{info_dict['title']}.mp3"
            logging.info(f"✅ Podcast downloaded to: {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"❌ Failed to download podcast: {str(e)}")
            raise

    def task(self, link: str) -> Task:
        """Create a download task"""
        return Task(
            description=f"Download the podcast from the link {link}",
            agent=self.agent,
            expected_output="Path to the downloaded podcast file"
        )
