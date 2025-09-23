# Calendar Summarizer

This script fetches tomorrow's events from your Google Calendar and posts a summary to a Slack channel.

## Setup

### 1. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

### 2. Google Calendar API Credentials

1.  **Enable the Google Calendar API:**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project.
    *   Go to **APIs & Services > Library**.
    *   Search for "Google Calendar API" and enable it.

2.  **Create OAuth 2.0 Credentials:**
    *   Go to **APIs & Services > Credentials**.
    *   Click **Create Credentials > OAuth client ID**.
    *   Select **Desktop app** as the application type.
    *   Click **Create**.
    *   Download the JSON file and save it as `credentials.json` in the same directory as the script.

### 3. Slack API Credentials

1.  **Create a Slack App:**
    *   Go to the [Slack API website](https://api.slack.com/apps).
    *   Click **Create New App**.
    *   Choose "From scratch", give your app a name, and select the workspace where you want to post messages.

2.  **Add Permissions:**
    *   In your app's settings, go to **OAuth & Permissions**.
    *   Under **Bot Token Scopes**, add the `chat:write` scope.

3.  **Install the App:**
    *   Install the app to your workspace.
    *   Copy the **Bot User OAuth Token**.

4.  **Set Environment Variable:**
    *   Set the `SLACK_BOT_TOKEN` environment variable to your Bot User OAuth Token.
        *   On macOS/Linux: `export SLACK_BOT_TOKEN="your-token-here"`
        *   On Windows: `set SLACK_BOT_TOKEN="your-token-here"`

### 4. Configure the Script

*   Open `main.py` and change the `SLACK_CHANNEL` variable to the name of the channel you want to post to (e.g., `#random`).

## Running the Script

1.  **First Run (Google Calendar Authentication):**
    *   Run the script from your terminal: `python main.py`
    *   Your web browser will open, asking you to authorize access to your Google Calendar.
    *   After you grant permission, a `token.json` file will be created in the same directory. This file stores your authentication tokens, so you won't have to log in every time.

2.  **Subsequent Runs:**
    *   Simply run the script again: `python main.py`
    *   The script will use the `token.json` file to authenticate and will post the summary of tomorrow's events to your specified Slack channel.
