from crewai import Crew, Process, Agent
from pathlib import Path
from datetime import datetime
import logging
import os
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up base directory
BASE_DIR = Path(__file__).parent
YAML_PATH = BASE_DIR / 'agents.yml'

# Import agents
from agents.transcribe_agent import TranscriptionAgent
from agents.extract_agent import URLExtractAgent
from agents.summarize_agent import WebsiteSummaryAgent
from agents.file_agent import FileGenerationAgent
from agents.podcastDownloaderAgent import PodcastDownloaderAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/process_{datetime.now().strftime("%Y%m%d_%H%M")}.log'),
        logging.StreamHandler()
    ]
)

def load_agent_configs():
    """Load agent configurations from YAML"""
    try:
        with open(YAML_PATH, 'r') as file:
            config = yaml.safe_load(file)
            logging.info(f"✅ Loaded agent configurations from {YAML_PATH}")
            return config
    except FileNotFoundError:
        logging.error(f"❌ Could not find agents.yml at {YAML_PATH}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"❌ Error parsing agents.yml: {str(e)}")
        raise

def setup_directories():
    """Create necessary directories if they don't exist"""
    Path("data/input").mkdir(parents=True, exist_ok=True)
    Path("data/output").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

def process_podcast(podcast_link: str):
    """Main function to orchestrate the podcast processing"""
    logging.info("\n\n🚀 Starting podcast processing pipeline\n")
    
    # Load agent configurations
    configs = load_agent_configs()
    logging.info("📝 Initializing agents with configurations...\n")
    
    # Initialize agents
    downloader_agent = PodcastDownloaderAgent(download_dir="data/input")
    transcription_agent = TranscriptionAgent(config_path=YAML_PATH)
    url_extract_agent = URLExtractAgent(config_path=YAML_PATH)
    website_summary_agent = WebsiteSummaryAgent(config_path=YAML_PATH)
    file_generation_agent = FileGenerationAgent(config_path=YAML_PATH)
    
    # Step 1: Download the podcast
    print("🔹 **Agent 1: Podcast Downloader**")
    print("Task: Downloading the podcast audio file...")
    podcast_path = downloader_agent._download_podcast(podcast_link)
    print("✅ Podcast downloaded successfully.\n")
    
    # Step 2: Transcribe the podcast
    print("🔹 **Agent 2: Podcast Transcriber**")
    print("Task: Transcribing the podcast audio file...")
    transcription_text = transcription_agent._transcribe_audio(podcast_path)
    print("✅ Podcast transcribed successfully.\n")
    
    # Step 3: Extract URLs from the transcription
    print("🔹 **Agent 3: URL Detective**")
    print("Task: Extracting URLs from the transcription...")
    urls = url_extract_agent._extract_urls(transcription_text)
    print("✅ URLs extracted successfully.\n")
    
    # Step 4: Analyze each URL
    print("🔹 **Agent 4: Website Analyzer**")
    print("Task: Analyzing the extracted URLs for brief descriptions...")
    analyzed_urls = [website_summary_agent._analyze_website(url) for url in urls]
    print("✅ URLs analyzed successfully.\n")
    
    # Step 5: Generate the report
    print("🔹 **Agent 5: Report Generator**")
    print("Task: Generating a structured report with URLs and descriptions...")
    report_path = file_generation_agent._generate_file(analyzed_urls)
    print("✅ Report generated successfully.\n")
    
    # Final structured output
    print("\n✨ **Processing Complete!**")
    print("📄 Final Output Summary:")
    print(f"- Total URLs Extracted: {len(urls)}")
    print(f"- Report Location: {report_path}\n")
    
    # Print report contents
    print("📄 **Report Contents**:\n")
    with open(report_path, 'r') as report_file:
        report_content = report_file.read()
        print(report_content)

    return report_path

if __name__ == "__main__":
    try:
        setup_directories()
        
        # Ask the user for the podcast link
        podcast_link = input("🔗 Please enter the podcast link (YouTube or direct MP3 link): ").strip()
        
        if not podcast_link:
            raise ValueError("❌ No podcast link provided. Please enter a valid URL.")
        
        # Process the podcast
        process_podcast(podcast_link)
        
    except Exception as e:
        logging.error(f"Failed to process podcast: {str(e)}")


