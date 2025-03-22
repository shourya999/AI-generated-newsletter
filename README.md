# AI-Driven Newsletter System

An AI-powered personalized newsletter system that curates content from RSS feeds based on user preferences.

## Features

- Fetches articles from various RSS feeds categorized by topics
- Categorizes articles using natural language processing
- Filters content based on user interests and preferred sources
- Generates personalized newsletters in Markdown format
- Provides an intuitive Streamlit web interface

## How to Run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py --server.address 127.0.0.1 --server.port 8501`
4. Access the web interface at http://127.0.0.1:8501/

## User Personas

The system includes five predefined user personas with different interests:
- Tech enthusiast
- Finance professional
- Sports fan
- Entertainment buff
- Science researcher

## File Structure

- `app.py`: Main Streamlit application
- `article_categorizer.py`: Handles article categorization
- `article_summarizer.py`: Creates article summaries
- `newsletter_generator.py`: Generates newsletter in Markdown format
- `rss_parser.py`: Fetches and parses articles from RSS feeds
- `user_preferences.py`: User persona definitions
- `utils.py`: Utility functions
