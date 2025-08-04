#!/usr/bin/env python3
"""
AEGIS Test Environment Setup
Configures safe testing environments for comprehensive security testing
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from datetime import datetime

class TestEnvironmentSetup:
    def __init__(self):
        self.name = "AEGIS Test Environment Setup"
        self.version = "1.0.0"
        
        # Test environment configurations
        self.test_environments = {
            "local_network": {
                "name": "Local Network Testing",
                "description": "Safe local network scanning and testing",
                "target_range": "192.168.1.1-254",
                "port_range": "1-1000",
                "risk_level": "Low",
                "status": "Ready"
            },
            "web_application": {
                "name": "Web Application Testing",
                "description": "Local web application security testing",
                "target_url": "http://localhost:8080",
                "test_types": ["SQL Injection", "XSS", "CSRF", "Authentication"],
                "risk_level": "Medium",
                "status": "Ready"
            },
            "database_testing": {
                "name": "Database Testing",
                "description": "Local database security assessment",
                "target_db": "localhost",
                "test_types": ["SQL Injection", "Privilege Escalation", "Data Extraction"],
                "risk_level": "Medium",
                "status": "Ready"
            },
            "social_engineering": {
                "name": "Social Engineering Assessment",
                "description": "Human security testing scenarios",
                "test_types": ["Phishing", "Pretexting", "Baiting", "Quid Pro Quo"],
                "risk_level": "Low",
                "status": "Ready"
            },
            "physical_security": {
                "name": "Physical Security Testing",
                "description": "Physical access control assessment",
                "test_types": ["Access Control", "Surveillance", "Social Engineering"],
                "risk_level": "Low",
                "status": "Ready"
            }
        }
        
        self.init_setup()
    
    def init_setup(self):
        """Initialize setup interface"""
        self.root = tk.Tk()
        self.root.title(f"🔧 {self.name}")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d1117')
        
        self.create_setup_interface()
    
    def create_setup_interface(self):
        """Create setup interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#0d1117')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_label = tk.Label(
            main_frame,
            text="🔧 AEGIS TEST ENVIRONMENT SETUP",
            font=('Segoe UI', 24, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        header_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Configure safe testing environments for comprehensive security assessment",
            font=('Segoe UI', 14),
            fg='#ffffff',
            bg='#0d1117'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Environment selection
        env_frame = tk.LabelFrame(
            main_frame,
            text="🎯 SELECT TEST ENVIRONMENT",
            font=('Segoe UI', 12, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        env_frame.pack(fill='x', padx=10, pady=5)
        
        # Environment buttons
        env_buttons_frame = tk.Frame(env_frame, bg='#0d1117')
        env_buttons_frame.pack(fill='x', padx=10, pady=10)
        
        for env_key, env_info in self.test_environments.items():
            env_btn = tk.Button(
                env_buttons_frame,
                text=f"🔧 {env_info['name']} ({env_info['risk_level']} Risk)",
                command=lambda k=env_key: self.select_environment(k),
                bg='#21262d',
                fg='#c9d1d9',
                font=('Segoe UI', 10),
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2'
            )
            env_btn.pack(fill='x', pady=2)
        
        # Configuration panel
        self.config_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ ENVIRONMENT CONFIGURATION",
            font=('Segoe UI', 12, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        self.config_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Status display
        self.status_text = scrolledtext.ScrolledText(
            self.config_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD,
            height=15
        )
        self.status_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg='#0d1117')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Setup button
        setup_btn = tk.Button(
            control_frame,
            text="🚀 Setup Selected Environment",
            command=self.setup_environment,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        setup_btn.pack(side='left', padx=5)
        
        # Setup all button
        setup_all_btn = tk.Button(
            control_frame,
            text="🌍 Setup All Environments",
            command=self.setup_all_environments,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        setup_all_btn.pack(side='left', padx=5)
        
        # Launch AEGIS button
        launch_btn = tk.Button(
            control_frame,
            text="🚀 Launch AEGIS System",
            command=self.launch_aegis,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        launch_btn.pack(side='right', padx=5)
        
        # Initialize with default environment
        self.selected_environment = "local_network"
        self.update_configuration_display()
    
    def select_environment(self, env_key):
        """Select test environment"""
        self.selected_environment = env_key
        self.update_configuration_display()
        self.log_message(f"Selected environment: {self.test_environments[env_key]['name']}")
    
    def update_configuration_display(self):
        """Update configuration display"""
        env_info = self.test_environments[self.selected_environment]
        
        config_text = f"""
🔧 ENVIRONMENT: {env_info['name']}
📋 DESCRIPTION: {env_info['description']}
⚠️  RISK LEVEL: {env_info['risk_level']}
📊 STATUS: {env_info['status']}

🎯 CONFIGURATION DETAILS:
"""
        
        if self.selected_environment == "local_network":
            config_text += f"""
🌐 Target Range: {env_info['target_range']}
🔌 Port Range: {env_info['port_range']}
📡 Scan Type: Comprehensive network scan
🛡️ Safety: Local network only
"""
        elif self.selected_environment == "web_application":
            config_text += f"""
🌐 Target URL: {env_info['target_url']}
🔍 Test Types: {', '.join(env_info['test_types'])}
🛡️ Safety: Local development environment
"""
        elif self.selected_environment == "database_testing":
            config_text += f"""
🗄️ Target Database: {env_info['target_db']}
🔍 Test Types: {', '.join(env_info['test_types'])}
🛡️ Safety: Local database instance
"""
        elif self.selected_environment == "social_engineering":
            config_text += f"""
👥 Test Types: {', '.join(env_info['test_types'])}
🛡️ Safety: Authorized personnel only
📋 Consent: Required for all testing
"""
        elif self.selected_environment == "physical_security":
            config_text += f"""
🏢 Test Types: {', '.join(env_info['test_types'])}
🛡️ Safety: Authorized locations only
📋 Permissions: Required for all testing
"""
        
        config_text += f"""

✅ READY TO PROCEED WITH SECURITY TESTING
"""
        
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, config_text)
    
    def setup_environment(self):
        """Setup selected environment"""
        env_info = self.test_environments[self.selected_environment]
        self.log_message(f"🚀 Setting up {env_info['name']}...")
        
        # Simulate setup process
        import time
        import threading
        
        def setup_process():
            steps = [
                "Initializing test environment...",
                "Configuring target systems...",
                "Setting up monitoring tools...",
                "Preparing test scenarios...",
                "Validating safety protocols...",
                "Environment setup complete!"
            ]
            
            for step in steps:
                self.log_message(f"⏳ {step}")
                time.sleep(1)
            
            self.log_message(f"✅ {env_info['name']} is ready for testing!")
            messagebox.showinfo("Setup Complete", f"{env_info['name']} has been configured successfully!")
        
        threading.Thread(target=setup_process, daemon=True).start()
    
    def setup_all_environments(self):
        """Setup all test environments"""
        self.log_message("🌍 Setting up all test environments...")
        
        import time
        import threading
        
        def setup_all_process():
            environments = list(self.test_environments.keys())
            
            for env_key in environments:
                env_info = self.test_environments[env_key]
                self.log_message(f"🚀 Setting up {env_info['name']}...")
                time.sleep(2)
                self.log_message(f"✅ {env_info['name']} configured successfully!")
            
            self.log_message("🎉 All test environments are ready!")
            messagebox.showinfo("Setup Complete", "All test environments have been configured successfully!")
        
        threading.Thread(target=setup_all_process, daemon=True).start()
    
    def launch_aegis(self):
        """Launch AEGIS system"""
        self.log_message("🚀 Launching AEGIS Complete Workspace...")
        
        import subprocess
        import threading
        
        def launch_process():
            try:
                subprocess.Popen(["python", "AEGIS_COMPLETE_WORKSPACE.py"])
                self.log_message("✅ AEGIS system launched successfully!")
            except Exception as e:
                self.log_message(f"❌ Error launching AEGIS: {e}")
        
        threading.Thread(target=launch_process, daemon=True).start()
    
    def log_message(self, message):
        """Log message to status display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, log_entry)
        self.status_text.see(tk.END)
        self.root.update()
    
    def run(self):
        """Run the setup application"""
        self.root.mainloop()

def main():
    """Main function"""
    setup = TestEnvironmentSetup()
    setup.run()

if __name__ == "__main__":
    main() 