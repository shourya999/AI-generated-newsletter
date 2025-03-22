from datetime import datetime

def format_date(date_obj):
    """Format a datetime object to a readable date string."""
    return date_obj.strftime("%B %d, %Y")

def generate_newsletter(articles, user_data):
    """Generate a personalized newsletter in Markdown format."""
    now = datetime.now()
    date_str = format_date(now)
    
    # Start with header
    newsletter = f"""# {user_data['name']}'s Personalized Newsletter
### {date_str}

---

"""
    
    # Add introduction
    interests_text = ', '.join(user_data['interests'][:3])
    newsletter += f"""## Today's Highlights
Welcome to your personalized newsletter, {user_data['name']}. Here are today's top stories curated just for you based on your interests in {interests_text}, and more.

---

"""
    
    # Group articles by category
    category_articles = {}
    
    for article in articles:
        primary_category = article["categories"][0] if article["categories"] else "General"
        if primary_category not in category_articles:
            category_articles[primary_category] = []
        category_articles[primary_category].append(article)
    
    # Sort categories by number of articles (descending)
    sorted_categories = sorted(category_articles.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Generate sections for each category
    for category, cat_articles in sorted_categories:
        # Add category header with emoji
        emoji = get_category_emoji(category)
        newsletter += f"## {emoji} {category}\n\n"
        
        # Add articles for this category (up to 4)
        for i, article in enumerate(cat_articles[:4]):
            # Format publication date
            pub_date = format_date(article['published']) if 'published' in article else "Recent"
            
            # Add article title with link
            newsletter += f"### [{article['title']}]({article['link']})\n"
            newsletter += f"*{article['source']} - {pub_date}*\n\n"
            
            # Add article summary
            if 'summary' in article and article['summary']:
                newsletter += f"{article['summary']}\n\n"
            else:
                newsletter += f"{article['content'][:250]}...\n\n"
            
            # Add separator between articles except after the last one
            if i < len(cat_articles[:4]) - 1:
                newsletter += "---\n\n"
            
        # Add some space between categories
        newsletter += "\n\n"
    
    # Add personalized closing section
    newsletter += f"""## Thanks for Reading!
This newsletter was generated specifically for {user_data['name']} based on personal interests including {interests_text}.

Check back tomorrow for more personalized news.
"""
    
    return newsletter

def get_category_emoji(category):
    """Return an emoji based on the category."""
    category_emojis = {
        "Technology": "💻",
        "Business": "💼",
        "Politics": "🏛️",
        "Health": "🏥",
        "Science": "🔬",
        "Entertainment": "🎬",
        "Sports": "🏆",
        "Finance": "💰",
        "Education": "📚",
        "Travel": "✈️",
        "General": "📰"
    }
    
    # Return the emoji for the category or a default newspaper emoji
    return category_emojis.get(category, "📄")
