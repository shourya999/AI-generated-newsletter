import feedparser
import pandas as pd
from datetime import datetime, timedelta
import re
import time
import requests
# Use a timeout for all requests to avoid hanging
TIMEOUT = 10
# RSS Feed URLs - organized by category with more entertainment sources
RSS_FEEDS = {
    "General News": [
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://www.reutersagency.com/feed/?best-regions=europe&post_type=best"
    ],
    "Technology": [
        "https://feeds.feedburner.com/TechCrunch",
        "https://www.wired.com/feed/rss",
        "https://www.theverge.com/rss/index.xml"
    ],
    "Finance": [
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "https://www.ft.com/rss/home"
    ],
    "Sports": [
        "https://www.espn.com/espn/rss/news",
        "https://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.skysports.com/rss/12040"
    ],
    "Entertainment": [
        "https://variety.com/feed/",
        "https://www.hollywoodreporter.com/feed/",
        "https://www.billboard.com/feed/",
        "https://www.rollingstone.com/feed/",
        "https://ew.com/feed/",
        "https://www.cinemablend.com/rss/topic/news/movies"
    ],
    "Science": [
        "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "https://www.sciencedaily.com/rss/all.xml",
        "https://arstechnica.com/science/feed/"
    ]
}
def clean_html(raw_html):
    """Remove HTML tags from text."""
    clean_regex = re.compile('<.*?>')
    clean_text = re.sub(clean_regex, '', raw_html)
    # Also remove multiple spaces and newlines
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text
def check_url_availability(url):
    """Check if a URL is available and reachable."""
    try:
        response = requests.head(url, timeout=TIMEOUT)
        return response.status_code < 400  # Return True for successful status codes
    except Exception:
        return False
def parse_feed(feed_url, category):
    """Parse a single RSS feed and extract articles."""
    try:
        # First check if the URL is accessible
        if not check_url_availability(feed_url):
            print(f"URL not accessible: {feed_url}")
            return []
            
        feed = feedparser.parse(feed_url)
        
        # Handle error in parsing
        if not feed or not feed.entries:
            print(f"Error parsing feed or empty feed: {feed_url}")
            return []
        
        articles = []
        # Get source name from feed title or domain
        if hasattr(feed.feed, 'title') and feed.feed.title:
            source = feed.feed.title
        else:
            source = feed_url.split("/")[2]
        
        # Clean up source name
        source = source.replace('RSS Feed', '').strip()
        if ' - ' in source:
            source = source.split(' - ')[0].strip()
        
        for entry in feed.entries[:10]:  # Limit to 10 articles per feed
            try:
                # Extract publication date
                published = None
                for date_attr in ['published_parsed', 'updated_parsed', 'created_parsed']:
                    if hasattr(entry, date_attr) and getattr(entry, date_attr):
                        published = datetime(*getattr(entry, date_attr)[:6])
                        break
                
                # If no date found, use current time
                if not published:
                    published = datetime.now()
                
                # Extract article content
                content = ""
                # Try different content fields
                if hasattr(entry, 'content') and entry.content:
                    content = entry.content[0].value
                elif hasattr(entry, 'summary'):
                    content = entry.summary
                elif hasattr(entry, 'description'):
                    content = entry.description
                else:
                    content = ""
                
                # Clean content
                content = clean_html(content)
                
                # Ensure minimum content length
                if not content or len(content) < 50:
                    content = f"This is an article from {source} about {entry.title}."
                
                # Get the URL
                link = entry.link if hasattr(entry, 'link') else None
                if not link:
                    continue
                
                article = {
                    "title": entry.title if hasattr(entry, 'title') else "Untitled Article",
                    "link": link,
                    "published": published,
                    "content": content,
                    "source": source,
                    "feed_category": category,
                    "categories": []  # Will be filled by the categorizer
                }
                
                articles.append(article)
            except Exception as e:
                print(f"Error processing entry in {feed_url}: {str(e)}")
                continue
            
        return articles
    
    except Exception as e:
        print(f"Error parsing feed {feed_url}: {str(e)}")
        return []
def fetch_rss_feeds():
    """Fetch articles from all RSS feeds."""
    all_articles = []
    
    for category, feed_urls in RSS_FEEDS.items():
        category_articles = []
        for feed_url in feed_urls:
            # Add a small delay to avoid hammering servers
            time.sleep(0.3)
            articles = parse_feed(feed_url, category)
            category_articles.extend(articles)
            
        all_articles.extend(category_articles)
    
    # Sort all articles by publication date (newest first)
    all_articles.sort(key=lambda x: x["published"], reverse=True)
    
    return all_articles
