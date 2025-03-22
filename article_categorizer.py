import re
import string
# Core categories for article classification with enhanced entertainment keywords
CATEGORIES = {
    "Technology": [
        "technology", "tech", "software", "hardware", "app", "computer", "programming",
        "ai", "artificial intelligence", "machine learning", "data", "cyber", "digital",
        "internet", "web", "mobile", "device", "smartphone", "code", "blockchain", "bitcoin"
    ],
    "Business": [
        "business", "company", "corporate", "market", "economy", "finance", "stock",
        "investment", "trade", "startup", "venture", "entrepreneur", "industry",
        "retail", "revenue", "profit", "growth", "commercial", "enterprise", "consumer"
    ],
    "Politics": [
        "politics", "government", "election", "vote", "political", "policy", 
        "congress", "senate", "president", "law", "legislation", "court", "democrat",
        "republican", "parliament", "minister", "diplomat", "foreign", "domestic"
    ],
    "Health": [
        "health", "medical", "medicine", "doctor", "disease", "patient", "treatment",
        "hospital", "drug", "virus", "vaccine", "diet", "fitness", "nutrition",
        "mental health", "wellness", "therapy", "pandemic", "covid", "healthcare"
    ],
    "Science": [
        "science", "scientific", "research", "study", "discovery", "physics", "biology",
        "chemistry", "space", "earth", "climate", "environment", "energy", "nasa",
        "experiment", "laboratory", "gene", "species", "evolution", "astronomy"
    ],
    "Entertainment": [
        "entertainment", "movie", "film", "cinema", "music", "celebrity", "hollywood", 
        "actor", "actress", "director", "show", "television", "tv", "streaming", "concert",
        "performance", "award", "drama", "comedy", "series", "theater", "book", "novel", 
        "author", "star", "song", "album", "artist", "band", "release", "singer", "netflix",
        "disney", "hbo", "amazon prime", "blockbuster", "box office", "hit", "billboard",
        "magazine", "fashion", "style", "red carpet", "premiere", "trailer", "review",
        "critic", "broadway", "musical", "festival"
    ],
    "Sports": [
        "sport", "sports", "game", "match", "team", "player", "athlete", "championship",
        "tournament", "football", "soccer", "basketball", "baseball", "tennis", "golf",
        "olympics", "league", "coach", "stadium", "score", "win", "race", "racing"
    ]
}
def preprocess_text(text):
    """Preprocess text for categorization."""
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
def categorize_article(article):
    """Categorize a single article based on title and content."""
    # Create a copy of the article to avoid modifying the original
    article_copy = dict(article)
    
    # Get the text to analyze (title + content)
    title = article_copy.get("title", "")
    content = article_copy.get("content", "")
    text = title + " " + content
    
    # Use feed category as a fallback
    feed_category = article_copy.get("feed_category", "")
    
    # Preprocess the text
    preprocessed_text = preprocess_text(text)
    
    # Count category keyword occurrences
    category_scores = {}
    
    for category, keywords in CATEGORIES.items():
        score = 0
        for keyword in keywords:
            # Count occurrences of the keyword
            keyword_count = preprocessed_text.count(keyword)
            
            # Add to score (with title matches weighted higher)
            if title and keyword in preprocess_text(title):
                score += 5 * keyword_count  # Title match is weighted higher
            else:
                score += keyword_count
        
        if score > 0:
            category_scores[category] = score
    
    # Also consider the feed category (if available)
    if feed_category:
        # Look for matching or similar category
        matching_category = None
        for category in category_scores.keys():
            if feed_category.lower() in category.lower() or category.lower() in feed_category.lower():
                category_scores[category] += 3  # Boost the score
                matching_category = category
        
        # If feed category doesn't match any existing category, add it as a separate category
        if not matching_category and feed_category not in category_scores:
            category_scores[feed_category] = 2  # Base score for feed category
    
    # Sort categories by score (descending)
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Keep only the top categories (those with significant scores)
    top_categories = [category for category, score in sorted_categories if score >= 2]
    
    # If no categories found, add the feed category or "General"
    if not top_categories:
        if feed_category:
            top_categories = [feed_category]
        else:
            top_categories = ["General"]
    
    # Ensure Entertainment gets priority for entertainment sources
    if feed_category == "Entertainment" and "Entertainment" not in top_categories:
        top_categories.insert(0, "Entertainment")
    
    # Limit to top 3 categories
    article_copy["categories"] = top_categories[:3]
    
    return article_copy
def categorize_articles(articles):
    """Categorize all articles."""
    categorized = []
    for article in articles:
        try:
            categorized_article = categorize_article(article)
            categorized.append(categorized_article)
        except Exception as e:
            # If categorization fails, just add the original article
            if "categories" not in article:
                article["categories"] = [article.get("feed_category", "General")]
            categorized.append(article)
    
    return categorized
