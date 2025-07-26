import os
import asyncio
import logging
from datetime import date, time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue,
    CallbackQueryHandler,
    MessageHandler,
    filters,
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

# User conversation states
USER_STATES: dict[int, str] = {}

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
    try:
        # First try to get from database
        stored_lang = supabase.get_user_language(update.effective_user.id)
        if stored_lang:
            return stored_lang
        
        # Then try to detect from Telegram
        detected_lang = detect_user_language(update)
        
        # Store detected language for future use
        try:
            supabase.set_user_language(update.effective_user.id, detected_lang)
            logger.info(f"Stored language {detected_lang} for user {update.effective_user.id}")
        except Exception as e:
            # If storing fails, just continue
            logger.warning(f"Failed to store language for user {update.effective_user.id}: {e}")
        
        return detected_lang
    except Exception as e:
        # If anything fails, fall back to English
        logger.error(f"Error getting user language for user {update.effective_user.id}: {e}")
        return "en"


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


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Today command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)
    
    # Get user language
    user_lang = get_user_language(update)
    
    try:
        # Get today's feeds for the user
        feeds = supabase.get_daily_feeds(update.effective_user.id, date.today())
        
        # Ensure feeds is a list
        if feeds is None:
            feeds = []
            
        total = sum(f.get("amount_ml", 0) for f in feeds)
        n_feeds = len(feeds)
        
        if n_feeds > 0:
            # Calculate average
            average = round(total / n_feeds, 1)
            message = get_message(user_lang, "today_with_feeds", 
                                n_feeds=n_feeds, 
                                total=total, 
                                average=average)
        else:
            message = get_message(user_lang, "today_no_feeds")
            
        await update.message.reply_text(message)
        logger.info(f"Today summary sent to user {update.effective_user.id}: {n_feeds} feeds, {total} ml")
        
    except Exception as e:
        logger.error(f"Error getting today's summary for user {update.effective_user.id}: {e}")
        message = get_message(user_lang, "today_error")
        await update.message.reply_text(message)


async def setup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Setup command received from user {update.effective_user.id}")
    USERS.add(update.effective_user.id)
    
    # Get user language
    user_lang = get_user_language(update)
    
    # Create inline keyboard with setup options
    keyboard = [
        [InlineKeyboardButton(
            get_message(user_lang, "setup_reminder_button"), 
            callback_data="setup_reminder"
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = get_message(user_lang, "setup_menu")
    await update.message.reply_text(message, reply_markup=reply_markup)


async def handle_setup_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback from setup menu buttons"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_lang = supabase.get_user_language(user_id) or "en"
    
    if query.data == "setup_reminder":
        # Show current reminder time if set
        current_time = supabase.get_user_reminder_time(user_id)
        if current_time:
            current_msg = get_message(user_lang, "setup_reminder_current", time=current_time)
            await query.edit_message_text(current_msg)
        
        # Set user state to waiting for reminder time
        USER_STATES[user_id] = "waiting_reminder_time"
        
        # Ask for new time
        message = get_message(user_lang, "setup_reminder_prompt")
        await context.bot.send_message(chat_id=user_id, text=message)


async def handle_reminder_time_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user input for reminder time"""
    user_id = update.effective_user.id
    user_lang = get_user_language(update)
    
    # Check if user is in the right state
    if USER_STATES.get(user_id) != "waiting_reminder_time":
        return
    
    time_input = update.message.text.strip()
    
    # Validate time format (HH:MM)
    import re
    time_pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    
    if not re.match(time_pattern, time_input):
        message = get_message(user_lang, "setup_reminder_invalid")
        await update.message.reply_text(message)
        return
    
    try:
        # Save the reminder time
        supabase.set_user_reminder_time(user_id, time_input)
        
        # Clear user state
        if user_id in USER_STATES:
            del USER_STATES[user_id]
        
        # Reschedule the reminder for this user
        reschedule_user_reminder(context.application, user_id)
        
        message = get_message(user_lang, "setup_reminder_set", time=time_input)
        await update.message.reply_text(message)
        
        logger.info(f"Reminder time set to {time_input} for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error setting reminder time for user {user_id}: {e}")
        message = get_message(user_lang, "setup_reminder_error")
        await update.message.reply_text(message)


def reschedule_user_reminder(app, user_id: int):
    """Reschedule reminder for a specific user"""
    try:
        reminder_time = supabase.get_user_reminder_time(user_id)
        user_tz = get_user_timezone(user_id)
        
        # Create a unique job name for this user
        job_name = f"daily_summary_{user_id}"
        
        # Remove existing job if it exists
        current_jobs = app.job_queue.get_jobs_by_name(job_name)
        for job in current_jobs:
            job.schedule_removal()
        
        if reminder_time:
            # Parse the time string (HH:MM)
            hour, minute = map(int, reminder_time.split(':'))
            
            # Schedule new job
            app.job_queue.run_daily(
                send_daily_summary_to_user,
                time=time(hour=hour, minute=minute, tzinfo=user_tz),
                data={'user_id': user_id},
                name=job_name
            )
            logger.info(f"Rescheduled daily reminder for user {user_id} at {reminder_time} ({user_tz})")
        else:
            # Use default time if no custom time is set
            app.job_queue.run_daily(
                send_daily_summary_to_user,
                time=time(hour=21, minute=0, tzinfo=user_tz),
                data={'user_id': user_id},
                name=job_name
            )
            logger.info(f"Rescheduled default daily reminder for user {user_id} at 21:00 ({user_tz})")
            
    except Exception as e:
        logger.error(f"Error rescheduling reminder for user {user_id}: {e}")


# ---------------------- Jobs ----------------------
async def send_daily_summary_to_user(context: ContextTypes.DEFAULT_TYPE):
    """Send daily summary to a specific user"""
    job_context = context.job.data
    user_id = job_context['user_id']
    
    user_tz = get_user_timezone(user_id)
    user_lang = supabase.get_user_language(user_id) or "en"
    
    feeds = supabase.get_daily_feeds(user_id, date.today())
    total = sum(f.get("amount_ml", 0) for f in feeds)
    n_feeds = len(feeds)
    
    if n_feeds > 0:
        text = get_message(user_lang, "summary_with_feeds", n_feeds=n_feeds, total=total)
    else:
        text = get_message(user_lang, "summary_no_feeds")
        
    try:
        await context.bot.send_message(chat_id=user_id, text=text)
        logger.info(f"Daily summary sent to user {user_id}: {n_feeds} feeds, {total} ml")
    except Exception as e:
        logger.error(f"Error sending daily summary to user {user_id}: {e}")


def schedule_user_reminders(app):
    """Schedule daily reminders for all users based on their individual settings"""
    for user_id in USERS:
        try:
            reminder_time = supabase.get_user_reminder_time(user_id)
            user_tz = get_user_timezone(user_id)
            
            if reminder_time:
                # Parse the time string (HH:MM)
                hour, minute = map(int, reminder_time.split(':'))
                
                # Create a unique job name for this user
                job_name = f"daily_summary_{user_id}"
                
                # Remove existing job if it exists
                current_jobs = app.job_queue.get_jobs_by_name(job_name)
                for job in current_jobs:
                    job.schedule_removal()
                
                # Schedule new job
                app.job_queue.run_daily(
                    send_daily_summary_to_user,
                    time=time(hour=hour, minute=minute, tzinfo=user_tz),
                    data={'user_id': user_id},
                    name=job_name
                )
                logger.info(f"Scheduled daily reminder for user {user_id} at {reminder_time} ({user_tz})")
            else:
                # Use default time if no custom time is set
                job_name = f"daily_summary_{user_id}"
                
                # Remove existing job if it exists
                current_jobs = app.job_queue.get_jobs_by_name(job_name)
                for job in current_jobs:
                    job.schedule_removal()
                
                # Schedule with default time
                app.job_queue.run_daily(
                    send_daily_summary_to_user,
                    time=time(hour=21, minute=0, tzinfo=user_tz),
                    data={'user_id': user_id},
                    name=job_name
                )
                logger.info(f"Scheduled default daily reminder for user {user_id} at 21:00 ({user_tz})")
                
        except Exception as e:
            logger.error(f"Error scheduling reminder for user {user_id}: {e}")


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
    app.add_handler(CommandHandler("today", today_command))
    app.add_handler(CommandHandler("setup", setup_command))
    app.add_handler(CommandHandler("timezone", timezone_command))
    
    # Callback query handler for inline buttons
    app.add_handler(CallbackQueryHandler(handle_setup_callback))
    
    # Message handler for reminder time input
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reminder_time_input))

    # Schedule individual reminders for users
    schedule_user_reminders(app)

    logger.info("Starting bot...")
    app.run_polling()


if __name__ == "__main__":
    main()