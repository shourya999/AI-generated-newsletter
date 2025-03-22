import newspaper
import nltk
from newspaper import Article
import time
import re

# Initialize NLTK 
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def clean_summary(text):
    """Clean and format the summary text."""
    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Ensure the summary ends with proper punctuation
    if text and not text[-1] in ['.', '!', '?']:
        text += '.'
        
    return text

def summarize_article(article_data):
    """
    Summarize an article using the newspaper3k library.
    
    Args:
        article_data: Dict containing article information including 'link'
        
    Returns:
        Updated article_data with summary field added
    """
    # Create a copy of the article data to avoid modifying the original
    result = dict(article_data)
    
    try:
        # Only attempt to summarize if we have a valid URL
        if not result.get("link"):
            result["summary"] = result.get("content", "")[:250] + "..."
            return result
            
        # Create a newspaper Article object
        article = Article(result["link"])
        
        # Configure article download
        article.config.browser_user_agent = 'Mozilla/5.0'
        article.config.request_timeout = 10
        
        # Download and parse the article
        article.download()
        time.sleep(0.2)  # Small delay to avoid hitting rate limits
        article.parse()
        
        # Try to use NLP to summarize
        try:
            article.nlp()
            summary = article.summary
            
            # If summary is too short or empty, use the first few sentences of the content
            if len(summary) < 100:
                # Use the first 2-3 sentences from the content
                sentences = nltk.sent_tokenize(result["content"])
                if sentences and len(sentences) >= 3:
                    summary = " ".join(sentences[:3])
                elif sentences:
                    summary = " ".join(sentences)
                else:
                    summary = result["content"][:250] + "..."
        except Exception:
            # If NLP fails, use the first few sentences of the content
            sentences = nltk.sent_tokenize(result["content"])
            if sentences and len(sentences) >= 3:
                summary = " ".join(sentences[:3])
            elif sentences:
                summary = " ".join(sentences)
            else:
                summary = result["content"][:250] + "..."
                
        # Clean and format the summary
        summary = clean_summary(summary)
                
        # If summary is still empty or too short, use the original content
        if not summary or len(summary) < 50:
            if len(result["content"]) > 250:
                summary = result["content"][:250] + "..."
            else:
                summary = result["content"]
                
        # Add the summary to the article data
        result["summary"] = summary
        
    except Exception:
        # If there's an error, use the content as the summary
        content = result.get("content", "")
        if content and len(content) > 250:
            result["summary"] = content[:250] + "..."
        else:
            result["summary"] = content
    
    return result

def summarize_articles(articles):
    """
    Summarize a list of articles.
    
    Args:
        articles: List of article dictionaries
        
    Returns:
        List of articles with summaries added
    """
    summarized = []
    for article in articles:
        summarized_article = summarize_article(article)
        summarized.append(summarized_article)
    
    return summarized
