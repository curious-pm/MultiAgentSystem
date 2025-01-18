import re
import yaml
import logging
from crewai import Agent, Task
from pathlib import Path

class URLExtractAgent:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self._create_agent()

    def _create_agent(self):
        """Create the URL extraction agent with config from YAML"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file).get('url_detector')
                if not config:
                    raise ValueError("No URL detector configuration found in YAML")
                
                self.agent = Agent(
                    role=config['role'],
                    goal=config['goal'],
                    backstory=config['backstory'],
                    llm=config['llm'],
                    verbose=True
                )
        except Exception as e:
            logging.error(f"Error creating URL extraction agent: {str(e)}")
            raise

    def _extract_urls(self, text: str) -> list:
        """Tool for extracting URLs from text"""
        logging.info("🔍 Searching for URLs in transcript...")
        url_pattern = r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)'
        urls = re.findall(url_pattern, text)
        unique_urls = list(set(urls))
        logging.info(f"✅ Found {len(unique_urls)} unique URLs")
        return unique_urls

    def task(self) -> Task:
        """Create a URL extraction task"""
        return Task(
            description='Extract all website URLs mentioned in the transcript',
            agent=self.agent,
            expected_output="List of unique URLs found in the transcript"
        )
