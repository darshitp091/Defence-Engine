import time
import threading
from typing import Dict, List, Optional
from datetime import datetime

# Import Phase 5 components
from phases.phase5_social_engineering.email_analysis.email_analyzer import EmailAnalyzer
from phases.phase5_social_engineering.url_reputation.url_reputation_checker import URLReputationChecker
from phases.phase5_social_engineering.phishing_detection.phishing_detector import PhishingDetector
from phases.phase5_social_engineering.user_education.user_educator import UserEducator
from phases.phase5_social_engineering.communication_analysis.communication_analyzer import CommunicationAnalyzer

class Phase5Integration:
    def __init__(self):
        self.email_analyzer = EmailAnalyzer()
        self.url_reputation_checker = URLReputationChecker()
        self.phishing_detector = PhishingDetector()
        self.user_educator = UserEducator()
        self.communication_analyzer = CommunicationAnalyzer()
        
        print("✅ Phase 5 Social Engineering Protection initialized!")
        print("   - Email Analysis")
        print("   - URL Reputation Checking")
        print("   - Phishing Detection")
        print("   - User Education")
        print("   - Communication Analysis")

    def start_phase5_protection(self):
        print("\n🎯 Starting Phase 5 Social Engineering Protection Components...")
        
        print("   📧 Starting Email Analysis...")
        self.email_analyzer.start_analysis()
        
        print("   🌐 Starting URL Reputation Checking...")
        self.url_reputation_checker.start_checking()
        
        print("   🎣 Starting Phishing Detection...")
        self.phishing_detector.start_detection()
        
        print("   🎓 Starting User Education...")
        self.user_educator.start_education()
        
        print("   💬 Starting Communication Analysis...")
        self.communication_analyzer.start_analysis()
        
        print("✅ Phase 5 Social Engineering Protection Active!")
        print("   - Email Analysis: ACTIVE")
        print("   - URL Reputation Checking: ACTIVE")
        print("   - Phishing Detection: ACTIVE")
        print("   - User Education: ACTIVE")
        print("   - Communication Analysis: ACTIVE")

    def stop_phase5_protection(self):
        print("\n⏹️ Stopping Phase 5 Social Engineering Protection Components...")
        
        self.email_analyzer.stop_analysis()
        self.url_reputation_checker.stop_checking()
        self.phishing_detector.stop_detection()
        self.user_educator.stop_education()
        self.communication_analyzer.stop_analysis()
        
        print("✅ Phase 5 Social Engineering Protection Stopped!")

    def get_phase5_report(self) -> Dict:
        """Get comprehensive Phase 5 protection report"""
        email_stats = self.email_analyzer.get_analysis_statistics()
        url_stats = self.url_reputation_checker.get_reputation_statistics()
        phishing_stats = self.phishing_detector.get_detection_statistics()
        education_stats = self.user_educator.get_education_statistics()
        communication_stats = self.communication_analyzer.get_analysis_statistics()
        
        # Calculate overall social engineering protection health
        social_engineering_protection_health = 100
        if email_stats.get('suspicious_emails_detected', 0) > 0:
            social_engineering_protection_health -= 15
        if url_stats.get('suspicious_urls_detected', 0) > 0:
            social_engineering_protection_health -= 10
        if phishing_stats.get('phishing_emails_detected', 0) > 0:
            social_engineering_protection_health -= 20
        if communication_stats.get('suspicious_communications_detected', 0) > 0:
            social_engineering_protection_health -= 15
        
        social_engineering_protection_health = max(0, social_engineering_protection_health)
        
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'social_engineering_protection_health': social_engineering_protection_health,
            'email_analysis': email_stats,
            'url_reputation': url_stats,
            'phishing_detection': phishing_stats,
            'user_education': education_stats,
            'communication_analysis': communication_stats,
            'total_suspicious_emails': email_stats.get('suspicious_emails_detected', 0),
            'total_suspicious_urls': url_stats.get('suspicious_urls_detected', 0),
            'total_phishing_emails': phishing_stats.get('phishing_emails_detected', 0),
            'total_suspicious_communications': communication_stats.get('suspicious_communications_detected', 0),
            'active_protections': sum([
                email_stats.get('analysis_active', False),
                url_stats.get('checking_active', False),
                phishing_stats.get('detection_active', False),
                education_stats.get('education_active', False),
                communication_stats.get('analysis_active', False)
            ])
        }

    def test_phase5_components(self):
        print("\n🧪 TESTING PHASE 5 COMPONENTS")
        print("============================================================")
        
        # Test Email Analysis
        print("📧 Testing Email Analysis...")
        test_email = {
            'id': 'test_email_1',
            'sender': 'suspicious@malware.com',
            'subject': 'Urgent Action Required',
            'body': 'Click here to verify your account immediately!',
            'links': ['http://bit.ly/suspicious'],
            'attachments': [{'filename': 'malware.exe', 'size': 1024000}]
        }
        email_analysis = self.email_analyzer.analyze_email(test_email)
        print(f"   ✅ Email Analysis: Suspicious Score {email_analysis.get('suspicious_score', 0)}/100")
        
        # Test URL Reputation Checking
        print("🌐 Testing URL Reputation Checking...")
        test_url = "http://suspicious-malware-site.com/phishing"
        url_reputation = self.url_reputation_checker.check_url_reputation(test_url)
        print(f"   ✅ URL Reputation: Score {url_reputation.get('reputation_score', 0)}/100")
        
        # Test Phishing Detection
        print("🎣 Testing Phishing Detection...")
        test_phishing_email = {
            'id': 'test_phishing_1',
            'sender': 'bank@fake-bank.com',
            'subject': 'Verify Your Account',
            'body': 'Click here to verify your account or it will be suspended!',
            'links': ['http://fake-bank.com/verify'],
            'attachments': []
        }
        phishing_detection = self.phishing_detector.detect_phishing(test_phishing_email)
        print(f"   ✅ Phishing Detection: Score {phishing_detection.get('phishing_score', 0)}/100")
        
        # Test User Education
        print("🎓 Testing User Education...")
        education_session = self.user_educator.educate_user('test_user', 'phishing_awareness')
        print(f"   ✅ Education Session: Completed = {education_session.get('education_completed', False)}")
        
        # Test Communication Analysis
        print("💬 Testing Communication Analysis...")
        test_communication = {
            'id': 'test_comm_1',
            'type': 'email',
            'sender': 'attacker@malware.com',
            'recipient': 'victim@company.com',
            'subject': 'Urgent Security Update',
            'content': 'Download this security update immediately!',
            'links': ['http://malware.com/update.exe'],
            'attachments': [{'filename': 'update.exe', 'size': 2048000}],
            'metadata': {'ip_address': '192.168.1.100', 'user_agent': 'Mozilla/5.0'}
        }
        communication_analysis = self.communication_analyzer.analyze_communication(test_communication)
        print(f"   ✅ Communication Analysis: Score {communication_analysis.get('suspicious_score', 0)}/100")
        
        print("✅ Phase 5 Component Testing Completed!")
        print("============================================================")

    def simulate_social_engineering_attacks(self):
        """Simulate various social engineering attacks for testing"""
        print("\n🎯 SIMULATING SOCIAL ENGINEERING ATTACKS FOR TESTING")
        print("============================================================")
        
        # Simulate phishing emails
        print("📧 Simulating Phishing Emails...")
        for i in range(3):
            phishing_email = {
                'id': f'phishing_email_{i}',
                'sender': f'bank{i}@fake-bank.com',
                'subject': f'Urgent: Verify Your Account #{i}',
                'body': f'Click here to verify your account or it will be suspended! This is your final notice #{i}.',
                'links': [f'http://fake-bank{i}.com/verify'],
                'attachments': []
            }
            email_analysis = self.email_analyzer.analyze_email(phishing_email)
            print(f"   Phishing Email {i+1}: Suspicious Score {email_analysis.get('suspicious_score', 0)}/100")
        
        # Simulate suspicious URLs
        print("🌐 Simulating Suspicious URLs...")
        for i in range(2):
            suspicious_url = f"http://malware-site{i}.com/download"
            url_reputation = self.url_reputation_checker.check_url_reputation(suspicious_url)
            print(f"   Suspicious URL {i+1}: Reputation Score {url_reputation.get('reputation_score', 0)}/100")
        
        # Simulate social engineering communications
        print("💬 Simulating Social Engineering Communications...")
        for i in range(4):
            social_engineering_comm = {
                'id': f'se_comm_{i}',
                'type': 'email',
                'sender': f'attacker{i}@malware.com',
                'recipient': f'victim{i}@company.com',
                'subject': f'Urgent: Security Breach Detected #{i}',
                'content': f'Your account has been compromised! Click here to secure it immediately! #{i}',
                'links': [f'http://malware{i}.com/secure'],
                'attachments': [{'filename': f'security_update{i}.exe', 'size': 1024000}],
                'metadata': {'ip_address': f'192.168.1.{100+i}', 'user_agent': 'Mozilla/5.0'}
            }
            communication_analysis = self.communication_analyzer.analyze_communication(social_engineering_comm)
            print(f"   Social Engineering Comm {i+1}: Suspicious Score {communication_analysis.get('suspicious_score', 0)}/100")
        
        # Simulate user education
        print("🎓 Simulating User Education...")
        for i in range(2):
            education_session = self.user_educator.educate_user(f'user_{i}', 'phishing_awareness')
            print(f"   Education Session {i+1}: Completed = {education_session.get('education_completed', False)}")
        
        print("✅ Social Engineering Attack Simulation Completed!")
        print("============================================================")

    def emergency_social_engineering_response(self):
        """Emergency response to social engineering attacks"""
        print("\n🚨 EMERGENCY SOCIAL ENGINEERING RESPONSE ACTIVATED!")
        print("============================================================")
        
        # Activate emergency protocols
        print("🚨 Activating Emergency Protocols...")
        
        # Emergency email lockdown
        print("📧 Activating Emergency Email Lockdown...")
        self.email_analyzer.emergency_email_lockdown()
        
        # Emergency URL lockdown
        print("🌐 Activating Emergency URL Lockdown...")
        self.url_reputation_checker.emergency_url_lockdown()
        
        # Emergency phishing response
        print("🎣 Activating Emergency Phishing Response...")
        self.phishing_detector.emergency_phishing_lockdown()
        
        # Emergency communication lockdown
        print("💬 Activating Emergency Communication Lockdown...")
        self.communication_analyzer.emergency_communication_lockdown()
        
        # Emergency education activation
        print("🎓 Activating Emergency Education...")
        self.user_educator.emergency_education_activation()
        
        print("✅ Emergency Social Engineering Response Completed!")
        print("============================================================")

    def restore_normal_operation(self):
        """Restore normal operation after emergency response"""
        print("\n✅ RESTORING NORMAL OPERATION")
        print("============================================================")
        
        # Restore normal email operation
        print("📧 Restoring Normal Email Operation...")
        self.email_analyzer.restore_normal_operation()
        
        # Restore normal URL operation
        print("🌐 Restoring Normal URL Operation...")
        self.url_reputation_checker.restore_normal_operation()
        
        # Restore normal phishing detection
        print("🎣 Restoring Normal Phishing Detection...")
        self.phishing_detector.restore_normal_operation()
        
        # Restore normal communication analysis
        print("💬 Restoring Normal Communication Analysis...")
        self.communication_analyzer.restore_normal_operation()
        
        # Restore normal education
        print("🎓 Restoring Normal Education...")
        self.user_educator.restore_normal_education()
        
        print("✅ Normal Operation Restored!")
        print("============================================================")

def main():
    print("🎯 PHASE 5 - SOCIAL ENGINEERING PROTECTION TESTING")
    print("============================================================")
    
    print("🎯 PHASE 5 - SOCIAL ENGINEERING PROTECTION INITIALIZATION")
    print("============================================================")
    
    phase5 = Phase5Integration()
    phase5.test_phase5_components()
    
    phase5.start_phase5_protection()
    print("\n⏱️ Running Phase 5 protection for 30 seconds...")
    time.sleep(30)
    
    phase5.simulate_social_engineering_attacks()
    
    phase5.stop_phase5_protection()
    
    report = phase5.get_phase5_report()
    print("\n📊 PHASE 5 INTEGRATION REPORT", report['timestamp'])
    print("============================================================")
    print(f"🎯 Social Engineering Protection Health: {report['social_engineering_protection_health']}/100")
    print(f"📧 Suspicious Emails: {report['email_analysis']['suspicious_emails_detected']}")
    print(f"🌐 Suspicious URLs: {report['url_reputation']['suspicious_urls_detected']}")
    print(f"🎣 Phishing Emails: {report['phishing_detection']['phishing_emails_detected']}")
    print(f"💬 Suspicious Communications: {report['communication_analysis']['suspicious_communications_detected']}")
    print(f"🎓 Education Sessions: {report['user_education']['education_sessions_completed']}")
    print(f"🚨 Total Threats Detected: {report['total_suspicious_emails'] + report['total_suspicious_urls'] + report['total_phishing_emails'] + report['total_suspicious_communications']}")
    print(f"🔒 Active Protections: {report['active_protections']}/5")
    print("============================================================")
    
    print("\n📊 PHASE 5 STATISTICS:")
    print(f"   Email Analysis: {report['email_analysis']['analysis_active']}")
    print(f"   URL Reputation: {report['url_reputation']['checking_active']}")
    print(f"   Phishing Detection: {report['phishing_detection']['detection_active']}")
    print(f"   User Education: {report['user_education']['education_active']}")
    print(f"   Communication Analysis: {report['communication_analysis']['analysis_active']}")
    
    print("\n✅ Phase 5 Social Engineering Protection Testing Completed!")
    print("============================================================")

if __name__ == "__main__":
    main()
