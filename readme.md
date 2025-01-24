[Join Idealabs Community](https://curios.pm) to connect, share, and learn with others!

# Podcast URL Extractor
This project automates the process of extracting website URLs mentioned in podcast episodes. It leverages AI-powered agents to download, transcribe, analyze, and generate structured reports from podcast audio files.

---

## What the Code Does

The code orchestrates a multi-step pipeline to process a podcast URL and extract valuable insights. It uses AI-driven agents to:

- **Download the podcast audio file** from a provided link.
- **Transcribe the audio** into text.
- **Extract website URLs** mentioned in the podcast.
- **Analyze the extracted URLs**, providing a brief summary for each.
- **Generate a report** containing the extracted URLs and their descriptions.

### Features

- **Automated Workflow:** Seamless orchestration from download to report generation.
- **Error Handling:** Provides descriptive logs and messages.
- **Modular Agents:** Easily extendable to add new functionalities.
- **Efficient Processing:** Handles large audio files with minimal CPU usage.
- **Customizable Pipeline:** Modify individual agent configurations for specific needs.

---

## How to Use It (Step by Step)

### 1. Install Dependencies
Ensure Python is installed, then install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory and add necessary API credentials:

```
API_KEY=your_api_key_here
```

### 3. Run the Application
Execute the main script to start processing the podcast:

```bash
python main.py
```

### 4. Enter Podcast Link
When prompted, enter a valid podcast link (YouTube or direct MP3 link):

```
🔗 Please enter the podcast link: https://example.com/podcast.mp3
```

### 5. View the Output
- The extracted URLs and their summaries will be displayed on the console.
- A report will be saved in the `data/output/` directory.

---


## What Happens in Each Step

1. **Podcast Downloading:**
   - Downloads the podcast from the provided link.
   - Saves the audio file in `data/input/`.

2. **Transcription:**
   - Converts the audio content into text.
   - Stores the transcription for further processing.

3. **URL Extraction:**
   - Identifies and extracts URLs mentioned in the transcription.

4. **Website Analysis:**
   - Summarizes the content of each extracted URL.

5. **Report Generation:**
   - Creates a markdown file with URLs and their descriptions.

---

## Understanding Agents

In this project, agents are modular components that handle specific tasks in the podcast processing workflow. Each agent encapsulates logic for:

- **PodcastDownloaderAgent:** Downloads audio files from URLs.
- **TranscriptionAgent:** Converts audio files into text using AI models.
- **URLExtractAgent:** Extracts URLs from transcribed text.
- **WebsiteSummaryAgent:** Analyzes and summarizes extracted URLs.
- **FileGenerationAgent:** Compiles the extracted information into a report.

Each agent operates independently but works in harmony within the `CrewAI` framework.

---

## Folder Structure

```
ai_agent_podcast-url-extractor/
├── agents/
│   ├── extract_agent.py       # Extracts URLs from transcriptions
│   ├── file_agent.py          # Generates reports with extracted URLs
│   ├── podcastDownloaderAgent.py  # Downloads podcast audio files
│   ├── summarize_agent.py     # Summarizes extracted URLs
│   └── transcribe_agent.py    # Transcribes audio files
├── data/
│   ├── input/                 # Stores downloaded podcast files
│   └── output/                # Contains generated reports
├── logs/                      # Logs processing activities
├── main.py                    # Orchestrates the entire workflow
├── agents.yml                 # Configuration for agent behavior
├── requirements.txt           # Dependencies for the project
└── .env                        # Environment variables and API keys
```
## Explanation of Each File

- **`main.py`** - The primary script that orchestrates the entire processing workflow by coordinating all agents and logging events.
- **`agents/` directory**
  - `extract_agent.py` - Handles the extraction of URLs from the transcribed text.
  - `file_agent.py` - Generates structured reports containing URLs and descriptions.
  - `podcastDownloaderAgent.py` - Downloads podcast audio files from the provided URLs.
  - `summarize_agent.py` - Analyzes and summarizes the extracted URLs to provide meaningful descriptions.
  - `transcribe_agent.py` - Converts the podcast audio files into text format.
- **`agents.yml`** - Configuration file that defines the operational parameters for each agent.
- **`data/` directory**
  - `input/` - Stores downloaded podcast audio files.
  - `output/` - Contains reports generated from the extracted data.
- **`logs/` directory** - Stores log files for monitoring and debugging the processing steps.
- **`requirements.txt`** - Lists all dependencies required to run the project.
- **`.env`** - Stores environment variables securely, including API keys and configuration details.

---

## Expected Output Example

**Input:**
```
🔗 Please enter the podcast link: https://example.com/podcast.mp3
```

**Output:**
```
✅ Podcast downloaded successfully.
✅ Podcast transcribed successfully.
✅ URLs extracted successfully.
📄 Report Location: data/output/podcast_urls_20250121_1819.md
```

---

## Common Issues & Troubleshooting

1. **Invalid Podcast Link:**
   - Ensure the provided link is accessible and points to a valid audio file.

2. **Missing Dependencies:**
   - Install missing packages using `pip install -r requirements.txt`.

3. **Permission Errors:**
   - Ensure write permissions for `data/output/` and `logs/` directories.

---

## Security Considerations

- Store credentials securely in the `.env` file.
- Do not share private API keys publicly.
- Regularly rotate API keys for security.

---

## Link to Hosted Version
[View Live App](#) *(Insert actual deployment link here)*


---

## Screenshots

1. **Console Output:**  
   ![Image](https://github.com/user-attachments/assets/ef9c5844-c0f0-450f-8c07-f0921c4b3593)

2. **Generated Report:**  
   ![Image](https://github.com/user-attachments/assets/cc947271-29e1-4579-a001-500fc1866536)

---

## Video Overview
*A short video walkthrough will be provided explaining the app's features and usage.*

