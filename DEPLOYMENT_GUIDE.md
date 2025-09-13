# Defence Engine - Deployment Guide

## Quick Start

### 1. Installation
```bash
# Clone or extract Defence Engine files
# Navigate to the Defence Engine directory
python install.py
```

### 2. Generate License Keys
```bash
# Run license generator
python defence_engine.py --mode license

# Or directly
python license_generator.py
```

### 3. Launch Application
```bash
# GUI Mode (recommended for first-time users)
python defence_engine.py

# Service Mode (for continuous protection)
python defence_engine.py --mode service --license-key YOUR_LICENSE_KEY --api-key YOUR_GEMINI_API_KEY
```

## Detailed Deployment Options

### Option 1: GUI Application (Recommended)

**Best for:** Individual users, testing, demonstration

**Steps:**
1. Run `python defence_engine.py`
2. Enter your license key and Gemini API key
3. System starts with full GUI dashboard
4. Monitor threats and control defenses through interface

**Advantages:**
- User-friendly interface
- Real-time monitoring dashboard
- Manual control over all features
- Easy to understand system status

### Option 2: Background Service

**Best for:** Continuous protection, server deployment, enterprise use

**Steps:**
1. Generate license key using license generator
2. Obtain Gemini API key from Google AI Studio
3. Run: `python defence_engine.py --mode service --license-key YOUR_KEY --api-key YOUR_API_KEY`
4. Service runs continuously in background

**Advantages:**
- No user interaction required
- Continuous protection
- Automatic startup and recovery
- Minimal resource usage

### Option 3: Windows Service Installation

**For permanent system protection:**

1. Create service wrapper script:
```python
# service_wrapper.py
import sys
import os
from service.background_service import DefenceBackgroundService

LICENSE_KEY = "YOUR_LICENSE_KEY_HERE"
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

service = DefenceBackgroundService(LICENSE_KEY, API_KEY)
service.run_forever()
```

2. Install as Windows service using tools like NSSM or create Windows service installer

## License Management

### Generating License Keys

**Single License:**
```bash
python licence_generator.py
# Select option 1
# Enter user details
```

**Bulk Licenses:**
```bash
python licence_generator.py
# Select option 2
# Specify quantity and prefix
```

**License Types:**
- **Time-based**: Expires after specified days
- **Usage-based**: Limited number of activations
- **Unlimited**: No expiry or usage limits
- **Combined**: Both time and usage limits

### License Key Format
```
DEF-XXXXXXXX-XXXXXXXX-XXXXXXXX
```
- Prefix: DEF (Defence Engine)
- 3 segments of 8 characters each
- Cryptographically secure generation
- Unique per user and timestamp

## API Key Setup

### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy the key for use in Defence Engine
4. Keep the key secure and don't share it

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- Sufficient for continuous monitoring

## Configuration Options

### System Configuration
Edit configuration in service/background_service.py:

```python
self.config = {
    'monitoring_interval': 5,        # Monitoring frequency (seconds)
    'pattern_rotation_interval': 300, # Pattern rotation (seconds)
    'log_cleanup_interval': 3600,    # Log cleanup (seconds)
    'max_log_size': 10 * 1024 * 1024, # Max log file size (bytes)
}
```

### Threat Detection Sensitivity
Adjust in ai/threat_detector.py:
```python
self.threat_threshold = 0.7  # Threat detection sensitivity (0.0-1.0)
```

### Defense Response Levels
Configure in defense/reverse_attack.py:
```python
barrier_config = {
    'max_connections_per_ip': 10,    # Max connections per IP
    'rate_limit_window': 60,         # Rate limit window (seconds)
    'auto_ban_threshold': 50,        # Auto-ban threshold
    'hash_rotation_interval': 30     # Hash rotation interval
}
```

## Monitoring and Maintenance

### Log Files
- `logs/service.log` - Service operations and status
- `logs/threats.log` - Detected threats and responses
- `logs/errors.log` - Error messages and recovery actions
- `logs/system_status.json` - Current system status

### Health Monitoring
The system performs automatic health checks:
- Memory usage monitoring
- Component status verification
- Log file size management
- License validity checking

### Maintenance Tasks
- **Log Rotation**: Automatic when files exceed 10MB
- **Pattern Rotation**: Every 5 minutes automatically
- **Health Checks**: Every minute
- **License Validation**: Every monitoring cycle

## Troubleshooting

### Common Issues

**1. License Validation Failed**
- Check license key format
- Verify license hasn't expired
- Ensure license hasn't exceeded usage limits

**2. AI Detection Not Working**
- Verify Gemini API key is valid
- Check internet connection
- Monitor API usage limits

**3. High Resource Usage**
- Adjust monitoring intervals
- Enable log cleanup
- Check for memory leaks in logs

**4. Service Won't Start**
- Check Python installation
- Verify all dependencies installed
- Review error logs for specific issues

### Debug Mode
Enable detailed logging by modifying log levels:
```python
# In any component
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Best Practices

### License Key Security
- Store license keys securely
- Don't share license keys
- Revoke compromised licenses immediately
- Use separate licenses for different deployments

### API Key Security
- Keep Gemini API keys confidential
- Rotate API keys regularly
- Monitor API usage for anomalies
- Use environment variables for keys in production

### System Security
- Run with minimal required privileges
- Keep system and Python updated
- Monitor log files for security events
- Regular backup of license database

## Performance Optimization

### Resource Usage
- **CPU**: Typically <5% on modern systems
- **Memory**: <100MB during normal operation
- **Disk**: Minimal, mainly for logs
- **Network**: Only for AI API calls

### Optimization Tips
- Increase monitoring intervals for lower resource usage
- Enable log compression for storage efficiency
- Use SSD storage for better performance
- Ensure adequate RAM for AI processing

## Enterprise Deployment

### Centralized Management
- Deploy license server for multiple installations
- Centralized logging and monitoring
- Custom configuration management
- Integration with existing security infrastructure

### Scaling Considerations
- Multiple instances for high availability
- Load balancing for API requests
- Distributed threat intelligence sharing
- Custom threat detection rules

### Compliance
- Audit trail maintenance
- Security event reporting
- Compliance with security standards
- Regular security assessments

## Support and Updates

### Getting Help
- Check log files for error details
- Review this documentation
- Verify system requirements
- Test with minimal configuration

### Updates
- Regular updates for threat detection
- Security patches and improvements
- New feature releases
- Compatibility updates

### Backup and Recovery
- Backup license database regularly
- Export important configuration
- Document custom modifications
- Test recovery procedures