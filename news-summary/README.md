# News Summary Script

This script fetches top 5 technology news, summarizes them using Gemini Pro, and posts the summaries to a Slack channel.

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
NEWS_API_KEY="your_news_api_key"
SLACK_BOT_TOKEN="your_slack_bot_token"
SLACK_CHANNEL_ID="your_slack_channel_id"
GEMINI_API_KEY="your_gemini_api_key"
```

Replace the placeholder values with your actual credentials:
- `your_news_api_key`: Your API key from [NewsAPI](https://newsapi.org/).
- `your_slack_bot_token`: Your Slack bot token. You can create a new Slack app and get the token.
- `your_slack_channel_id`: The ID of the Slack channel where you want to post the news.
- `your_gemini_api_key`: Your API key for Gemini Pro.

### 4. Run the Script

Once you have completed the setup, you can run the script with the following command:
```bash
python news_summary.py
```

The script will fetch the latest technology news, summarize them, and post the summaries to your configured Slack channel.

### 5. Automate with Cronjob on AlmaLinux

To run the script automatically at a scheduled time, you can set up a cronjob. This example runs the script every day at 9 AM.

1.  **Open the crontab editor:**
    ```bash
    crontab -e
    ```

2.  **Add the cronjob entry:**

    Add the following line to the file, replacing `/path/to/your/project/news-summary` with the absolute path to your project directory.

    ```
    0 9 * * * /path/to/your/project/news-summary/venv/bin/python /path/to/your/project/news-summary/news_summary.py
    ```

    This command does the following:
    - `0 9 * * *`: This is the schedule. It means the job will run at 9:00 AM every day.
    - `/path/to/your/project/news-summary/venv/bin/python`: This specifies the Python interpreter from your virtual environment.
    - `/path/to/your/project/news-summary/news_summary.py`: This is the path to the script you want to run.

3.  **Save and Exit:**

    Save the file and exit the editor. The cronjob is now active.