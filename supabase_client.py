import os
import asyncio
from datetime import date, time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from supabase import create_client, Client

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase integration
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Keep a set of users who have used the bot
USERS: set[int] = set()

# Timezone for scheduled summary (adjust if needed)
TZ = ZoneInfo("Europe/Madrid")


# Supabase client class
class SupabaseClient:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def register_feed(self, user_id: int, amount_ml: int):
        """Register a new feeding in the database"""
        data = {
            "user_id": user_id,
            "amount_ml": amount_ml,
        }
        return self.supabase.table("feeds").insert(data).execute()

    def get_daily_feeds(self, user_id: int, day: date):
        """Get all feedings for a specific user on a specific day"""
        # Convert date to string in ISO format for the query
        day_str = day.isoformat()

        # Query feeds for this user on this day
        response = (
            self.supabase.table("feeds")
            .select("*")
            .eq("user_id", user_id)
            .gte("created_at", f"{day_str}T00:00:00")
            .lt("created_at", f"{day_str}T23:59:59")
            .execute()
        )

        return response.data


# ---------------------- Handlers ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.add(update.effective_user.id)
    await update.message.reply_text("¡Hola! Usa /feed <ml> para registrar un biberón.")


async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.add(update.effective_user.id)

    if not context.args:
        await update.message.reply_text("Uso: /feed <ml> (ejemplo: /feed 120)")
        return

    try:
        amount_ml = int(context.args[0])
    except ValueError:
        await update.message.reply_text("El valor debe ser un número entero. Ejemplo: /feed 120")
        return

    supabase.register_feed(update.effective_user.id, amount_ml)
    await update.message.reply_text(f"Feed registrado: {amount_ml} ml")


# ---------------------- Jobs ----------------------
async def send_daily_summary(context: ContextTypes.DEFAULT_TYPE):
    for user_id in list(USERS):
        feeds = supabase.get_daily_feeds(user_id, date.today())
        total = sum(f["amount_ml"] for f in feeds)
        n_feeds = len(feeds)
        if n_feeds > 0:
            text = f"Resumen de hoy:\nTomas: {n_feeds}\nTotal: {total} ml"
        else:
            text = "Hoy no has registrado tomas."
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
        except Exception:
            # El usuario puede haber bloqueado el bot, etc.
            pass


# ---------------------- Main ----------------------
async def main():
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("feed", feed))

    # Jobs: resumen diario a las 21:00 hora de Madrid
    app.job_queue.run_daily(send_daily_summary, time=time(hour=21, minute=0, tzinfo=TZ))

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())