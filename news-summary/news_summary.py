"""
This script fetches top news from CNN and BBC, summarizes them, and posts the
summaries to a Slack channel.

To use this script, you need to set the following environment variables:
- WORLD_NEWS_API_KEY: Your API key for the World News API.
- SLACK_BOT_TOKEN: Your Slack bot token.
- SLACK_CHANNEL_ID: The ID of the Slack channel where you want to post the news.

You can create a .env file in the same directory as this script and add the
environment variables there, for example:
WORLD_NEWS_API_KEY="your_api_key"
SLACK_BOT_TOKEN="your_slack_bot_token"
SLACK_CHANNEL_ID="your_slack_channel_id"

The script will then automatically load these variables.
"""
import os
import requests
from dotenv import load_dotenv
from transformers import pipeline
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

def get_news(source):
    """
    Fetches news from a given source using the World News API.

    Args:
        source (str): The source to fetch news from (e.g., "cnn.com").

    Returns:
        list: A list of news articles, or an empty list if an error occurs.
    """
    api_key = os.getenv("WORLD_NEWS_API_KEY")
    if not api_key:
        print("Error: WORLD_NEWS_API_KEY environment variable not set.")
        return []

    url = "https://api.worldnewsapi.com/search-news"
    params = {
        "source-countries": "us",
        "news-sources": f"https://www.{source}",
        "api-key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("news", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from {source}: {e}")
        return []

def summarize_text(text):
    """
    Summarizes a given text using a pre-trained model.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The summarized text.
    """
    try:
        summarizer = pipeline("summarization", model="t5-small")
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return ""

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
        response = client.chat_postMessage(channel=channel_id, text=message)
        print("Message posted to Slack successfully.")
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")

if __name__ == "__main__":
    channel_id = os.getenv("SLACK_CHANNEL_ID")
    if not channel_id:
        print("Error: SLACK_CHANNEL_ID environment variable not set.")
    else:
        cnn_news = get_news("cnn.com")
        if cnn_news:
            for article in cnn_news:
                summary = summarize_text(article['text'])
                message = f"📰 *CNN News:* {article['title']}\n\n{summary}"
                post_to_slack(channel_id, message)

        bbc_news = get_news("bbc.com")
        if bbc_news:
            for article in bbc_news:
                summary = summarize_text(article['text'])
                message = f"📰 *BBC News:* {article['title']}\n\n{summary}"
                post_to_slack(channel_id, message)
