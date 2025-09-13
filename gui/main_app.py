"""
Advanced GUI Application for Defence Engine
Modern interface with real-time monitoring and controls
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from typing import Dict, List, Optional
import json
from datetime import datetime

# Import Defence Engine components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.quantum_hash import QuantumHashEngine
from ai.threat_detector import AIThreatDetector
from defense.reverse_attack import ReverseAttackSystem
from license.license_manager import LicenseManager
from config import DefenceConfig

class DefenceEngineGUI:
    """Main GUI Application for Defence Engine"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ Defence Engine - Advanced Security Protection System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize components
        self.quantum_engine = None
        self.ai_detector = None
        self.reverse_attack = None
        self.license_manager = LicenseManager()
        
        # GUI state
        self.is_running = False
        self.license_key = ""
        self.update_thread = None
        
        # Create GUI
        self._create_gui()
        
        # Start update loop
        self._start_update_loop()
    
    def _create_gui(self):
        """Create the main GUI interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2d2d2d', foreground='white')
        style.configure('TNotebook.Tab', background='#3d3d3d', foreground='white', padding=[20, 10])
        style.configure('TFrame', background='#2d2d2d')
        style.configure('TLabel', background='#2d2d2d', foreground='white')
        style.configure('TButton', background='#4d4d4d', foreground='white')
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self._create_dashboard_tab()
        self._create_hash_monitor_tab()
        self._create_threat_detection_tab()
        self._create_defense_controls_tab()
        self._create_license_management_tab()
        self._create_settings_tab()
        
        # Status bar
        self._create_status_bar(main_frame)
    
    def _create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Title
        title_label = ttk.Label(dashboard_frame, text="🛡️ Defence Engine Dashboard", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Control panel
        control_frame = ttk.LabelFrame(dashboard_frame, text="System Controls", padding=20)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # License input
        license_frame = ttk.Frame(control_frame)
        license_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(license_frame, text="License Key:").pack(side=tk.LEFT)
        self.license_entry = ttk.Entry(license_frame, width=50, show="*")
        self.license_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Defence Engine", 
                                      command=self._start_defence_engine)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop Defence Engine", 
                                     command=self._stop_defence_engine, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status display
        status_frame = ttk.LabelFrame(dashboard_frame, text="System Status", padding=20)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Status labels
        self.status_labels = {}
        status_items = [
            ("Engine Status", "Stopped"),
            ("Hash Generation", "0 h/s"),
            ("Threats Detected", "0"),
            ("Active Defenses", "0"),
            ("License Status", "Not Validated"),
            ("Security Level", "Standard")
        ]
        
        for i, (label, value) in enumerate(status_items):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(status_frame, text=f"{label}:").grid(row=row, column=col, sticky=tk.W, padx=10, pady=5)
            self.status_labels[label] = ttk.Label(status_frame, text=value, foreground='#00ff00')
            self.status_labels[label].grid(row=row, column=col+1, sticky=tk.W, padx=10, pady=5)
    
    def _create_hash_monitor_tab(self):
        """Create hash monitoring tab"""
        hash_frame = ttk.Frame(self.notebook)
        self.notebook.add(hash_frame, text="🔬 Hash Monitor")
        
        # Title
        title_label = ttk.Label(hash_frame, text="Real-time Hash Generation Monitor", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        
        # Hash display
        hash_display_frame = ttk.LabelFrame(hash_frame, text="Live Hash Stream", padding=10)
        hash_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.hash_display = scrolledtext.ScrolledText(hash_display_frame, height=20, 
                                                     bg='#1e1e1e', fg='#00ff00', 
                                                     font=('Courier', 10))
        self.hash_display.pack(fill=tk.BOTH, expand=True)
        
        # Hash statistics
        stats_frame = ttk.LabelFrame(hash_frame, text="Hash Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.hash_stats_labels = {}
        stats_items = [
            ("Total Hashes", "0"),
            ("Hashes/Second", "0"),
            ("Hashes/Minute", "0"),
            ("Pattern Rotations", "0"),
            ("Security Layers", "8"),
            ("GPU Acceleration", "Disabled")
        ]
        
        for i, (label, value) in enumerate(stats_items):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(stats_frame, text=f"{label}:").grid(row=row, column=col, sticky=tk.W, padx=10, pady=5)
            self.hash_stats_labels[label] = ttk.Label(stats_frame, text=value, foreground='#00ff00')
            self.hash_stats_labels[label].grid(row=row, column=col+1, sticky=tk.W, padx=10, pady=5)
    
    def _create_threat_detection_tab(self):
        """Create threat detection tab"""
        threat_frame = ttk.Frame(self.notebook)
        self.notebook.add(threat_frame, text="🤖 Threat Detection")
        
        # Title
        title_label = ttk.Label(threat_frame, text="AI-Powered Threat Detection", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        
        # Threat display
        threat_display_frame = ttk.LabelFrame(threat_frame, text="Threat Alerts", padding=10)
        threat_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.threat_display = scrolledtext.ScrolledText(threat_display_frame, height=15, 
                                                       bg='#1e1e1e', fg='#ff6b6b', 
                                                       font=('Courier', 10))
        self.threat_display.pack(fill=tk.BOTH, expand=True)
        
        # Threat statistics
        threat_stats_frame = ttk.LabelFrame(threat_frame, text="Threat Statistics", padding=10)
        threat_stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.threat_stats_labels = {}
        threat_stats_items = [
            ("Total Threats", "0"),
            ("High Level", "0"),
            ("Medium Level", "0"),
            ("Low Level", "0"),
            ("AI Confidence", "0%"),
            ("Neural Model", "Not Trained")
        ]
        
        for i, (label, value) in enumerate(threat_stats_items):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(threat_stats_frame, text=f"{label}:").grid(row=row, column=col, sticky=tk.W, padx=10, pady=5)
            self.threat_stats_labels[label] = ttk.Label(threat_stats_frame, text=value, foreground='#ff6b6b')
            self.threat_stats_labels[label].grid(row=row, column=col+1, sticky=tk.W, padx=10, pady=5)
    
    def _create_defense_controls_tab(self):
        """Create defense controls tab"""
        defense_frame = ttk.Frame(self.notebook)
        self.notebook.add(defense_frame, text="🛡️ Defense Controls")
        
        # Title
        title_label = ttk.Label(defense_frame, text="Advanced Defense Systems", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        
        # Defense controls
        controls_frame = ttk.LabelFrame(defense_frame, text="Defense Controls", padding=20)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Honeypot controls
        honeypot_frame = ttk.Frame(controls_frame)
        honeypot_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(honeypot_frame, text="Honeypot Network:").pack(side=tk.LEFT)
        self.honeypot_status = ttk.Label(honeypot_frame, text="Inactive", foreground='#ff6b6b')
        self.honeypot_status.pack(side=tk.LEFT, padx=10)
        
        # Reverse attack controls
        reverse_frame = ttk.Frame(controls_frame)
        reverse_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(reverse_frame, text="Reverse Attack System:").pack(side=tk.LEFT)
        self.reverse_status = ttk.Label(reverse_frame, text="Inactive", foreground='#ff6b6b')
        self.reverse_status.pack(side=tk.LEFT, padx=10)
        
        # Defense statistics
        defense_stats_frame = ttk.LabelFrame(defense_frame, text="Defense Statistics", padding=10)
        defense_stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.defense_stats_display = scrolledtext.ScrolledText(defense_stats_frame, height=15, 
                                                              bg='#1e1e1e', fg='#4ecdc4', 
                                                              font=('Courier', 10))
        self.defense_stats_display.pack(fill=tk.BOTH, expand=True)
    
    def _create_license_management_tab(self):
        """Create license management tab"""
        license_frame = ttk.Frame(self.notebook)
        self.notebook.add(license_frame, text="🔐 License Management")
        
        # Title
        title_label = ttk.Label(license_frame, text="License Management System", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        
        # License info
        license_info_frame = ttk.LabelFrame(license_frame, text="Current License", padding=20)
        license_info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.license_info_labels = {}
        license_items = [
            ("License Key", "Not Set"),
            ("User ID", "Unknown"),
            ("Status", "Not Validated"),
            ("Usage Count", "0"),
            ("Expiry Date", "Unknown")
        ]
        
        for i, (label, value) in enumerate(license_items):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(license_info_frame, text=f"{label}:").grid(row=row, column=col, sticky=tk.W, padx=10, pady=5)
            self.license_info_labels[label] = ttk.Label(license_info_frame, text=value, foreground='#00ff00')
            self.license_info_labels[label].grid(row=row, column=col+1, sticky=tk.W, padx=10, pady=5)
        
        # License statistics
        license_stats_frame = ttk.LabelFrame(license_frame, text="License Statistics", padding=10)
        license_stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.license_stats_display = scrolledtext.ScrolledText(license_stats_frame, height=15, 
                                                              bg='#1e1e1e', fg='#ffd93d', 
                                                              font=('Courier', 10))
        self.license_stats_display.pack(fill=tk.BOTH, expand=True)
    
    def _create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Title
        title_label = ttk.Label(settings_frame, text="System Settings", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        
        # Security level
        security_frame = ttk.LabelFrame(settings_frame, text="Security Configuration", padding=20)
        security_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(security_frame, text="Security Level:").pack(side=tk.LEFT)
        self.security_level = ttk.Combobox(security_frame, values=['basic', 'standard', 'high', 'maximum', 'quantum'])
        self.security_level.set('quantum')
        self.security_level.pack(side=tk.LEFT, padx=10)
        
        # Monitoring settings
        monitoring_frame = ttk.LabelFrame(settings_frame, text="Monitoring Settings", padding=20)
        monitoring_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(monitoring_frame, text="Monitoring Interval (seconds):").pack(side=tk.LEFT)
        self.monitoring_interval = ttk.Spinbox(monitoring_frame, from_=1, to=60, value=5)
        self.monitoring_interval.pack(side=tk.LEFT, padx=10)
        
        # Hash display settings
        hash_settings_frame = ttk.LabelFrame(settings_frame, text="Hash Display Settings", padding=20)
        hash_settings_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.show_hashes = tk.BooleanVar(value=True)
        ttk.Checkbutton(hash_settings_frame, text="Show Real-time Hashes", 
                       variable=self.show_hashes).pack(side=tk.LEFT)
    
    def _create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.time_label = ttk.Label(status_frame, text="", relief=tk.SUNKEN)
        self.time_label.pack(side=tk.RIGHT)
    
    def _start_defence_engine(self):
        """Start the Defence Engine"""
        license_key = self.license_entry.get().strip()
        
        if not license_key:
            messagebox.showerror("Error", "Please enter a license key!")
            return
        
        # Validate license
        validation_result = self.license_manager.validate_license(license_key)
        
        if not validation_result['valid']:
            messagebox.showerror("License Error", f"Invalid license: {validation_result['reason']}")
            return
        
        try:
            # Initialize components
            self.quantum_engine = QuantumHashEngine(display_hashes=self.show_hashes.get())
            self.ai_detector = AIThreatDetector()
            self.reverse_attack = ReverseAttackSystem(self.quantum_engine)
            
            # Start components
            self.quantum_engine.start_real_time_hashing()
            self.ai_detector.start_monitoring()
            self.reverse_attack.create_crash_proof_barrier()
            
            # Update GUI state
            self.is_running = True
            self.license_key = license_key
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Update license info
            self._update_license_info(validation_result)
            
            self.status_label.config(text="Defence Engine Active")
            messagebox.showinfo("Success", "Defence Engine started successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Defence Engine: {str(e)}")
    
    def _stop_defence_engine(self):
        """Stop the Defence Engine"""
        try:
            # Stop components
            if self.quantum_engine:
                self.quantum_engine.stop_real_time_hashing()
            
            if self.ai_detector:
                self.ai_detector.stop_monitoring()
            
            if self.reverse_attack:
                self.reverse_attack.stop_defense()
            
            # Update GUI state
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            self.status_label.config(text="Defence Engine Stopped")
            messagebox.showinfo("Success", "Defence Engine stopped successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop Defence Engine: {str(e)}")
    
    def _update_license_info(self, validation_result: Dict):
        """Update license information display"""
        license_data = validation_result.get('license_data', {})
        
        self.license_info_labels["License Key"].config(text=self.license_key[:20] + "...")
        self.license_info_labels["User ID"].config(text=license_data.get('user_id', 'Unknown'))
        self.license_info_labels["Status"].config(text="Valid", foreground='#00ff00')
        self.license_info_labels["Usage Count"].config(text=str(validation_result.get('usage_count', 0)))
        self.license_info_labels["Expiry Date"].config(text=license_data.get('expiry_date', 'Never'))
    
    def _start_update_loop(self):
        """Start the GUI update loop"""
        def update_loop():
            while True:
                try:
                    self._update_display()
                    time.sleep(1)
                except:
                    break
        
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def _update_display(self):
        """Update GUI display"""
        try:
            # Update time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.config(text=current_time)
            
            if not self.is_running:
                return
            
            # Update status
            self.status_labels["Engine Status"].config(text="Running", foreground='#00ff00')
            
            # Update hash statistics
            if self.quantum_engine:
                stats = self.quantum_engine.get_hash_statistics()
                self.status_labels["Hash Generation"].config(text=f"{stats.get('total_hashes_generated', 0):,} h/s")
                self.hash_stats_labels["Total Hashes"].config(text=f"{stats.get('total_hashes_generated', 0):,}")
                self.hash_stats_labels["Pattern Rotations"].config(text=str(stats.get('rotation_counter', 0)))
                self.hash_stats_labels["Security Layers"].config(text=str(stats.get('obfuscation_layers', 8)))
                self.hash_stats_labels["GPU Acceleration"].config(text="Enabled" if stats.get('gpu_enabled', False) else "Disabled")
            
            # Update threat statistics
            if self.ai_detector:
                threat_stats = self.ai_detector.get_threat_statistics()
                self.status_labels["Threats Detected"].config(text=str(threat_stats.get('total_threats_detected', 0)))
                self.threat_stats_labels["Total Threats"].config(text=str(threat_stats.get('total_threats_detected', 0)))
                self.threat_stats_labels["AI Confidence"].config(text="85%")
                self.threat_stats_labels["Neural Model"].config(text="Trained" if threat_stats.get('neural_model_trained', False) else "Not Trained")
            
            # Update defense statistics
            if self.reverse_attack:
                defense_stats = self.reverse_attack.get_defense_statistics()
                self.status_labels["Active Defenses"].config(text=str(defense_stats.get('active_attacks', 0)))
                
                # Update defense display
                defense_text = f"Defense Statistics:\n"
                defense_text += f"Active Attacks: {defense_stats.get('active_attacks', 0)}\n"
                defense_text += f"Honeypot Connections: {defense_stats.get('honeypot_network', {}).get('total_connections', 0)}\n"
                defense_text += f"Resource Attacks: {defense_stats.get('resource_attacks_active', 0)}\n"
                
                self.defense_stats_display.delete(1.0, tk.END)
                self.defense_stats_display.insert(tk.END, defense_text)
            
            # Update license statistics
            license_stats = self.license_manager.get_license_statistics()
            license_text = f"License Statistics:\n"
            license_text += f"Total Licenses: {license_stats.get('total_licenses', 0)}\n"
            license_text += f"Active Licenses: {license_stats.get('active_licenses', 0)}\n"
            license_text += f"Total Usage: {license_stats.get('total_usage', 0)}\n"
            license_text += f"Blockchain Blocks: {license_stats.get('blockchain_blocks', 0)}\n"
            
            self.license_stats_display.delete(1.0, tk.END)
            self.license_stats_display.insert(tk.END, license_text)
            
        except Exception as e:
            print(f"❌ Display update error: {e}")
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()
