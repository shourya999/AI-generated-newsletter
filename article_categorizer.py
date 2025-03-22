import re
import string
from collections import Counter

# Core categories for article classification
CATEGORIES = {
    "Technology": [
        "ai", "artificial intelligence", "machine learning", "deep learning",
        "technology", "software", "hardware", "app", "application", "computer", 
        "computing", "code", "programming", "developer", "tech", "algorithm",
        "data science", "robotics", "automation", "cyber", "digital",
        "gadget", "internet", "web", "mobile", "smartphone", "app",
        "database", "cloud", "server", "network", "iot", "startup",
        "innovation", "blockchain", "cryptocurrency", "bitcoin", "ethereum",
        "vr", "ar", "virtual reality", "augmented reality"
    ],
    "Business": [
        "business", "company", "corporate", "industry", "market", "economy", 
        "economic", "finance", "financial", "stock", "investment", "investor",
        "trade", "trading", "commerce", "commercial", "venture", "enterprise",
        "entrepreneur", "startup", "corporation", "firm", "merger", "acquisition",
        "ipo", "revenue", "profit", "earnings", "quarterly", "fiscal", "ceo",
        "executive", "management", "strategy", "growth", "expansion"
    ],
    "Politics": [
        "politics", "government", "election", "campaign", "vote", "voter", 
        "political", "policy", "law", "regulation", "senate", "congress",
        "parliament", "democrat", "republican", "conservative", "liberal",
        "progressive", "politician", "president", "minister", "governor",
        "mayor", "legislation", "bill", "act", "constitution", "court",
        "justice", "supreme court", "ruling", "diplomacy", "diplomatic",
        "international relations", "foreign policy", "domestic policy"
    ],
    "Health": [
        "health", "medical", "medicine", "doctor", "hospital", "patient", 
        "disease", "condition", "treatment", "symptom", "diagnosis", "therapy",
        "drug", "pharmaceutical", "biotech", "vaccine", "vaccination", "virus",
        "epidemic", "pandemic", "public health", "healthcare", "wellness",
        "mental health", "psychology", "psychiatry", "diet", "nutrition",
        "exercise", "fitness", "obesity", "cancer", "diabetes", "research"
    ],
    "Science": [
        "science", "scientific", "research", "study", "discovery", "laboratory", 
        "experiment", "physics", "chemistry", "biology", "astronomy", "space",
        "earth", "environment", "climate", "weather", "planet", "solar system",
        "universe", "cosmos", "quantum", "particle", "molecule", "atom",
        "gene", "genetic", "evolution", "species", "biodiversity", "ecosystem",
        "sustainability", "renewable", "fossil", "carbon", "energy", "technology"
    ],
    "Entertainment": [
        "entertainment", "movie", "film", "cinema", "hollywood", "actor", "actress", 
        "director", "producer", "television", "tv", "show", "series", "streaming",
        "music", "song", "album", "artist", "band", "concert", "tour", "celebrity",
        "star", "fame", "award", "oscar", "emmy", "grammy", "box office", "premiere",
        "theater", "performance", "comedy", "drama", "genre", "release", "trailer"
    ],
    "Sports": [
        "sport", "sports", "game", "match", "tournament", "championship", "league", 
        "team", "player", "athlete", "coach", "manager", "football", "soccer",
        "basketball", "baseball", "hockey", "tennis", "golf", "racing", "formula",
        "olympics", "olympic", "medal", "competition", "score", "win", "victory",
        "defeat", "loss", "stadium", "arena", "field", "court", "season", "fan"
    ],
    "Finance": [
        "finance", "financial", "bank", "banking", "investment", "investor", 
        "stock", "share", "market", "trading", "trader", "fund", "asset",
        "portfolio", "wealth", "money", "currency", "exchange", "forex", "crypto",
        "cryptocurrency", "bitcoin", "ethereum", "blockchain", "fintech", "loan",
        "mortgage", "interest", "rate", "inflation", "deflation", "economy",
        "economic", "recession", "growth", "gdp", "fiscal", "monetary", "policy"
    ],
    "Education": [
        "education", "school", "university", "college", "student", "teacher", 
        "professor", "academic", "learn", "learning", "study", "course", "degree",
        "graduate", "undergraduate", "campus", "classroom", "lecture", "curriculum",
        "exam", "test", "assessment", "research", "scholarship", "tuition", "student loan",
        "discipline", "field", "knowledge", "skills", "training", "development"
    ],
    "Travel": [
        "travel", "tourism", "tourist", "destination", "vacation", "holiday", 
        "trip", "journey", "adventure", "explore", "tour", "flight", "airline",
        "hotel", "resort", "accommodation", "booking", "reservation", "itinerary",
        "cruise", "beach", "mountain", "city", "country", "international", "domestic",
        "passport", "visa", "luggage", "backpack", "experience", "culture", "local"
    ]
}

def preprocess_text(text):
    """Preprocess text for categorization."""
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
    text = article_copy["title"] + " " + article_copy["content"]
    
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
            if article_copy["title"].lower().count(keyword) > 0:
                score += 5 * keyword_count  # Title match is weighted higher
            else:
                score += keyword_count
        
        if score > 0:
            category_scores[category] = score
    
    # Also consider the feed category (if available)
    if "feed_category" in article_copy and article_copy["feed_category"]:
        feed_category = article_copy["feed_category"]
        
        # Look for matching or similar category
        for category in category_scores.keys():
            if feed_category.lower() in category.lower() or category.lower() in feed_category.lower():
                category_scores[category] += 3  # Boost the score
    
    # Sort categories by score (descending)
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Keep only the top categories (those with significant scores)
    top_categories = [category for category, score in sorted_categories if score >= 2]
    
    # If no categories found, add the feed category or "General"
    if not top_categories:
        if "feed_category" in article_copy and article_copy["feed_category"]:
            top_categories = [article_copy["feed_category"]]
        else:
            top_categories = ["General"]
    
    # Limit to top 3 categories
    article_copy["categories"] = top_categories[:3]
    
    return article_copy

def categorize_articles(articles):
    """Categorize all articles."""
    categorized = []
    for article in articles:
        categorized_article = categorize_article(article)
        categorized.append(categorized_article)
    return categorized