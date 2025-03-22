# AI-Driven Newsletter System

An AI-powered personalized newsletter system that curates content from RSS feeds based on user preferences.


## Project Overview

This AI-powered system automates news curation and delivery by:
- Fetching news articles from RSS feeds.
- Categorizing them using NLP-based classification.
- Summarizing content using AI-powered text processing.
- Generating a structured newsletter in Markdown format.
- Allowing users to select preferences and receive personalized news.

Built using: 🐍 Python | ⚡ Streamlit | 📡 RSS Feeds | 🧠 NLP (NLTK, newspaper3k)


## Features

Real-time News Fetching – Retrieves the latest articles from sources like BBC, TechCrunch, Bloomberg, ESPN, NASA.
- NLP-Based Categorization – Assigns articles to Technology, Business, Science, Sports, Entertainment, etc.
- AI-Powered Summarization – Uses newspaper3k & NLTK for concise summaries.
- Personalized Filtering – Matches articles with user-specific interests.
- Streamlit UI – Interactive web-based interface for easy access.
- Automated Markdown Newsletter – Well-formatted, easy-to-read news summaries.


## User Personas

The system includes five predefined user personas with different interests:
 1. Alex Parker (Tech Enthusiast, 28, USA)
 • Interests: AI, cybersecurity, blockchain, startups, programming
 •  Sources: TechCrunch, Wired Tech, Ars Technica, MIT Tech Review

 2. Priya Sharma (Finance & Business Guru, 35, India)
 • Interests: Global markets, startups, fintech, cryptocurrency, economics
 • Sources: Bloomberg, Financial Times, Forbes, CoinDesk

 3. Marco Rossi (Sports Journalist, 30, Italy)
 • Interests: Football, F1, NBA, Olympic sports, esports
 • Sources: ESPN, BBC Sport, Sky Sports F1, The Athletic
 
 4. Lisa Thompson (Entertainment Buff, 24, UK)
 • Interests: Movies, celebrity news, TV shows, music, books
 • Sources: Variety, Rolling Stone, Billboard, Hollywood Reporter

 5. David Martinez (Science & Space Nerd, 40, Spain)
 • Interests: Space exploration, AI, biotech, physics, renewable energy
 •  Sources: NASA, Science Daily, Nature, Ars Technica Science

  
## File Structure

ai-newsletter-generator/

├── .streamlit/
│ 
└── config.toml # Streamlit configuration

├── app.py # Main Streamlit application

├── article_categorizer.py # Article categorization using NLP

├── article_summarizer.py # Article summarization

├── newsletter_generator.py # Newsletter generation

├── rss_parser.py # RSS feed parser

├── user_preferences.py # User personas

├── utils.py # Utility functions

└── requirements.txt # Dependencies


## File Functions

- `app.py`: Main Streamlit application
- `article_categorizer.py`: Handles article categorization
- `article_summarizer.py`: Creates article summaries
- `newsletter_generator.py`: Generates newsletter in Markdown format
- `rss_parser.py`: Fetches and parses articles from RSS feeds
- `user_preferences.py`: User persona definitions
- `utils.py`: Utility functions


## How to Run

1. Clone the repository: `git clone https://github.com/shourya999/AI-generated-newsletter.git
cd AI-generated-newsletter`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py --server.address 127.0.0.1 --server.port 8501`
4. Access the web interface at http://127.0.0.1:8501/
5. Select User Persona & Preferences: Choose a user profile from the sidebar (e.g., Tech Enthusiast, Finance Guru).
The system will fetch, analyze, and generate a personalized newsletter.
6. Download Your Newsletter: Once generated, you can preview & download the Markdown file.









