#!/usr/bin/env python3
"""
Team 8: System Monitoring - Monitoring Dashboard (Mini)
Operational Silo: Essential real-time monitoring and alerts
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import random
from datetime import datetime

class AEGISMonitoringDashboard:
    def __init__(self):
        self.name = "AEGIS Monitoring Dashboard"
        self.version = "1.0.0"
        self.monitoring_active = False
        
    def create_monitoring_interface(self, parent):
        """Create monitoring dashboard interface"""
        monitor_frame = tk.LabelFrame(
            parent,
            text="📊 REAL-TIME MONITORING DASHBOARD",
            font=('Segoe UI', 12, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        monitor_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Control panel
        control_frame = tk.Frame(monitor_frame, bg='#0d1117')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Start/Stop monitoring
        self.monitor_btn = tk.Button(
            control_frame,
            text="🚀 Start Monitoring",
            command=self.toggle_monitoring,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.monitor_btn.pack(side='left', padx=5)
        
        # Clear logs
        clear_btn = tk.Button(
            control_frame,
            text="Clear Logs",
            command=self.clear_logs,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=5)
        
        # Status indicators
        status_frame = tk.Frame(monitor_frame, bg='#0d1117')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        # System status
        self.system_status_label = tk.Label(
            status_frame,
            text="🟢 System: Online",
            font=('Segoe UI', 9),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        self.system_status_label.pack(side='left', padx=10)
        
        # Network status
        self.network_status_label = tk.Label(
            status_frame,
            text="🟢 Network: Active",
            font=('Segoe UI', 9),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        self.network_status_label.pack(side='left', padx=10)
        
        # Operations status
        self.ops_status_label = tk.Label(
            status_frame,
            text="🟢 Operations: Running",
            font=('Segoe UI', 9),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        self.ops_status_label.pack(side='left', padx=10)
        
        # Monitoring log
        log_frame = tk.LabelFrame(
            monitor_frame,
            text="📋 Monitoring Log",
            font=('Segoe UI', 10, 'bold'),
            fg='#58a6ff',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.monitoring_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.monitoring_log.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial log message
        self.log_message("Monitoring Dashboard initialized")
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if not self.monitoring_active:
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    def start_monitoring(self):
        """Start monitoring"""
        self.monitoring_active = True
        self.monitor_btn.config(text="⏹️ Stop Monitoring", bg='#ff6b6b')
        self.log_message("🚀 Monitoring started")
        
        # Start monitoring thread
        threading.Thread(target=self.monitor_systems, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        self.monitor_btn.config(text="🚀 Start Monitoring", bg='#4ecdc4')
        self.log_message("⏹️ Monitoring stopped")
    
    def monitor_systems(self):
        """Monitor systems in background"""
        while self.monitoring_active:
            # Simulate system monitoring
            self.check_system_status()
            self.check_network_status()
            self.check_operations_status()
            
            time.sleep(3)  # Check every 3 seconds
    
    def check_system_status(self):
        """Check system status"""
        if random.random() < 0.1:  # 10% chance of issue
            self.system_status_label.config(text="🔴 System: Warning", fg='#ff6b6b')
            self.log_message("⚠️ System warning detected")
        else:
            self.system_status_label.config(text="🟢 System: Online", fg='#4ecdc4')
    
    def check_network_status(self):
        """Check network status"""
        if random.random() < 0.05:  # 5% chance of issue
            self.network_status_label.config(text="🔴 Network: Issue", fg='#ff6b6b')
            self.log_message("⚠️ Network issue detected")
        else:
            self.network_status_label.config(text="🟢 Network: Active", fg='#4ecdc4')
    
    def check_operations_status(self):
        """Check operations status"""
        if random.random() < 0.15:  # 15% chance of issue
            self.ops_status_label.config(text="🔴 Operations: Alert", fg='#ff6b6b')
            self.log_message("⚠️ Operations alert detected")
        else:
            self.ops_status_label.config(text="🟢 Operations: Running", fg='#4ecdc4')
    
    def log_message(self, message):
        """Log monitoring message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.monitoring_log.insert(tk.END, formatted_message)
        self.monitoring_log.see(tk.END)
    
    def clear_logs(self):
        """Clear monitoring logs"""
        self.monitoring_log.delete('1.0', tk.END)
        self.log_message("Logs cleared") 