from crewai import Agent, Task
from datetime import datetime
from pathlib import Path
import yaml
import logging

class FileGenerationAgent:
    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self._create_agent()

    def _create_agent(self):
        """Create the file generation agent with config from YAML"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file).get('report_generator')
                if not config:
                    raise ValueError("No report generator configuration found in YAML")
                
                self.agent = Agent(
                    role=config['role'],
                    goal=config['goal'],
                    backstory=config['backstory'],
                    llm=config['llm'],
                    verbose=True
                )
        except Exception as e:
            logging.error(f"Error creating file generation agent: {str(e)}")
            raise

    def _generate_file(self, content: list) -> str:
        """Tool for generating the final report file"""
        logging.info("📝 Generating report file...")
        
        output_dir = Path("data/output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = output_dir / f"podcast_urls_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        report = "# Website References from Podcast\n\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for item in content:
            report += f"- {item}\n"
        
        with open(filename, 'w') as f:
            f.write(report)
        
        logging.info(f"✅ Report saved to: {filename}")
        return str(filename)

    def task(self) -> Task:
        """Create a file generation task"""
        return Task(
            description='Create a markdown file containing all URLs and their descriptions',
            agent=self.agent,
            expected_output="Path to the generated markdown report file"
        )
