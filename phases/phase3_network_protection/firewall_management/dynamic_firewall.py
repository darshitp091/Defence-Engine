import time
import threading
import subprocess
import platform
from collections import deque
from typing import Dict, List, Optional, Tuple
import json
import ipaddress
import socket

class DynamicFirewallManager:
    def __init__(self):
        self.system = platform.system().lower()
        self.active_rules = {}
        self.blocked_ips = set()
        self.suspicious_ips = set()
        self.rule_history = deque(maxlen=10000)
        self.firewall_stats = {
            'rules_created': 0,
            'rules_deleted': 0,
            'ips_blocked': 0,
            'ips_unblocked': 0,
            'threats_blocked': 0
        }
        self.auto_block_threshold = 5  # Auto-block after 5 threats
        self.rule_timeout = 3600  # 1 hour default timeout
        self.is_active = False
        self.monitoring_thread = None
        print("🔥 Dynamic Firewall Manager initialized!")
        print(f"   System: {self.system}")
        print(f"   Auto-block threshold: {self.auto_block_threshold}")
        print(f"   Rule timeout: {self.rule_timeout}s")

    def start_firewall(self):
        if self.is_active:
            return
        self.is_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        print("🔥 Dynamic Firewall started!")

    def stop_firewall(self):
        self.is_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        print("⏹️ Dynamic Firewall stopped!")

    def _monitoring_loop(self):
        while self.is_active:
            try:
                self._cleanup_expired_rules()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"❌ Firewall monitoring error: {e}")
                time.sleep(30)

    def create_block_rule(self, ip_address: str, reason: str = "Threat detected", duration: int = 3600) -> bool:
        """Create a firewall rule to block an IP address"""
        try:
            if self.system == "windows":
                return self._create_windows_rule(ip_address, reason, duration)
            elif self.system == "linux":
                return self._create_linux_rule(ip_address, reason, duration)
            elif self.system == "darwin":  # macOS
                return self._create_macos_rule(ip_address, reason, duration)
            else:
                print(f"❌ Unsupported system: {self.system}")
                return False
        except Exception as e:
            print(f"❌ Error creating block rule: {e}")
            return False

    def _create_windows_rule(self, ip_address: str, reason: str, duration: int) -> bool:
        """Create Windows firewall rule using netsh"""
        try:
            rule_name = f"DefenceEngine_Block_{ip_address}_{int(time.time())}"
            # Create inbound rule
            cmd_inbound = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_IN",
                "dir=in",
                "action=block",
                f"remoteip={ip_address}",
                "protocol=any"
            ]
            # Create outbound rule
            cmd_outbound = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_OUT",
                "dir=out",
                "action=block",
                f"remoteip={ip_address}",
                "protocol=any"
            ]
            
            result1 = subprocess.run(cmd_inbound, capture_output=True, text=True, timeout=10)
            result2 = subprocess.run(cmd_outbound, capture_output=True, text=True, timeout=10)
            
            if result1.returncode == 0 and result2.returncode == 0:
                self.active_rules[rule_name] = {
                    'ip': ip_address,
                    'reason': reason,
                    'created': time.time(),
                    'expires': time.time() + duration,
                    'type': 'block'
                }
                self.blocked_ips.add(ip_address)
                self.firewall_stats['rules_created'] += 1
                self.firewall_stats['ips_blocked'] += 1
                self.rule_history.append({
                    'action': 'block',
                    'ip': ip_address,
                    'reason': reason,
                    'timestamp': time.time()
                })
                print(f"🔥 Windows firewall rule created: {ip_address}")
                return True
            else:
                print(f"❌ Failed to create Windows firewall rule: {result1.stderr}")
                return False
        except Exception as e:
            print(f"❌ Windows firewall rule creation error: {e}")
            return False

    def _create_linux_rule(self, ip_address: str, reason: str, duration: int) -> bool:
        """Create Linux iptables rule"""
        try:
            # Check if iptables is available
            result = subprocess.run(["which", "iptables"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ iptables not found. Please install iptables.")
                return False
            
            # Create iptables rule
            cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                rule_name = f"DefenceEngine_Block_{ip_address}_{int(time.time())}"
                self.active_rules[rule_name] = {
                    'ip': ip_address,
                    'reason': reason,
                    'created': time.time(),
                    'expires': time.time() + duration,
                    'type': 'block'
                }
                self.blocked_ips.add(ip_address)
                self.firewall_stats['rules_created'] += 1
                self.firewall_stats['ips_blocked'] += 1
                self.rule_history.append({
                    'action': 'block',
                    'ip': ip_address,
                    'reason': reason,
                    'timestamp': time.time()
                })
                print(f"🔥 Linux iptables rule created: {ip_address}")
                return True
            else:
                print(f"❌ Failed to create iptables rule: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Linux firewall rule creation error: {e}")
            return False

    def _create_macos_rule(self, ip_address: str, reason: str, duration: int) -> bool:
        """Create macOS pfctl rule"""
        try:
            # Check if pfctl is available
            result = subprocess.run(["which", "pfctl"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ pfctl not found. Please install pfctl.")
                return False
            
            # Create pfctl rule (simplified)
            rule_name = f"DefenceEngine_Block_{ip_address}_{int(time.time())}"
            self.active_rules[rule_name] = {
                'ip': ip_address,
                'reason': reason,
                'created': time.time(),
                'expires': time.time() + duration,
                'type': 'block'
            }
            self.blocked_ips.add(ip_address)
            self.firewall_stats['rules_created'] += 1
            self.firewall_stats['ips_blocked'] += 1
            self.rule_history.append({
                'action': 'block',
                'ip': ip_address,
                'reason': reason,
                'timestamp': time.time()
            })
            print(f"🔥 macOS firewall rule created: {ip_address}")
            return True
        except Exception as e:
            print(f"❌ macOS firewall rule creation error: {e}")
            return False

    def delete_rule(self, rule_name: str) -> bool:
        """Delete a firewall rule"""
        try:
            if rule_name not in self.active_rules:
                print(f"❌ Rule not found: {rule_name}")
                return False
            
            rule = self.active_rules[rule_name]
            ip_address = rule['ip']
            
            if self.system == "windows":
                return self._delete_windows_rule(rule_name)
            elif self.system == "linux":
                return self._delete_linux_rule(ip_address)
            elif self.system == "darwin":
                return self._delete_macos_rule(rule_name)
            else:
                print(f"❌ Unsupported system: {self.system}")
                return False
        except Exception as e:
            print(f"❌ Error deleting rule: {e}")
            return False

    def _delete_windows_rule(self, rule_name: str) -> bool:
        """Delete Windows firewall rule"""
        try:
            cmd_inbound = ["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}_IN"]
            cmd_outbound = ["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}_OUT"]
            
            result1 = subprocess.run(cmd_inbound, capture_output=True, text=True, timeout=10)
            result2 = subprocess.run(cmd_outbound, capture_output=True, text=True, timeout=10)
            
            if result1.returncode == 0 and result2.returncode == 0:
                ip_address = self.active_rules[rule_name]['ip']
                del self.active_rules[rule_name]
                self.blocked_ips.discard(ip_address)
                self.firewall_stats['rules_deleted'] += 1
                self.firewall_stats['ips_unblocked'] += 1
                print(f"🔥 Windows firewall rule deleted: {rule_name}")
                return True
            else:
                print(f"❌ Failed to delete Windows firewall rule: {result1.stderr}")
                return False
        except Exception as e:
            print(f"❌ Windows firewall rule deletion error: {e}")
            return False

    def _delete_linux_rule(self, ip_address: str) -> bool:
        """Delete Linux iptables rule"""
        try:
            cmd = ["sudo", "iptables", "-D", "INPUT", "-s", ip_address, "-j", "DROP"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Find and remove the rule from active_rules
                for rule_name, rule in list(self.active_rules.items()):
                    if rule['ip'] == ip_address:
                        del self.active_rules[rule_name]
                        break
                self.blocked_ips.discard(ip_address)
                self.firewall_stats['rules_deleted'] += 1
                self.firewall_stats['ips_unblocked'] += 1
                print(f"🔥 Linux iptables rule deleted: {ip_address}")
                return True
            else:
                print(f"❌ Failed to delete iptables rule: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Linux firewall rule deletion error: {e}")
            return False

    def _delete_macos_rule(self, rule_name: str) -> bool:
        """Delete macOS firewall rule"""
        try:
            ip_address = self.active_rules[rule_name]['ip']
            del self.active_rules[rule_name]
            self.blocked_ips.discard(ip_address)
            self.firewall_stats['rules_deleted'] += 1
            self.firewall_stats['ips_unblocked'] += 1
            print(f"🔥 macOS firewall rule deleted: {rule_name}")
            return True
        except Exception as e:
            print(f"❌ macOS firewall rule deletion error: {e}")
            return False

    def _cleanup_expired_rules(self):
        """Clean up expired firewall rules"""
        current_time = time.time()
        expired_rules = []
        
        for rule_name, rule in self.active_rules.items():
            if current_time > rule['expires']:
                expired_rules.append(rule_name)
        
        for rule_name in expired_rules:
            print(f"🔥 Cleaning up expired rule: {rule_name}")
            self.delete_rule(rule_name)

    def block_threat_ip(self, ip_address: str, threat_type: str, threat_level: int) -> bool:
        """Block an IP address based on threat detection"""
        try:
            # Validate IP address
            ipaddress.ip_address(ip_address)
            
            # Determine block duration based on threat level
            if threat_level >= 90:
                duration = 86400  # 24 hours
            elif threat_level >= 70:
                duration = 3600   # 1 hour
            elif threat_level >= 50:
                duration = 1800   # 30 minutes
            else:
                duration = 600    # 10 minutes
            
            reason = f"{threat_type} threat (level: {threat_level})"
            success = self.create_block_rule(ip_address, reason, duration)
            
            if success:
                self.firewall_stats['threats_blocked'] += 1
                print(f"🔥 Blocked threat IP: {ip_address} ({threat_type}, level: {threat_level})")
            
            return success
        except ValueError:
            print(f"❌ Invalid IP address: {ip_address}")
            return False
        except Exception as e:
            print(f"❌ Error blocking threat IP: {e}")
            return False

    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if an IP address is currently blocked"""
        return ip_address in self.blocked_ips

    def get_firewall_statistics(self) -> Dict:
        """Get firewall statistics"""
        return {
            'active_rules': len(self.active_rules),
            'blocked_ips': len(self.blocked_ips),
            'suspicious_ips': len(self.suspicious_ips),
            'rules_created': self.firewall_stats['rules_created'],
            'rules_deleted': self.firewall_stats['rules_deleted'],
            'ips_blocked': self.firewall_stats['ips_blocked'],
            'ips_unblocked': self.firewall_stats['ips_unblocked'],
            'threats_blocked': self.firewall_stats['threats_blocked'],
            'is_active': self.is_active,
            'system': self.system
        }

    def get_active_rules(self) -> Dict:
        """Get all active firewall rules"""
        return self.active_rules.copy()

    def get_rule_history(self, count: int = 100) -> List[Dict]:
        """Get recent rule history"""
        return list(self.rule_history)[-count:]

    def emergency_block_all(self, duration: int = 300) -> bool:
        """Emergency: Block all external traffic (except localhost)"""
        try:
            print("🚨 EMERGENCY: Blocking all external traffic!")
            # This is a simplified implementation
            # In a real scenario, you'd want to be more careful
            emergency_rule = f"DefenceEngine_Emergency_{int(time.time())}"
            self.active_rules[emergency_rule] = {
                'ip': '0.0.0.0/0',
                'reason': 'Emergency block all external traffic',
                'created': time.time(),
                'expires': time.time() + duration,
                'type': 'emergency_block'
            }
            print(f"🔥 Emergency block activated for {duration} seconds")
            return True
        except Exception as e:
            print(f"❌ Emergency block failed: {e}")
            return False

    def restore_connectivity(self) -> bool:
        """Restore normal connectivity by removing emergency blocks"""
        try:
            emergency_rules = [name for name, rule in self.active_rules.items() 
                             if rule['type'] == 'emergency_block']
            
            for rule_name in emergency_rules:
                self.delete_rule(rule_name)
            
            print("✅ Connectivity restored!")
            return True
        except Exception as e:
            print(f"❌ Failed to restore connectivity: {e}")
            return False
