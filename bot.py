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
from messages import get_message, detect_user_language

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


def get_user_language(update: Update) -> str:
    """Get the user's preferred language"""
    # First try to get from database
    stored_lang = supabase.get_user_language(update.effective_user.id)
    if stored_lang:
        return stored_lang
    
    # Then try to detect from Telegram
    detected_lang = detect_user_language(update)
    
    # Store detected language for future use
    try:
        supabase.set_user_language(update.effective_user.id, detected_lang)
    except Exception:
        # If storing fails, just continue
        pass
    
    return detected_lang


# ---------------------- Handlers ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Start command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)
    
    # Get user language
    user_lang = get_user_language(update)
    message = get_message(user_lang, "start_message")
    
    await update.message.reply_text(message)


async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Feed command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)
    
    # Get user language
    user_lang = get_user_language(update)

    if not context.args:
        message = get_message(user_lang, "feed_usage")
        await update.message.reply_text(message)
        return

    try:
        amount_ml = int(context.args[0])
    except ValueError:
        message = get_message(user_lang, "feed_invalid_number")
        await update.message.reply_text(message)
        return

    try:
        supabase.register_feed(update.effective_user.id, amount_ml)
        message = get_message(user_lang, "feed_logged", amount_ml=amount_ml)
        await update.message.reply_text(message)
        logger.info(f"Feed logged: {amount_ml} ml for user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error logging feed: {e}")
        message = get_message(user_lang, "feed_error")
        await update.message.reply_text(message)


async def timezone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Timezone command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)
    
    # Get user language
    user_lang = get_user_language(update)

    if not context.args:
        # Show current timezone
        current_tz = supabase.get_user_timezone(update.effective_user.id)
        if current_tz:
            message = get_message(user_lang, "timezone_current", timezone=current_tz)
        else:
            message = get_message(user_lang, "timezone_not_set")
        await update.message.reply_text(message)
        return

    timezone_str = context.args[0]
    
    # Validate timezone
    try:
        ZoneInfo(timezone_str)
    except Exception:
        message = get_message(user_lang, "timezone_invalid", timezone=timezone_str)
        await update.message.reply_text(message)
        return

    try:
        supabase.set_user_timezone(update.effective_user.id, timezone_str)
        message = get_message(user_lang, "timezone_set", timezone=timezone_str)
        await update.message.reply_text(message)
        logger.info(f"Timezone set to {timezone_str} for user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error setting timezone: {e}")
        message = get_message(user_lang, "timezone_error")
        await update.message.reply_text(message)


# ---------------------- Jobs ----------------------
async def send_daily_summary(context: ContextTypes.DEFAULT_TYPE):
    for user_id in list(USERS):
        user_tz = get_user_timezone(user_id)
        user_lang = supabase.get_user_language(user_id) or "en"
        
        feeds = supabase.get_daily_feeds(user_id, date.today())
        total = sum(f["amount_ml"] for f in feeds)
        n_feeds = len(feeds)
        
        if n_feeds > 0:
            text = get_message(user_lang, "summary_with_feeds", n_feeds=n_feeds, total=total)
        else:
            text = get_message(user_lang, "summary_no_feeds")
            
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