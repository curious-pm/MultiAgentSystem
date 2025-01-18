from crewai import Agent, Task
import requests
from bs4 import BeautifulSoup
import yaml
import logging
from pathlib import Path

class WebsiteSummaryAgent:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self._create_agent()

    def _create_agent(self):
        """Create the website summary agent with config from YAML"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file).get('website_analyzer')
                if not config:
                    raise ValueError("No website analyzer configuration found in YAML")
                
                self.agent = Agent(
                    role=config['role'],
                    goal=config['goal'],
                    backstory=config['backstory'],
                    llm=config['llm'],
                    verbose=True
                )
        except Exception as e:
            logging.error(f"Error creating website summary agent: {str(e)}")
            raise

    def _analyze_website(self, url: str) -> str:
        """Tool for analyzing websites and creating descriptions"""
        try:
            # Ensure URL is complete
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title and meta description
            title = soup.title.string.strip() if soup.title else ''
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'].strip() if meta_desc else ''
            
            # Use description or fallback to title
            summary = description or title
            return f"{url}: {summary[:150]}"  # Limit summary length
        except Exception:
            return f"{url}: Could not access website"

    def task(self) -> Task:
        """Create a website analysis task"""
        return Task(
            description='Analyze each website found and create a one-line description',
            agent=self.agent,
            expected_output="List of websites with their descriptions"
        )
