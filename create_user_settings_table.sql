-- SQL script to create the user_settings table in Supabase
-- Run this in your Supabase SQL editor

CREATE TABLE IF NOT EXISTS user_settings (
    user_id BIGINT PRIMARY KEY,
    timezone TEXT,
    language TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index for faster queries
CREATE INDEX IF NOT EXISTS idx_user_settings_user_id ON user_settings(user_id);

-- Enable Row Level Security (RLS) if needed
-- ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;

-- Optional: Create a policy to allow users to only access their own settings
-- CREATE POLICY "Users can access their own settings" ON user_settings
--     FOR ALL USING (auth.uid()::text = user_id::text);
