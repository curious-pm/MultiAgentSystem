from crewai import Agent, Task
import whisper
import yaml
import logging
from pathlib import Path

class TranscriptionAgent:
    def __init__(self, config_path: str | Path):
        self.model = whisper.load_model("base")
        self.config_path = Path(config_path)
        self._create_agent()

    def _create_agent(self):
        """Create the transcription agent with config from YAML"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file).get('transcriber')
                if not config:
                    raise ValueError("No transcriber configuration found in YAML")
                
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
        """Tool for transcribing audio"""
        logging.info("🎙️ Starting transcription...")
        try:
            result = self.model.transcribe(audio_path)
            logging.info("✅ Transcription complete")
            return result["text"]
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