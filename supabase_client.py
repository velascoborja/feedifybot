import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def register_feed(self, user_id: int, amount_ml: int):
        now = datetime.utcnow().isoformat()
        data = {
            "user_id": user_id,
            "amount_ml": amount_ml,
            "timestamp": now
        }
        res = self.client.table("feeds").insert(data).execute()
        return res

    def get_daily_feeds(self, user_id: int, day: date):
        day_str = day.strftime('%Y-%m-%d')
        res = (
            self.client.table("feeds")
            .select("amount_ml, timestamp")
            .eq("user_id", user_id)
            .gte("timestamp", f"{day_str}T00:00:00")
            .lte("timestamp", f"{day_str}T23:59:59")
            .execute()
        )
        return res.data if hasattr(res, 'data') else [] 