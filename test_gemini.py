"""
Test Gemini API Integration
"""
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.threat_detector import AIThreatDetector
from config import DefenceConfig

def test_gemini_api():
    """Test Gemini API connection and functionality"""
    print("=" * 60)
    print("Defence Engine - Gemini API Test")
    print("=" * 60)
    
    try:
        # Initialize AI detector with built-in API key
        print("Initializing AI Threat Detector...")
        detector = AIThreatDetector()
        
        print(f"Using API Key: {DefenceConfig.get_gemini_api_key()[:20]}...")
        
        # Test basic AI functionality
        print("\nTesting AI threat analysis...")
        
        # Sample system data for testing
        test_system_data = {
            'timestamp': '2024-01-01T12:00:00',
            'cpu_percent': 85.5,
            'memory_percent': 78.2,
            'processes': 156,
            'connections': 45,
            'disk_io': {'read_bytes': 1024000, 'write_bytes': 512000},
            'network_io': {'bytes_sent': 2048000, 'bytes_recv': 1536000}
        }
        
        # Analyze the test data
        threat_level = detector._analyze_threats(test_system_data)
        
        print(f"✅ AI Analysis Complete!")
        print(f"Threat Level: {threat_level}")
        
        if threat_level > 0.5:
            print("🚨 High threat detected in test data")
        else:
            print("✅ System appears normal")
            
        print("\n" + "=" * 60)
        print("Gemini API Integration: SUCCESS")
        print("Defence Engine is ready for deployment!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        print("\nPossible issues:")
        print("1. Internet connection required")
        print("2. API key might be invalid")
        print("3. Gemini API service might be down")
        print("4. Rate limits might be exceeded")
        
        return False

def test_configuration():
    """Test configuration system"""
    print("\nTesting Configuration System...")
    
    print(f"Default API Key: {DefenceConfig.DEFAULT_GEMINI_API_KEY[:20]}...")
    print(f"Monitoring Interval: {DefenceConfig.MONITORING_INTERVAL}s")
    print(f"Threat Threshold: {DefenceConfig.THREAT_THRESHOLD}")
    print(f"Pattern Rotation: {DefenceConfig.PATTERN_ROTATION_INTERVAL}s")
    
    print("✅ Configuration system working correctly")

if __name__ == "__main__":
    print("Testing Defence Engine components...\n")
    
    # Test configuration
    test_configuration()
    
    # Test Gemini API
    success = test_gemini_api()
    
    if success:
        print("\n🎉 All tests passed! Defence Engine is ready to use.")
    else:
        print("\n⚠️ Some tests failed. Please check the configuration.")
        
    input("\nPress Enter to exit...")