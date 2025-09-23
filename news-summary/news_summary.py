"""
This script fetches top news from CNN and BBC, summarizes them using Gemini Pro,
and posts the summaries to a Slack channel.

To use this script, you need to set the following environment variables:
- NEWS_API_KEY: Your API key for the News API.
- SLACK_BOT_TOKEN: Your Slack bot token.
- SLACK_CHANNEL_ID: The ID of the Slack channel where you want to post the news.
- GEMINI_API_KEY: Your API key for Gemini Pro.

You can create a .env file in the same directory as this script and add the
environment variables there, for example:
NEWS_API_KEY=\"your_api_key\"
SLACK_BOT_TOKEN=\"your_slack_bot_token\"
SLACK_CHANNEL_ID=\"your_slack_channel_id\"
GEMINI_API_KEY=\"your_gemini_api_key\"

The script will then automatically load these variables.
"""
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

def get_news(source):
    """
    Fetches news from a given source using the News API.

    Args:
        source (str): The source to fetch news from (e.g., "cnn").

    Returns:
        list: A list of news articles, or an empty list if an error occurs.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("Error: NEWS_API_KEY environment variable not set.")
        return []

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "sources": source,
        "apiKey": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from {source}: {e}")
        return []

def summarize_text(text):
    """
    Summarizes a given text using the Gemini Pro model.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The summarized text.
    """
    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            print("Error: GEMINI_API_KEY environment variable not set.")
            return None

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(f"Summarize the following news article in 1-2 sentences: {text}")
        return response.text
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None

def post_to_slack(channel_id, message):
    """
    Posts a message to a Slack channel.

    Args:
        channel_id (str): The ID of the Slack channel.
        message (str): The message to post.
    """
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    if not slack_bot_token:
        print("Error: SLACK_BOT_TOKEN environment variable not set.")
        return

    client = WebClient(token=slack_bot_token)
    try:
        client.chat_postMessage(channel=channel_id, text=message)
        print("Message posted to Slack successfully.")
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")

def process_and_post_news(channel_id, source_id, source_name):
    """
    Fetches, summarizes, and posts news from a given source.

    Args:
        channel_id (str): The ID of the Slack channel.
        source_id (str): The ID of the news source (e.g., "cnn").
        source_name (str): The name of the news source (e.g., "CNN").
    """
    news_articles = get_news(source_id)
    if news_articles:
        for article in news_articles:
            text_to_summarize = article.get('content') or article.get('description')
            if text_to_summarize:
                summary = summarize_text(text_to_summarize)
                if summary is not None:
                    message = f"📰 *{source_name}:* {article['title']}\n\n{summary}"
                    post_to_slack(channel_id, message)

if __name__ == "__main__":
    channel_id = os.getenv("SLACK_CHANNEL_ID")
    if not channel_id:
        print("Error: SLACK_CHANNEL_ID environment variable not set.")
    else:
        news_sources = [("cnn", "CNN"), ("bbc-news", "BBC News")]
        for source_id, source_name in news_sources:
            process_and_post_news(channel_id, source_id, source_name)