from datetime import datetime
import markdown

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
    newsletter += f"""## Today's Highlights
Welcome to your personalized newsletter, {user_data['name']}. Here are today's top stories curated just for you based on your interests in {', '.join(user_data['interests'][:3])}, and more.

---

"""
    
    # Group articles by category
    category_articles = {}
    
    for article in articles:
        for category in article["categories"]:
            if category not in category_articles:
                category_articles[category] = []
            category_articles[category].append(article)
    
    # Sort categories by number of articles (descending)
    sorted_categories = sorted(category_articles.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Generate sections for each category
    for category, cat_articles in sorted_categories:
        newsletter += f"## {category}\n\n"
        
        # Add articles for this category (up to 5)
        for article in cat_articles[:5]:
            newsletter += f"### [{article['title']}]({article['link']})\n"
            newsletter += f"*{article['source']} - {format_date(article['published'])}*\n\n"
            newsletter += f"{article.get('summary', article['content'][:300])}...\n\n"
            newsletter += "---\n\n"
    
    # Add footer
    newsletter += f"""
## Thanks for Reading!
This newsletter was generated specifically for {user_data['name']} based on personal interests and preferences. 

Check back tomorrow for more personalized news.
"""

    # Convert Markdown to HTML for better rendering in Streamlit
    html_content = markdown.markdown(newsletter)
    
    return html_content