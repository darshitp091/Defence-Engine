# 🚀 **STEP-BY-STEP SUPABASE SETUP**

## ✅ **Your Supabase is Connected!**

The connection test shows your Supabase is working, but we need to create the licenses table.

## 📋 **Step 1: Create Licenses Table**

### **Go to Supabase Dashboard:**
1. Open: https://supabase.com/dashboard
2. Click on your project: `wuzjrpezzqgibkcsxigb`
3. Go to **SQL Editor** (left sidebar)
4. Click **New Query**

### **Run This SQL:**
Copy and paste this entire SQL script:

```sql
-- Defence Engine Licenses Table Setup
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

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_licenses_key ON licenses(license_key);
CREATE INDEX IF NOT EXISTS idx_licenses_user ON licenses(user_id);

-- Enable RLS
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Allow anonymous read" ON licenses FOR SELECT USING (true);
CREATE POLICY "Allow service role all" ON licenses FOR ALL USING (auth.role() = 'service_role');

-- Grant permissions
GRANT SELECT ON licenses TO anon;
GRANT ALL ON licenses TO service_role;
GRANT USAGE ON SEQUENCE licenses_id_seq TO service_role;

-- Insert test license
INSERT INTO licenses (license_key, user_id, created_date, expiry_date, is_active, usage_count, max_usage, metadata)
VALUES (
    'DEF-TEST-1234-5678-9012',
    'test_user',
    NOW(),
    NOW() + INTERVAL '30 days',
    true,
    0,
    100,
    '{"generated_by": "defence_engine", "version": "4.0"}'::jsonb
);

-- Verify
SELECT 'Table created successfully!' as status;
SELECT COUNT(*) as license_count FROM licenses;
```

5. Click **Run** button
6. You should see "Table created successfully!" and "1" license count

## 🧪 **Step 2: Test Connection**

After creating the table, run:
```bash
python test_supabase_connection.py
```

You should see:
- ✅ Supabase connection successful!
- ✅ Licenses table accessible!
- 📋 Found 1 licenses in database

## 🎯 **Step 3: Generate Your First License**

```bash
python supabase_license_generator.py
```

## 🏗️ **Step 4: Build Supabase Executable**

```bash
python build_supabase.py
```

## 🧪 **Step 5: Test Executable**

```bash
dist\DefenceEngine_Supabase.exe --mode license --license-key YOUR_GENERATED_LICENSE
```

## 🎉 **You're Ready!**

Once you complete these steps, you'll have:
- ✅ Cloud-based license system
- ✅ Real-time validation
- ✅ No local database issues
- ✅ Professional executable

**🎯 Your Supabase Defence Engine will be ready for your business strategy! 🛡️**
