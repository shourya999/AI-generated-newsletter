import newspaper
import nltk
from newspaper import Article
import time

# Download the necessary NLTK data if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

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
        # Create a newspaper Article object
        article = Article(result["link"])
        
        # Download and parse the article
        article.download()
        
        # Small delay to avoid hitting rate limits
        time.sleep(0.1)
        
        article.parse()
        
        # Try to use NLP to summarize
        try:
            article.nlp()
            summary = article.summary
            
            # If summary is too short or empty, use the first few sentences of the content
            if len(summary) < 100:
                # Use the first 2-3 sentences from the content
                sentences = nltk.sent_tokenize(result["content"])
                if sentences:
                    summary = " ".join(sentences[:3])
        except Exception:
            # If NLP fails, use the first few sentences of the content
            sentences = nltk.sent_tokenize(result["content"])
            if sentences:
                summary = " ".join(sentences[:3])
            else:
                summary = result["content"][:300] + "..."
                
        # If summary is still empty or too short, use the original content
        if not summary or len(summary) < 50:
            if len(result["content"]) > 300:
                summary = result["content"][:300] + "..."
            else:
                summary = result["content"]
                
        # Add the summary to the article data
        result["summary"] = summary
        
    except Exception as e:
        # If there's an error, use the content as the summary
        if len(result["content"]) > 300:
            result["summary"] = result["content"][:300] + "..."
        else:
            result["summary"] = result["content"]
    
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