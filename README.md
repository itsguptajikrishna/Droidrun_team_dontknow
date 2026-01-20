# Droidrun_team_dontknow
📖 Overview
This project is an autonomous agent system designed to automate the entire lifecycle of social media content creation. Using DroidRun for mobile automation and Google Gemini for reasoning, the system scrapes global news sources, identifies high-impact trends, gathers multimedia assets, and publishes verified posts directly to the X (formerly Twitter) mobile app.

It solves the problem of manual content curation by creating a "human-like" agent that navigates real apps and websites to keep social feeds active with relevant, trending news.

🚀 Key Features
Modular News Scraping: targeted scraping of headlines from major sources (X, BBC, Reuters) using mobile browser automation.

AI Trend Analysis: Uses Gemini to synthesize cross-platform data and identify the single most relevant viral topic.

Automated Asset Collection: autonomously navigates Google Images to download relevant media and extract detailed summaries.

Smart Validation: Includes self-healing logic that verifies if a page loaded or an image was downloaded before proceeding.

Mobile UI Posting: Interacts directly with the X Android app to compose tweets, attach images from the gallery, and publish.

🛠️ Tech Stack
Language: Python 3.8+

Core API: DroidRun API (Mobile Automation)

Intelligence: Google Gemini 2.0 Flash (via DroidRun)

Platform: Android (Real Device or Emulator)

📋 Prerequisites
Before running the automation, ensure you have:

DroidRun API Key: A valid key to authenticate requests.

Device ID: The UUID of the connected Android device provided by DroidRun.

X (Twitter) App: Installed and logged in on the target Android device.

├── phase1_scrape.py       # Scrapes raw headlines from news sites
├── phase2_analyze.py      # AI selects the top trending topic
├── phase3_collect.py      # Downloads images & extracts summary text
├── phase4_post.py         # Posts content to X mobile app
├── data/
│   ├── trending_headings.json  # Raw scraped data
│   ├── selected_topic.txt      # The chosen trend
│   ├── topic_content.txt       # Generated post body
│   └── topic_links.txt         # Source URLs
└── README.md
