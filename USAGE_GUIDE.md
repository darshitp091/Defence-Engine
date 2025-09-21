# Defence Engine - Client Generator Usage Guide

## 🎯 Quick Start Commands

### 1. Interactive Generator (Easiest)
```bash
python generate_client_app.py
```
This will ask you questions step by step.

### 2. Windows Batch File
```bash
generate_client.bat
```
Double-click or run from command prompt.

### 3. Quick Command Line
```bash
python quick_generate.py "Client Name" "Company" "email@company.com" 30 100 demo
```

### 4. Full Command Line
```bash
python client_gui_generator.py --client-name "Client Name" --company "Company" --email "email@company.com" --expiry-days 30 --max-usage 100 --demo
```

## 📋 Examples

### Generate Demo for Sales
```bash
python quick_generate.py "Sales Demo" "Prospect Corp" "sales@prospect.com" 7 10 demo
```

### Generate Trial License
```bash
python quick_generate.py "Trial User" "TechCorp" "trial@techcorp.com" 14 50
```

### Generate Full License
```bash
python quick_generate.py "John Smith" "Enterprise Inc" "john@enterprise.com" 365 -1
```

## 🔧 What Happens When You Generate

1. **License Creation**: A unique license key is generated
2. **Package Creation**: A complete folder is created with all files
3. **Customization**: The GUI is personalized for the client
4. **Documentation**: README and user manual are generated
5. **Installation Scripts**: Windows and Linux installers are created

## 📦 Generated Package Contents

```
client_packages/
└── ClientName_YYYYMMDD_HHMMSS/
    ├── run_defence_engine.py          # 🚀 Main launcher
    ├── install.bat                    # ⚙️ Windows installer
    ├── install.sh                     # ⚙️ Linux/Mac installer
    ├── requirements.txt               # 📋 Dependencies
    ├── config.py                      # ⚙️ Configuration
    ├── core/                          # 🔧 Core engine
    ├── ai/                           # 🤖 AI components
    ├── defense/                      # 🛡️ Defense systems
    ├── license/                      # 🔐 License system
    ├── service/                      # 🔄 Background services
    ├── gui/
    │   └── client_app.py             # 🎨 Custom GUI
    └── docs/
        ├── README.md                 # 📚 Client docs
        └── USER_MANUAL.md            # 📖 User manual
```

## 🎯 Client Experience

### Step 1: License Verification
When the client runs the application:
- They see a welcome screen with their name
- They enter their license key
- The system validates the license
- If valid, they proceed to the main application

### Step 2: Main Application
After license validation:
- Full Defence Engine GUI opens
- All features are available
- Real-time monitoring starts
- License information is displayed

### Step 3: Demo Mode (if enabled)
If demo mode is selected:
- Limited functionality is available
- Clear demo indicators are shown
- Contact information for full license is provided

## 🔐 License System Features

### Security
- **Cryptographic Signing**: Each license is cryptographically signed
- **Blockchain Validation**: Advanced blockchain-based verification
- **Usage Tracking**: Monitors how many times the license is used
- **Expiry Control**: Automatic expiration after set period
- **Tamper Detection**: Prevents license modification

### Flexibility
- **Custom Expiry**: Set any expiry period (days)
- **Usage Limits**: Control maximum usage count
- **Demo Mode**: Create limited functionality versions
- **Company Branding**: Include company information
- **Contact Details**: Add client contact information

## 📱 Testing Your Generated Package

### 1. Navigate to Package
```bash
cd client_packages/ClientName_YYYYMMDD_HHMMSS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python run_defence_engine.py
```

### 4. Test License
- Enter the generated license key
- Verify the application starts
- Check all features work
- Test demo mode (if enabled)

## 🚀 Distribution to Clients

### Method 1: Zip Package
1. Zip the entire client package folder
2. Send to client via email/cloud
3. Client extracts and runs

### Method 2: Direct Folder
1. Copy the entire package folder
2. Transfer via USB/network
3. Client runs from folder

### Method 3: Cloud Storage
1. Upload package to cloud storage
2. Share download link with client
3. Client downloads and runs

## 💡 Best Practices

### For You (Developer)
- **Test Each Package**: Always test generated packages
- **Use Descriptive Names**: Clear client identification
- **Set Appropriate Limits**: Reasonable expiry and usage limits
- **Include Documentation**: Generated docs are comprehensive
- **Keep License Keys**: Store for support purposes

### For Your Clients
- **Read Documentation**: Generated README and manual
- **Install Dependencies**: Run install scripts first
- **Keep License Secure**: Don't share license keys
- **Contact Support**: Use provided contact information
- **Regular Updates**: Check for updates with valid license

## 🔧 Troubleshooting

### Common Issues

**Package Won't Generate**
- Check Python version (3.8+ required)
- Ensure all dependencies are installed
- Verify file permissions

**Client App Won't Start**
- Check Python installation
- Install requirements: `pip install -r requirements.txt`
- Verify all files are present

**License Validation Fails**
- Check internet connection
- Verify license key is correct
- Ensure license hasn't expired

**Import Errors**
- Reinstall dependencies
- Check Python path
- Verify file structure

### Getting Help
- Check generated documentation
- Review error messages carefully
- Contact support with details
- Include license key in support requests

## 📊 License Management

### View All Licenses
```bash
python license_generator.py
# Select option 4: List all licenses
```

### Check License Status
```bash
python license_generator.py
# Select option 3: View license info
```

### Revoke License
```bash
python license_generator.py
# Select option 5: Revoke license
```

## 🎯 Use Cases

### Sales Demos
- Generate demo versions with limited features
- Set short expiry (7-14 days)
- Include contact information for full license

### Trial Licenses
- Create evaluation versions
- Set moderate expiry (30-90 days)
- Include usage limits for testing

### Corporate Licenses
- Generate full-featured versions
- Set long expiry (1 year+)
- Include company branding

### Training Versions
- Create educational versions
- Set appropriate limits
- Include training materials

---

## 📞 Support

For technical support or questions:
- Check the generated documentation
- Review this usage guide
- Contact support with license details
- Include error messages and system information

---

**© 2024 Defence Engine. All rights reserved.**
