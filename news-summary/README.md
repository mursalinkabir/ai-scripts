# News Summary Script

This script fetches top news from CNN and BBC, summarizes them, and posts the summaries to a Slack channel.

## Setup Instructions

### 1. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage the dependencies for this project.

**On macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

Install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

This script requires you to set up a few environment variables for the API keys and Slack configuration.

Create a file named `.env` in the `news-summary` directory and add the following content:

```
WORLD_NEWS_API_KEY="your_world_news_api_key"
SLACK_BOT_TOKEN="your_slack_bot_token"
SLACK_CHANNEL_ID="your_slack_channel_id"
```

Replace the placeholder values with your actual credentials:
- `your_world_news_api_key`: Your API key from [World News API](https://worldnewsapi.com/).
- `your_slack_bot_token`: Your Slack bot token. You can create a new Slack app and get the token.
- `your_slack_channel_id`: The ID of the Slack channel where you want to post the news.

### 4. Run the Script

Once you have completed the setup, you can run the script with the following command:
```bash
python news_summary.py
```

The script will fetch the latest news from CNN and BBC, summarize them, and post the summaries to your configured Slack channel.
