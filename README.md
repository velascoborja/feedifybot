# FeedifyBot

FeedifyBot is a Telegram bot in Python to log your baby's bottle feeds (in ml). It allows you to keep a daily record and receive an automatic summary every day at 21:00.

## Features
- `/feed <ml>` command to log the amount of milk fed.
- Automatic daily summary at 21:00 with the number of feeds and the total ml.
- Data persistence in Supabase.
- Easy deployment on Railway.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd feedifybot
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file with the following variables:
     - `TELEGRAM_BOT_TOKEN` (your Telegram bot token)
     - `SUPABASE_URL` (your Supabase project URL)
     - `SUPABASE_KEY` (your Supabase API Key)

## Deployment on Railway

1. Push the project to a GitHub repository.
2. Connect the repository to Railway.
3. Set the environment variables in Railway (`TELEGRAM_BOT_TOKEN`, `SUPABASE_URL`, `SUPABASE_KEY`).
4. Railway will automatically run the bot.

## Notes on the daily summary
- The daily summary is scheduled using a persistent scheduler (e.g., APScheduler with database storage or Railway cron jobs) to avoid missing it after restarts or deployments.

## License
MIT 