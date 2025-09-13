"""
Defence Engine Configuration
"""
import os
from pathlib import Path

class DefenceConfig:
    """Configuration management for Defence Engine"""
    
    # Default Gemini API Key
    DEFAULT_GEMINI_API_KEY = "AIzaSyBBDP4NnmxGA8bJc8DsSd_WOI5QwZCsF6o"
    
    # System Configuration
    MONITORING_INTERVAL = 5  # seconds
    PATTERN_ROTATION_INTERVAL = 300  # 5 minutes
    LOG_CLEANUP_INTERVAL = 3600  # 1 hour
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Threat Detection Configuration
    THREAT_THRESHOLD = 0.7  # 0.0 to 1.0
    HIGH_THREAT_THRESHOLD = 0.9
    MEDIUM_THREAT_THRESHOLD = 0.7
    
    # Defense Configuration
    MAX_CONNECTIONS_PER_IP = 10
    RATE_LIMIT_WINDOW = 60  # seconds
    AUTO_BAN_THRESHOLD = 50
    HASH_ROTATION_INTERVAL = 30  # seconds
    
    # Hash Engine Configuration
    OBFUSCATION_LAYERS = 5
    HASH_TRAP_COUNT = 1000
    
    # License Configuration
    DEFAULT_LICENSE_EXPIRY_DAYS = 365
    DEFAULT_MAX_USAGE = -1  # unlimited
    
    @classmethod
    def get_gemini_api_key(cls):
        """Get Gemini API key from environment or default"""
        return os.getenv('GEMINI_API_KEY', cls.DEFAULT_GEMINI_API_KEY)
    
    @classmethod
    def get_config_dir(cls):
        """Get configuration directory"""
        config_dir = Path.home() / '.defence_engine'
        config_dir.mkdir(exist_ok=True)
        return config_dir
    
    @classmethod
    def get_logs_dir(cls):
        """Get logs directory"""
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        return logs_dir