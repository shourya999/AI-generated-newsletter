import feedparser
import pandas as pd
from datetime import datetime, timedelta
import re
import time
import random
import requests

# Use a timeout for all requests to avoid hanging
TIMEOUT = 10

# Sample data to use when feeds are unavailable
SAMPLE_ARTICLE_DATA = {
    "General News": [
        {"title": "Global Climate Summit Reaches Historic Agreement", "content": "World leaders have agreed to a new climate treaty that will significantly reduce carbon emissions by 2030. The agreement includes financial aid for developing nations and stricter regulations for major polluters."},
        {"title": "New International Trade Deal Signed", "content": "A landmark trade agreement has been signed between 15 countries, creating one of the largest free trade zones in the world. Economists predict this will boost global GDP by at least 0.5% over the next five years."}
    ],
    "Technology": [
        {"title": "Tech Giant Unveils Revolutionary AI System", "content": "A leading technology company has announced a new artificial intelligence system that can solve complex problems faster than any previous model, with potential applications in healthcare, climate science, and quantum physics."},
        {"title": "Breakthrough in Quantum Computing Achieved", "content": "Scientists have demonstrated quantum supremacy in a new experiment that solved calculations impossible for traditional supercomputers. This development brings practical quantum computing applications closer to reality."}
    ],
    "Finance": [
        {"title": "Central Banks Announce Coordinated Rate Decision", "content": "Multiple central banks have announced a coordinated approach to interest rates in response to global inflation concerns. Markets responded positively to the rare show of international financial cooperation."},
        {"title": "Major Cryptocurrency Adoption by Banking Sector", "content": "Several international banks have announced plans to integrate cryptocurrency services into their traditional banking offerings, signaling a shift in mainstream financial acceptance of digital currencies."}
    ],
    "Sports": [
        {"title": "Underdog Team Wins Championship in Stunning Upset", "content": "In what analysts are calling one of the greatest upsets in sports history, the underdog team defeated the heavily favored champions with a last-minute play that will be remembered for years to come."},
        {"title": "Star Athlete Breaks Decades-Old World Record", "content": "A remarkable performance has resulted in breaking a world record that stood for over 30 years. Sports scientists are analyzing the techniques used to achieve this historic milestone."}
    ],
    "Entertainment": [
        {"title": "Indie Film Sweeps Major Awards Season", "content": "A low-budget independent film has won multiple prestigious awards, beating out big-studio productions. The director's unique storytelling approach has been praised for revolutionizing the genre."},
        {"title": "Streaming Platforms Announce Groundbreaking Content Partnership", "content": "Two major streaming services have announced a collaboration to produce a series of interconnected shows, representing the largest content investment in streaming history."}
    ],
    "Science": [
        {"title": "Researchers Discover Potential Cancer Treatment Breakthrough", "content": "Scientists have identified a new mechanism that could lead to more effective cancer treatments with fewer side effects. Early clinical trials show promising results across multiple types of previously resistant tumors."},
        {"title": "New Space Telescope Reveals Unprecedented Views of Deep Space", "content": "The newest space telescope has sent back its first images, showing previously unobservable celestial features. Astronomers say this will revolutionize our understanding of the early universe."}
    ]
}

# RSS Feed URLs - organized by category
RSS_FEEDS = {
    "General News": [
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://www.reutersagency.com/feed/?best-regions=europe&post_type=best"
    ],
    "Technology": [
        "https://techcrunch.com/feed/",
        "https://www.wired.com/feed/rss",
        "https://www.technologyreview.com/feed/"
    ],
    "Finance": [
        "https://www.bloomberg.com/feed/podcast/etf-report",
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
        "https://www.billboard.com/feed/"
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
            print(f"URL not accessible: {feed_url}, using sample data instead")
            return generate_sample_articles(category)
            
        feed = feedparser.parse(feed_url)
        
        # Handle error in parsing
        if not feed or not feed.entries:
            print(f"Error parsing feed: {feed_url}, using sample data instead")
            return generate_sample_articles(category)
        
        articles = []
        source = feed.feed.title if hasattr(feed.feed, 'title') else feed_url.split("/")[2]
        
        for entry in feed.entries[:10]:  # Limit to 10 articles per feed
            try:
                # Extract publication date
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                else:
                    published = datetime.now()
                
                # Extract article content
                if hasattr(entry, 'content') and entry.content:
                    content = entry.content[0].value
                elif hasattr(entry, 'summary'):
                    content = entry.summary
                else:
                    content = ""
                
                # Clean content
                content = clean_html(content)
                
                article = {
                    "title": entry.title,
                    "link": entry.link,
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
        
        if not articles:
            print(f"No articles found in feed: {feed_url}, using sample data instead")
            return generate_sample_articles(category)
            
        return articles
    
    except Exception as e:
        print(f"Error parsing feed {feed_url}: {str(e)}, using sample data instead")
        return generate_sample_articles(category)

def generate_sample_articles(category):
    """Generate sample articles when feeds are unavailable."""
    articles = []
    now = datetime.now()
    
    # Get sample data for this category
    if category in SAMPLE_ARTICLE_DATA:
        sample_data = SAMPLE_ARTICLE_DATA[category]
    else:
        # Use General News as fallback
        sample_data = SAMPLE_ARTICLE_DATA["General News"]
    
    for i, sample in enumerate(sample_data):
        # Create a sample article with realistic data
        source_domains = {
            "General News": ["bbc.com", "nytimes.com", "reuters.com"],
            "Technology": ["techcrunch.com", "wired.com", "technologyreview.com"],
            "Finance": ["bloomberg.com", "cnbc.com", "ft.com"],
            "Sports": ["espn.com", "bbc.co.uk/sport", "skysports.com"],
            "Entertainment": ["variety.com", "hollywoodreporter.com", "billboard.com"],
            "Science": ["nasa.gov", "sciencedaily.com", "arstechnica.com/science"]
        }
        
        # Get domain for the category or use a generic one
        domains = source_domains.get(category, ["example.com"])
        domain = random.choice(domains)
        
        # Generate a unique ID for the article link
        article_id = f"{int(time.time())}-{random.randint(1000, 9999)}-{i}"
        
        # Calculate a random date in the past few days
        days = random.randint(0, 3)
        hours = random.randint(0, 23)
        past_date = now - timedelta(days=days, hours=hours)
        
        article = {
            "title": sample["title"],
            "link": f"https://{domain}/article/{article_id}",
            "published": past_date,
            "content": sample["content"],
            "source": domain.split('.')[0].capitalize(),
            "feed_category": category,
            "categories": []  # Will be filled by the categorizer
        }
        
        articles.append(article)
    
    return articles

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
        
        # If we couldn't get any articles for a category, generate sample ones
        if not category_articles:
            sample_articles = generate_sample_articles(category)
            category_articles.extend(sample_articles)
            
        all_articles.extend(category_articles)
    
    # Make sure we have at least some articles
    if not all_articles:
        # Generate sample articles for all categories
        for category in RSS_FEEDS.keys():
            all_articles.extend(generate_sample_articles(category))
    
    # Sort all articles by publication date (newest first)
    all_articles.sort(key=lambda x: x["published"], reverse=True)
    
    return all_articles