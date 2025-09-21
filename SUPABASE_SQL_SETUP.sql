-- Defence Engine Licenses Table Setup for Supabase
-- Copy and paste this entire SQL script into your Supabase SQL Editor

-- Step 1: Create the licenses table
CREATE TABLE IF NOT EXISTS licenses (
    id SERIAL PRIMARY KEY,
    license_key TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expiry_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    usage_count INTEGER DEFAULT 0,
    max_usage INTEGER DEFAULT -1,
    metadata JSONB
);

-- Step 2: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_licenses_key ON licenses(license_key);
CREATE INDEX IF NOT EXISTS idx_licenses_user ON licenses(user_id);
CREATE INDEX IF NOT EXISTS idx_licenses_active ON licenses(is_active);

-- Step 3: Enable Row Level Security (RLS)
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;

-- Step 4: Create policies for RLS
-- Allow anonymous users to read licenses (for validation)
CREATE POLICY "Allow anonymous read" ON licenses
    FOR SELECT USING (true);

-- Allow service role to insert, update, delete
CREATE POLICY "Allow service role all" ON licenses
    FOR ALL USING (auth.role() = 'service_role');

-- Step 5: Grant necessary permissions
GRANT SELECT ON licenses TO anon;
GRANT ALL ON licenses TO service_role;
GRANT USAGE ON SEQUENCE licenses_id_seq TO service_role;

-- Step 6: Insert a test license to verify the setup
INSERT INTO licenses (license_key, user_id, created_date, expiry_date, is_active, usage_count, max_usage, metadata)
VALUES (
    'DEF-TEST-1234-5678-9012',
    'test_user',
    NOW(),
    NOW() + INTERVAL '30 days',
    true,
    0,
    100,
    '{"generated_by": "defence_engine", "version": "4.0", "features": ["all_phases", "real_time_protection", "ai_detection"]}'::jsonb
);

-- Step 7: Verify the table was created successfully
SELECT 'Table created successfully!' as status;
SELECT COUNT(*) as license_count FROM licenses;
