import streamlit as st
import pandas as pd
import os
import time
import random
from user_preferences import USER_PERSONAS
from rss_parser import fetch_rss_feeds
from article_categorizer import categorize_articles
from newsletter_generator import generate_newsletter
from article_summarizer import summarize_articles
from utils import get_timestamp
st.set_page_config(
    page_title="AI-Driven Newsletter System", 
    page_icon="📰",
    layout="wide"
)
@st.cache_data(ttl=1800)  # Cache data for 30 minutes
def get_articles():
    """Fetch articles from RSS feeds."""
    articles = fetch_rss_feeds()
    if articles:
        return categorize_articles(articles)
    return []
def main():
    st.title("AI-Driven Personalized Newsletter System")
    st.write("This system curates personalized newsletters based on user preferences and interests.")
    
    # Sidebar for user selection and settings
    st.sidebar.title("Settings")
    
    # User selection
    selected_user = st.sidebar.selectbox(
        "Select User Persona",
        options=list(USER_PERSONAS.keys()),
        index=0
    )
    
    user_data = USER_PERSONAS[selected_user]
    
    # Display user details
    st.sidebar.subheader("User Details")
    st.sidebar.write(f"**Name:** {selected_user}")
    st.sidebar.write(f"**Age:** {user_data['age']}")
    st.sidebar.write(f"**Location:** {user_data['location']}")
    
    st.sidebar.subheader("Interests")
    for interest in user_data["interests"]:
        st.sidebar.write(f"- {interest}")
    
    st.sidebar.subheader("Preferred Sources")
    for source in user_data["sources"]:
        st.sidebar.write(f"- {source}")
    
    # Control section
    st.sidebar.subheader("Newsletter Generation")
    
    # Add refresh option to force refresh the cached articles
    refresh_data = st.sidebar.checkbox("Refresh Article Data", value=False)
    if refresh_data:
        st.cache_data.clear()
        st.sidebar.success("✅ Cache cleared! Article data will be refreshed.")
    
    generate_button = st.sidebar.button("Generate Newsletter")
    
    # Main content area
    if generate_button:
        with st.spinner("Generating your personalized newsletter..."):
            # Step 1: Fetch and categorize articles
            articles = get_articles()
            
            if not articles:
                st.error("Unable to fetch articles. Please check your internet connection and try again.")
                return
            
            # Step 2: Filter articles based on user preferences
            filtered_articles = filter_articles_for_user(articles, user_data)
            
            if not filtered_articles:
                st.warning(f"No relevant articles found for {selected_user}. Try refreshing the data.")
                return
            
            # Step 3: Summarize articles
            summarized_articles = summarize_articles(filtered_articles)
            
            # Step 4: Generate newsletter
            newsletter_content = generate_newsletter(summarized_articles, user_data)
            
            # Save newsletter with timestamp
            timestamp = get_timestamp()
            st.session_state[f"newsletter_{selected_user}"] = {
                "content": newsletter_content,
                "timestamp": timestamp
            }
        
        st.success(f"✅ Generated personalized newsletter for {selected_user}.")
    
    # Display generated newsletter if available
    if f"newsletter_{selected_user}" in st.session_state:
        newsletter_data = st.session_state[f"newsletter_{selected_user}"]
        
        st.header(f"{selected_user}'s Personalized Newsletter")
        st.caption(f"Generated on: {newsletter_data['timestamp']}")
        
        # Display newsletter using native Streamlit markdown rendering
        st.markdown(newsletter_data["content"])
        
        # Add option to download as markdown
        st.download_button(
            label="Download Newsletter as Markdown",
            data=newsletter_data["content"],
            file_name=f"{selected_user.replace(' ', '_')}_newsletter_{newsletter_data['timestamp'].replace(':', '-').replace(' ', '_')}.md",
            mime="text/markdown"
        )
    else:
        st.info("👈 Select a user and click 'Generate Newsletter' to create a personalized newsletter.")
        st.write("The system will fetch articles from RSS feeds, categorize them using NLP, and generate a personalized newsletter based on the selected user's interests.")
def filter_articles_for_user(categorized_articles, user_data):
    """Filter articles based on user preferences with enhanced matching for entertainment content."""
    filtered_articles = []
    
    # Get user interests and preferred sources
    interests = [interest.lower() for interest in user_data["interests"]]
    sources = [source.lower() for source in user_data["sources"]]
    
    # Special case for entertainment interests (for Lisa Thompson)
    entertainment_keywords = ["movie", "film", "cinema", "tv", "television", "show", "celebrity", 
                            "music", "song", "album", "artist", "actor", "actress", "entertainment",
                            "hollywood", "book", "novel", "author", "star", "concert", "festival",
                            "award", "performance", "theater", "series", "streaming", "netflix",
                            "disney", "hbo", "release", "premiere"]
    
    # Check if user has entertainment interests
    has_entertainment_interests = any(interest in entertainment_keywords for interest in interests)
    
    for article in categorized_articles:
        # Get article properties
        article_categories = [cat.lower() for cat in article.get("categories", [])]
        article_source = article.get("source", "").lower()
        article_title = article.get("title", "").lower()
        article_content = article.get("content", "").lower()
        
        # Calculate relevance score
        relevance_score = 0
        
        # Check for category/interest match
        for category in article_categories:
            for interest in interests:
                if interest in category or category in interest:
                    relevance_score += 3
                    break
        
        # Check for interest in title (stronger match)
        for interest in interests:
            if interest in article_title:
                relevance_score += 4
                break
        
        # Check for interest in content
        if relevance_score == 0:  # Only check content if no matches found yet
            for interest in interests:
                if interest in article_content:
                    relevance_score += 1
                    break
        
        # Check for source match
        for source in sources:
            if source in article_source or article_source in source:
                relevance_score += 2
                break
        
        # Special handling for entertainment content when needed
        if has_entertainment_interests and relevance_score == 0:
            # Check if article is about entertainment
            for keyword in entertainment_keywords:
                if keyword in article_title or keyword in " ".join(article_categories):
                    relevance_score += 2
                    break
                elif keyword in article_content:
                    relevance_score += 1
                    break
        
        # Add article if it's relevant enough
        if relevance_score > 0:
            article["relevance_score"] = relevance_score
            filtered_articles.append(article)
    
    # Sort by relevance score
    filtered_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    # If we still have no articles, try a broader match (especially for entertainment)
    if not filtered_articles and has_entertainment_interests:
        for article in categorized_articles:
            article_content = article.get("content", "").lower()
            article_title = article.get("title", "").lower()
            
            # Check for any entertainment-related content
            for keyword in entertainment_keywords:
                if keyword in article_title or keyword in article_content:
                    article["relevance_score"] = 1
                    filtered_articles.append(article)
                    break
        
        # Sort these by relevance score
        filtered_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    # If still no articles, include some general articles
    if not filtered_articles:
        # Take a sample of recent articles
        sample_size = min(10, len(categorized_articles))
        filtered_articles = random.sample(categorized_articles, sample_size)
    
    # Limit to top 15 articles
    return filtered_articles[:15]
if __name__ == "__main__":
    main()
