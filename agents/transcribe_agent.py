from crewai import Agent, Task
import whisper
import yaml
import logging
from pathlib import Path


class TranscriptionAgent:
    def __init__(self, config_path: str | Path):
        """Initialize the Transcription Agent"""
        self.model = whisper.load_model("base")  # Load the Whisper model
        self.config_path = Path(config_path)
        self._create_agent()

    def _create_agent(self):
        """Create the transcription agent using configuration from YAML"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file).get('transcriber')
                if not config:
                    raise ValueError("No transcriber configuration found in YAML")
                
                # Initialize the Agent
                self.agent = Agent(
                    role=config['role'],
                    goal=config['goal'],
                    backstory=config['backstory'],
                    llm=config['llm'],
                    verbose=True
                )
        except Exception as e:
            logging.error(f"Error creating transcription agent: {str(e)}")
            raise

    def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe the audio file using Whisper"""
        logging.info(f"🎙️ Starting transcription for file: {audio_path}")
        try:
            # Perform transcription
            result = self.model.transcribe(audio_path)
            transcription = result["text"]
            logging.info("✅ Transcription complete")
            return transcription
        except Exception as e:
            logging.error(f"❌ Transcription failed: {str(e)}")
            raise

    def task(self, audio_path: str) -> Task:
        """Create a transcription task"""
        return Task(
            description=f"Transcribe the podcast at {audio_path} to text",
            agent=self.agent,
            expected_output="Complete text transcription of the audio file"
        )
