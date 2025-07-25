import os
from telegram import Update
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
import asyncio
import pytz

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Placeholder for Supabase integration
from supabase_client import SupabaseClient
supabase = SupabaseClient()

# Keep a set of users who have used the bot
USERS = set()

def start(update, context):
    USERS.add(update.effective_user.id)
    update.message.reply_text('Hello! Use /feed <ml> to log a bottle feed.')

def feed(update, context):
    USERS.add(update.effective_user.id)
    try:
        amount_ml = int(context.args[0])
        supabase.register_feed(update.effective_user.id, amount_ml)
        update.message.reply_text(f'Feed logged: {amount_ml} ml')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /feed <ml> (example: /feed 120)')

def send_daily_summary():
    from telegram import Bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    for user_id in USERS:
        feeds = supabase.get_daily_feeds(user_id, date.today())
        total = sum(f["amount_ml"] for f in feeds)
        n_feeds = len(feeds)
        if n_feeds > 0:
            text = f"Today's summary:\nFeeds: {n_feeds}\nTotal: {total} ml"
        else:
            text = 'No feeds have been logged today.'
        try:
            bot.send_message(chat_id=user_id, text=text)
        except Exception:
            pass  # The user may have blocked the bot, etc.

if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('feed', feed))

    scheduler = BackgroundScheduler(timezone=pytz.utc)
    # Run at 21:00 server time
    scheduler.add_job(send_daily_summary, 'cron', hour=21, minute=0)
    scheduler.start()

    updater.start_polling()
    updater.idle() 