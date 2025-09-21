# 🌐 **PURE SUPABASE SETUP - STEP BY STEP**

## ✅ **Your Supabase Credentials (Already Configured):**

- **Supabase URL:** `https://wuzjrpezzqgibkcsxigb.supabase.co`
- **Anon Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1empycGV6enFnaWJrY3N4aWdiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg0NTE5MzYsImV4cCI6MjA3NDAyNzkzNn0.NNXNNTEJybLoR7GjKhbCOrY_bVHqohLZBykAh5Fgv-c`
- **Service Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1empycGV6enFnaWJrY3N4aWdiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODQ1MTkzNiwiZXhwIjoyMDc0MDI3OTM2fQ.gRqvugB-dLKHJjdOi7WVCAkt7U-_NhSy84MJzTKD5Vw`

## 🚀 **Step 1: Create Licenses Table in Supabase**

### **Go to Supabase Dashboard:**
1. Open: https://supabase.com/dashboard
2. Click on your project: `wuzjrpezzqgibkcsxigb`
3. Go to **SQL Editor** (left sidebar)
4. Click **New Query**

### **Run This SQL:**
Copy and paste the **ENTIRE** contents of `SUPABASE_SQL_SETUP.sql` file:

```sql
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
```

5. Click **Run** button
6. You should see:
   - "Table created successfully!"
   - "1" (license count)

## 🧪 **Step 2: Test Connection**

After creating the table, run:
```bash
python supabase_pure_license_manager.py
```

You should see:
- ✅ Supabase connection successful!
- ✅ Test license generated: [license key]
- ✅ License validation: [validation result]

## 🎯 **Step 3: Generate Your First License**

```bash
python supabase_pure_license_generator.py
```

## 🏗️ **Step 4: Build Pure Supabase Executable**

```bash
python build_supabase.py
```

## 🧪 **Step 5: Test Executable**

```bash
dist\DefenceEngine_Supabase.exe --mode license --license-key YOUR_GENERATED_LICENSE
```

## 🎉 **You're Ready!**

Once you complete these steps, you'll have:
- ✅ Pure Supabase cloud-based license system
- ✅ Real-time validation via REST API
- ✅ No local database issues
- ✅ Professional cloud infrastructure

## 🎯 **What This Solves:**

### **✅ File Explorer Issue:**
- **No local database** - Uses Supabase cloud only
- **Works from anywhere** - No path issues
- **Real-time validation** - Instant cloud checking
- **Professional quality** - Cloud infrastructure

### **✅ Business Strategy:**
- **Cloud-based licensing** - More professional
- **Scalable system** - Handles multiple users
- **Secure authentication** - REST API with keys
- **Real-time management** - Instant updates

**🎯 Your Pure Supabase Defence Engine will be ready for your business strategy! 🛡️**
