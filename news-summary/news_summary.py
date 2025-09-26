"""
This script fetches top 10 technology news and posts them to a Slack channel.

To use this script, you need to set the following environment variables:
- NEWS_API_KEY: Your API key for the News API.
- SLACK_BOT_TOKEN: Your Slack bot token.
- SLACK_CHANNEL_ID: The ID of the Slack channel where you want to post the news.

You can create a .env file in the same directory as this script and add the
environment variables there, for example:
NEWS_API_KEY="your_api_key"
SLACK_BOT_TOKEN="your_slack_bot_token"
SLACK_CHANNEL_ID="your_slack_channel_id"

The script will then automatically load these variables.
"""
import os
import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import date, timedelta

load_dotenv()

def get_top_technology_news():
    """Fetches the top 10 technology news articles from the previous day in the
    United States.

    This function queries the NewsAPI for the top 10 technology headlines,
    sorted by popularity. It requires the `NEWS_API_KEY` environment variable
    to be set.

    Returns:
        list: A list of dictionaries, where each dictionary represents a news
              article. Returns an empty list if the API key is not set or if
              an error occurs during the API request.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("Error: NEWS_API_KEY environment variable not set.")
        return []

    url = "https://newsapi.org/v2/top-headlines"
    yesterday = date.today() - timedelta(days=1)
    params = {
        "country": "us",
        "from": yesterday.strftime('%Y-%m-%d'),
        "sortBy": "popularity",
        "category": "technology",
        "apiKey": api_key,
        "pageSize": 10
    }
    headers = {
        "User-Agent": "test"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching technology news: {e}")
        return []

def post_to_slack(channel_id, message):
    """Posts a message to a specified Slack channel.

    This function sends a message to a Slack channel using the Slack WebClient
    API. It requires the `SLACK_BOT_TOKEN` environment variable to be set.

    Args:
        channel_id (str): The ID of the Slack channel where the message will be
                          posted.
        message (str): The content of the message to post.
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

if __name__ == "__main__":
    channel_id = os.getenv("SLACK_CHANNEL_ID")
    if not channel_id:
        print("Error: SLACK_CHANNEL_ID environment variable not set.")
    else:
        articles = get_top_technology_news()
        if articles:
            message_body = ""
            for article in articles:
                title = article.get('title')
                description = article.get('description')
                url = article.get('url')
                if title and description and url:
                    message_body += f"• *<{url}|{title}>*\n_{description}_\n\n"
            
            if message_body:
                message = f"📰 *Top 10 Tech News*\n\n{message_body}"
                post_to_slack(channel_id, message)
