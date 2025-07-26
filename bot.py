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

# Default timezone (used if user hasn't set a custom one)
DEFAULT_TZ = ZoneInfo("Europe/Madrid")


# ---------------------- Helper Functions ----------------------
def get_user_timezone(user_id: int):
    """Get the user's timezone or return default"""
    user_tz = supabase.get_user_timezone(user_id)
    if user_tz:
        try:
            return ZoneInfo(user_tz)
        except Exception:
            # If invalid timezone, return default
            return DEFAULT_TZ
    return DEFAULT_TZ


# ---------------------- Handlers ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Start command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)
    await update.message.reply_text("Hi! Use /feed <ml> to log a bottle.\n\nYou can also set your timezone with /timezone <timezone> (e.g., /timezone Europe/Madrid)")


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


async def timezone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Timezone command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)

    if not context.args:
        # Show current timezone
        current_tz = supabase.get_user_timezone(update.effective_user.id)
        if current_tz:
            await update.message.reply_text(f"Your current timezone is: {current_tz}")
        else:
            await update.message.reply_text(f"You haven't set a timezone. Using default: Europe/Madrid\n\nTo set your timezone, use: /timezone <timezone>\nExample: /timezone America/New_York")
        return

    timezone_str = context.args[0]
    
    # Validate timezone
    try:
        ZoneInfo(timezone_str)
    except Exception:
        await update.message.reply_text(f"Invalid timezone: {timezone_str}\n\nPlease use a valid timezone like:\n- Europe/Madrid\n- America/New_York\n- Asia/Tokyo\n- UTC")
        return

    try:
        supabase.set_user_timezone(update.effective_user.id, timezone_str)
        await update.message.reply_text(f"Timezone set to: {timezone_str}")
        logger.info(f"Timezone set to {timezone_str} for user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error setting timezone: {e}")
        await update.message.reply_text("Sorry, there was an error setting your timezone. Please try again.")


# ---------------------- Jobs ----------------------
async def send_daily_summary(context: ContextTypes.DEFAULT_TYPE):
    for user_id in list(USERS):
        user_tz = get_user_timezone(user_id)
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
    app.add_handler(CommandHandler("timezone", timezone_command))

    # Jobs: daily summary at 21:00 using default timezone
    # Note: Each user will get the summary based on their timezone
    app.job_queue.run_daily(send_daily_summary, time=time(hour=21, minute=0, tzinfo=DEFAULT_TZ))

    logger.info("Starting bot...")
    app.run_polling()


if __name__ == "__main__":
    main()