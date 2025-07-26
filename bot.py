import os
import asyncio
import logging
from datetime import date, time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue,
)

from supabase_client import SupabaseClient

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    exit(1)

logger.info("Bot starting...")

# Supabase integration
supabase = SupabaseClient()

# Keep a set of users who have used the bot
USERS: set[int] = set()

# Timezone for scheduled summary (adjust if needed)
TZ = ZoneInfo("Europe/Madrid")


# ---------------------- Handlers ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Start command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)
    await update.message.reply_text("Hi! Use /feed <ml> to log a bottle.")


async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Feed command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)

    if not context.args:
        await update.message.reply_text("Usage: /feed <ml> (example: /feed 120)")
        return

    try:
        amount_ml = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Value must be an integer. Example: /feed 120")
        return

    try:
        supabase.register_feed(update.effective_user.id, amount_ml)
        await update.message.reply_text(f"Feed logged: {amount_ml} ml")
        logger.info(f"Feed logged: {amount_ml} ml for user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error logging feed: {e}")
        await update.message.reply_text("Sorry, there was an error logging your feed. Please try again.")


# ---------------------- Jobs ----------------------
async def send_daily_summary(context: ContextTypes.DEFAULT_TYPE):
    for user_id in list(USERS):
        feeds = supabase.get_daily_feeds(user_id, date.today())
        total = sum(f["amount_ml"] for f in feeds)
        n_feeds = len(feeds)
        if n_feeds > 0:
            text = f"Today's summary:\nFeeds: {n_feeds}\nTotal: {total} ml"
        else:
            text = "You haven't logged any feeds today."
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
        except Exception:
            # The user may have blocked the bot, etc.
            pass


# ---------------------- Main ----------------------
def main():
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .job_queue(JobQueue())
        .build()
    )

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("feed", feed))

    # Jobs: daily summary at 21:00 Europe/Madrid
    app.job_queue.run_daily(send_daily_summary, time=time(hour=21, minute=0, tzinfo=TZ))

    logger.info("Starting bot...")
    app.run_polling()


if __name__ == "__main__":
    main()