import os
from datetime import date
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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

    def set_user_timezone(self, user_id: int, timezone: str):
        """Set or update the timezone for a user"""
        try:
            data = {
                "user_id": user_id,
                "timezone": timezone,
            }
            # Use upsert to insert or update
            return self.supabase.table("user_settings").upsert(data).execute()
        except Exception as e:
            # Log the error but don't crash
            print(f"Error setting user timezone: {e}")
            return None

    def get_user_timezone(self, user_id: int):
        """Get the timezone for a user, returns None if not set"""
        try:
            response = (
                self.supabase.table("user_settings")
                .select("timezone")
                .eq("user_id", user_id)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                return response.data[0].get("timezone")
            return None
        except Exception as e:
            # Log the error but don't crash
            print(f"Error getting user timezone: {e}")
            return None

    def set_user_language(self, user_id: int, language: str):
        """Set or update the language for a user"""
        try:
            # Get existing settings first
            existing = (
                self.supabase.table("user_settings")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            
            if existing.data:
                # Update existing record
                data = existing.data[0]
                data["language"] = language
                return self.supabase.table("user_settings").update(data).eq("user_id", user_id).execute()
            else:
                # Create new record
                data = {
                    "user_id": user_id,
                    "language": language,
                }
                return self.supabase.table("user_settings").insert(data).execute()
        except Exception as e:
            # Log the error but don't crash
            print(f"Error setting user language: {e}")
            return None

    def get_user_language(self, user_id: int):
        """Get the language for a user, returns None if not set"""
        try:
            response = (
                self.supabase.table("user_settings")
                .select("language")
                .eq("user_id", user_id)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                return response.data[0].get("language")
            return None
        except Exception as e:
            # Log the error but don't crash
            print(f"Error getting user language: {e}")
            return None
