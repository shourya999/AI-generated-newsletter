import streamlit as st
import pandas as pd
import os
import time
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
    generate_button = st.sidebar.button("Generate Newsletter")
    
    # Main content area
    if generate_button:
        with st.spinner("Fetching articles from RSS feeds..."):
            # Step 1: Fetch articles from RSS feeds
            articles = fetch_rss_feeds()
            st.success(f"✅ Successfully fetched {len(articles)} articles from RSS feeds.")
            
        with st.spinner("Categorizing articles..."):
            # Step 2: Categorize articles
            categorized_articles = categorize_articles(articles)
            st.success("✅ Successfully categorized articles.")
            
        with st.spinner("Filtering articles based on user preferences..."):
            # Step 3: Filter articles based on user preferences
            filtered_articles = filter_articles_for_user(categorized_articles, user_data)
            st.success(f"✅ Found {len(filtered_articles)} relevant articles for {selected_user}.")
            
        with st.spinner("Summarizing articles..."):
            # Step 4: Summarize articles
            summarized_articles = summarize_articles(filtered_articles)
            st.success("✅ Generated article summaries.")
            
        with st.spinner("Generating personalized newsletter..."):
            # Step 5: Generate newsletter
            newsletter_content = generate_newsletter(summarized_articles, user_data)
            
            # Save newsletter timestamp
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
        
        # Display newsletter in a nice format
        st.markdown(newsletter_data["content"], unsafe_allow_html=True)
    else:
        st.info("👈 Select a user and click 'Generate Newsletter' to create a personalized newsletter.")
        st.write("The system will fetch articles from RSS feeds, categorize them using NLP, and generate a personalized newsletter based on the selected user's interests.")

def filter_articles_for_user(categorized_articles, user_data):
    """Filter articles based on user preferences."""
    filtered_articles = []
    
    # Get user interests and preferred sources
    interests = [interest.lower() for interest in user_data["interests"]]
    sources = [source.lower() for source in user_data["sources"]]
    
    for article in categorized_articles:
        # Check if article matches user interests or comes from preferred source
        article_categories = [cat.lower() for cat in article["categories"]]
        article_source = article["source"].lower()
        
        # Calculate relevance score
        relevance_score = 0
        
        # Check for category/interest match
        for category in article_categories:
            for interest in interests:
                if interest in category or category in interest:
                    relevance_score += 3
                    break
        
        # Check for source match
        for source in sources:
            if source in article_source or article_source in source:
                relevance_score += 2
                break
        
        # Add article if it's relevant enough
        if relevance_score > 0:
            article["relevance_score"] = relevance_score
            filtered_articles.append(article)
    
    # Sort by relevance score
    filtered_articles.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Limit to top 15 articles
    return filtered_articles[:15]

if __name__ == "__main__":
    main()