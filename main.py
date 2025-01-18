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

def process_podcast(audio_path: str):
    """Main function to orchestrate the podcast processing"""
    logging.info("🚀 Starting podcast processing pipeline")
    
    # Validate audio file exists
    if not Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Load agent configurations
    configs = load_agent_configs()
    logging.info("📝 Initializing agents with configurations...")
    
    # Initialize agents
    transcription_agent = TranscriptionAgent(config_path=YAML_PATH)
    url_extract_agent = URLExtractAgent(config_path=YAML_PATH)
    website_summary_agent = WebsiteSummaryAgent(config_path=YAML_PATH)
    file_generation_agent = FileGenerationAgent(config_path=YAML_PATH)
    
    # Create tasks
    tasks = [
        transcription_agent.task(audio_path),
        url_extract_agent.task(),
        website_summary_agent.task(),
        file_generation_agent.task()
    ]
    
    # Create crew
    crew = Crew(
        tasks=tasks,
        agents=[
            transcription_agent.agent,
            url_extract_agent.agent,
            website_summary_agent.agent,
            file_generation_agent.agent
        ],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute the crew's tasks
        result = crew.kickoff()
        logging.info("✨ Processing complete!")
        return result
    except Exception as e:
        logging.error(f"❌ Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        setup_directories()
        
        # Audio file path
        audio_file = "data/input/videoplayback.mp3"
        
        # Process the podcast
        result = process_podcast(audio_file)
        
        # Print the final result
        print("\n🎉 Final Result:")
        print(result)
        
    except Exception as e:
        logging.error(f"Failed to process podcast: {str(e)}")