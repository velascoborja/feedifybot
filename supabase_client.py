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
        try:
            # First, let's get all feeds to see what columns exist
            response = (
                self.supabase.table("feeds")
                .select("*")
                .eq("user_id", user_id)
                .limit(1)
                .execute()
            )
            
            if response.data:
                print(f"Available columns in feeds table: {list(response.data[0].keys())}")
            
            # Get all feeds for this user
            response = (
                self.supabase.table("feeds")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            
            all_feeds = response.data if response.data else []
            print(f"Total feeds found for user {user_id}: {len(all_feeds)}")
            
            # If no timestamp column exists, return all feeds for now
            if not all_feeds:
                return []
            
            # Check what date/time columns are available
            sample_feed = all_feeds[0]
            date_columns = []
            for key in sample_feed.keys():
                if any(word in key.lower() for word in ['created', 'date', 'time', 'timestamp']):
                    date_columns.append(key)
            
            print(f"Potential date columns found: {date_columns}")
            
            # If no date column found, return all feeds (needs manual filtering)
            if not date_columns:
                print("No date columns found, returning all feeds")
                return all_feeds
            
            # Try to filter by the first date column found
            date_column = date_columns[0]
            day_str = day.isoformat()
            
            today_feeds = []
            for feed in all_feeds:
                date_value = feed.get(date_column, '')
                if date_value:
                    try:
                        # Extract date part
                        if 'T' in str(date_value):
                            feed_date = str(date_value).split('T')[0]
                        elif ' ' in str(date_value):
                            feed_date = str(date_value).split(' ')[0]
                        else:
                            feed_date = str(date_value)
                        
                        if feed_date == day_str:
                            today_feeds.append(feed)
                    except Exception as e:
                        continue
            
            print(f"Feeds found for {day_str}: {len(today_feeds)}")
            return today_feeds
            
        except Exception as e:
            print(f"Error getting daily feeds: {e}")
            return []

    def get_all_user_feeds(self, user_id: int):
        """Get all feeds for a user (for debugging)"""
        try:
            response = (
                self.supabase.table("feeds")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting all user feeds: {e}")
            return []

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

    def set_user_reminder_time(self, user_id: int, reminder_time: str):
        """Set or update the reminder time for a user (HH:MM format)"""
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
                data["reminder_time"] = reminder_time
                return self.supabase.table("user_settings").update(data).eq("user_id", user_id).execute()
            else:
                # Create new record
                data = {
                    "user_id": user_id,
                    "reminder_time": reminder_time,
                }
                return self.supabase.table("user_settings").insert(data).execute()
        except Exception as e:
            # Log the error but don't crash
            print(f"Error setting user reminder time: {e}")
            return None

    def get_user_reminder_time(self, user_id: int):
        """Get the reminder time for a user, returns None if not set"""
        try:
            response = (
                self.supabase.table("user_settings")
                .select("reminder_time")
                .eq("user_id", user_id)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                return response.data[0].get("reminder_time")
            return None
        except Exception as e:
            # Log the error but don't crash
            print(f"Error getting user reminder time: {e}")
            return None
