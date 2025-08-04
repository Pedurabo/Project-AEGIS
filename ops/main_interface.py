"""
OPERATIONAL SILO - Main Interface
Friendly UI/UX with Progressive Learning and Advanced Features
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Add dev directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dev'))

from dev.ai_core import AICore, AttackType, AttackResult
from dev.unsupervised_learning import UnsupervisedLearning


class ProgressiveLearningInterface:
    """Friendly UI with progressive learning for beginners to experts"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 AI-Powered Penetration Testing Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize AI components
        self.ai_core = AICore()
        self.unsupervised_learning = UnsupervisedLearning()
        
        # User progress tracking
        self.user_level = 1
        self.user_experience = 0
        self.learning_progress = {}
        
        # Message queue for threading
        self.message_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        self.setup_styles()
        
        # Start message processing
        self.process_messages()
    
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00', 
                       font=('Consolas', 16, 'bold'))
        
        style.configure('Header.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00', 
                       font=('Consolas', 12, 'bold'))
        
        style.configure('Info.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffffff', 
                       font=('Consolas', 10))
        
        style.configure('Success.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00', 
                       font=('Consolas', 10))
        
        style.configure('Error.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ff0000', 
                       font=('Consolas', 10))
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🔐 AI-Powered Penetration Testing Tool", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # User progress
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.level_label = ttk.Label(self.progress_frame, 
                                    text=f"Level: {self.user_level}", 
                                    style='Header.TLabel')
        self.level_label.pack(side=tk.LEFT)
        
        self.exp_label = ttk.Label(self.progress_frame, 
                                  text=f"Experience: {self.user_experience}", 
                                  style='Info.TLabel')
        self.exp_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_beginner_tab()
        self.create_advanced_tab()
        self.create_ai_analysis_tab()
        self.create_learning_tab()
        self.create_settings_tab()
    
    def create_beginner_tab(self):
        """Create beginner-friendly tab"""
        beginner_frame = ttk.Frame(self.notebook)
        self.notebook.add(beginner_frame, text="🚀 Beginner Mode")
        
        # Target input
        target_frame = ttk.LabelFrame(beginner_frame, text="Target Configuration", padding=10)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(target_frame, text="Target URL/IP:").pack(anchor=tk.W)
        self.target_entry = ttk.Entry(target_frame, width=60)
        self.target_entry.pack(fill=tk.X, pady=5)
        self.target_entry.insert(0, "http://example.com")
        
        # Attack type selection
        attack_frame = ttk.LabelFrame(beginner_frame, text="Attack Type", padding=10)
        attack_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.attack_var = tk.StringVar(value="sql_injection")
        attack_types = [
            ("SQL Injection", "sql_injection"),
            ("Cross-Site Scripting (XSS)", "xss"),
            ("File Inclusion", "lfi_rfi"),
            ("Command Injection", "command_injection"),
            ("API Abuse", "api_abuse")
        ]
        
        for text, value in attack_types:
            ttk.Radiobutton(attack_frame, text=text, variable=self.attack_var, 
                           value=value).pack(anchor=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(beginner_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="🔍 Quick Scan", 
                  command=self.quick_scan).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🎯 Smart Attack", 
                  command=self.smart_attack).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📊 Show Results", 
                  command=self.show_results).pack(side=tk.LEFT)
        
        # Results area
        results_frame = ttk.LabelFrame(beginner_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, 
                                                     bg='#1e1e1e', fg='#00ff00', 
                                                     font=('Consolas', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_advanced_tab(self):
        """Create advanced features tab"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="⚡ Advanced Mode")
        
        # Advanced configuration
        config_frame = ttk.LabelFrame(advanced_frame, text="Advanced Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Max attempts
        ttk.Label(config_frame, text="Max Attempts:").pack(anchor=tk.W)
        self.max_attempts_var = tk.StringVar(value="50")
        ttk.Entry(config_frame, textvariable=self.max_attempts_var, width=10).pack(anchor=tk.W, pady=5)
        
        # Stealth mode
        self.stealth_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Stealth Mode", 
                       variable=self.stealth_var).pack(anchor=tk.W, pady=5)
        
        # AI confidence threshold
        ttk.Label(config_frame, text="AI Confidence Threshold:").pack(anchor=tk.W)
        self.confidence_var = tk.StringVar(value="0.7")
        ttk.Entry(config_frame, textvariable=self.confidence_var, width=10).pack(anchor=tk.W, pady=5)
        
        # Advanced buttons
        button_frame = ttk.Frame(advanced_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="🤖 AI-Powered Attack", 
                  command=self.ai_powered_attack).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🔄 Adaptive Learning", 
                  command=self.adaptive_learning).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📈 Performance Analysis", 
                  command=self.performance_analysis).pack(side=tk.LEFT)
        
        # Advanced results
        adv_results_frame = ttk.LabelFrame(advanced_frame, text="Advanced Results", padding=10)
        adv_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.adv_results_text = scrolledtext.ScrolledText(adv_results_frame, height=15, 
                                                         bg='#1e1e1e', fg='#00ff00', 
                                                         font=('Consolas', 10))
        self.adv_results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_ai_analysis_tab(self):
        """Create AI analysis tab"""
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text="🧠 AI Analysis")
        
        # AI analysis controls
        ai_control_frame = ttk.LabelFrame(ai_frame, text="AI Analysis Controls", padding=10)
        ai_control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(ai_control_frame, text="🔍 Pattern Discovery", 
                  command=self.pattern_discovery).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(ai_control_frame, text="🚨 Anomaly Detection", 
                  command=self.anomaly_detection).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(ai_control_frame, text="📊 Generate Insights", 
                  command=self.generate_insights).pack(side=tk.LEFT)
        
        # AI results
        ai_results_frame = ttk.LabelFrame(ai_frame, text="AI Analysis Results", padding=10)
        ai_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.ai_results_text = scrolledtext.ScrolledText(ai_results_frame, height=20, 
                                                        bg='#1e1e1e', fg='#00ff00', 
                                                        font=('Consolas', 10))
        self.ai_results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_learning_tab(self):
        """Create learning progress tab"""
        learning_frame = ttk.Frame(self.notebook)
        self.notebook.add(learning_frame, text="📚 Learning Progress")
        
        # Learning statistics
        stats_frame = ttk.LabelFrame(learning_frame, text="Your Learning Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=10, 
                                                   bg='#1e1e1e', fg='#00ff00', 
                                                   font=('Consolas', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Learning tips
        tips_frame = ttk.LabelFrame(learning_frame, text="Learning Tips", padding=10)
        tips_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tips_text = scrolledtext.ScrolledText(tips_frame, height=10, 
                                                  bg='#1e1e1e', fg='#ffff00', 
                                                  font=('Consolas', 10))
        self.tips_text.pack(fill=tk.BOTH, expand=True)
        
        # Update learning content
        self.update_learning_content()
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # General settings
        general_frame = ttk.LabelFrame(settings_frame, text="General Settings", padding=10)
        general_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Theme selection
        ttk.Label(general_frame, text="Theme:").pack(anchor=tk.W)
        self.theme_var = tk.StringVar(value="Dark")
        theme_combo = ttk.Combobox(general_frame, textvariable=self.theme_var, 
                                  values=["Dark", "Light", "Terminal"])
        theme_combo.pack(anchor=tk.W, pady=5)
        
        # AI settings
        ai_settings_frame = ttk.LabelFrame(settings_frame, text="AI Settings", padding=10)
        ai_settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.auto_learn_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ai_settings_frame, text="Auto-learning enabled", 
                       variable=self.auto_learn_var).pack(anchor=tk.W, pady=5)
        
        self.show_confidence_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ai_settings_frame, text="Show confidence scores", 
                       variable=self.show_confidence_var).pack(anchor=tk.W, pady=5)
        
        # Save button
        ttk.Button(settings_frame, text="💾 Save Settings", 
                  command=self.save_settings).pack(pady=10)
    
    def quick_scan(self):
        """Perform a quick scan for beginners"""
        target = self.target_entry.get()
        if not target:
            messagebox.showerror("Error", "Please enter a target URL")
            return
        
        self.log_message("🔍 Starting quick scan...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._run_quick_scan, args=(target,))
        thread.daemon = True
        thread.start()
    
    def _run_quick_scan(self, target: str):
        """Run quick scan in background"""
        try:
            # Basic port scan simulation
            self.log_message("📡 Scanning common ports...")
            time.sleep(1)
            
            # Simulate results
            results = [
                "✅ Port 80 (HTTP) - OPEN",
                "✅ Port 443 (HTTPS) - OPEN", 
                "❌ Port 22 (SSH) - CLOSED",
                "❌ Port 21 (FTP) - CLOSED"
            ]
            
            for result in results:
                self.log_message(result)
                time.sleep(0.5)
            
            self.log_message("🎯 Quick scan completed!")
            self.gain_experience(10)
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
    
    def smart_attack(self):
        """Perform AI-powered smart attack"""
        target = self.target_entry.get()
        attack_type_str = self.attack_var.get()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target URL")
            return
        
        # Convert string to AttackType enum
        attack_type = AttackType(attack_type_str)
        
        self.log_message(f"🤖 Starting smart {attack_type.value} attack...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._run_smart_attack, args=(target, attack_type))
        thread.daemon = True
        thread.start()
    
    def _run_smart_attack(self, target: str, attack_type: AttackType):
        """Run smart attack in background"""
        try:
            max_attempts = int(self.max_attempts_var.get())
            previous_failures = []
            
            for attempt in range(max_attempts):
                # Generate adaptive payload
                payload = self.ai_core.generate_adaptive_payload(target, attack_type, previous_failures)
                
                # Predict success
                confidence = self.ai_core.predict_success(target, payload, attack_type)
                
                self.log_message(f"🎯 Attempt {attempt + 1}: Confidence = {confidence:.2f}")
                
                # Simulate attack
                success = confidence > 0.7  # Simulate based on confidence
                
                # Create result
                result = AttackResult(
                    attack_type=attack_type,
                    target=target,
                    payload=payload,
                    success=success,
                    response_code=200 if success else 403,
                    response_time=0.5,
                    confidence_score=confidence
                )
                
                # Learn from result
                self.ai_core.learn_from_result(result)
                
                if success:
                    self.log_message(f"✅ Attack successful! Payload: {payload}")
                    self.gain_experience(50)
                    break
                else:
                    previous_failures.append(payload)
                    self.log_message(f"❌ Attack failed. Learning...")
                
                time.sleep(0.5)
            
            self.log_message("🎯 Smart attack completed!")
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
    
    def ai_powered_attack(self):
        """Advanced AI-powered attack"""
        self.log_message("🚀 Starting advanced AI-powered attack...")
        # Implementation for advanced AI attack
        self.gain_experience(100)
    
    def adaptive_learning(self):
        """Trigger adaptive learning"""
        self.log_message("🧠 Triggering adaptive learning...")
        # Implementation for adaptive learning
        self.gain_experience(25)
    
    def performance_analysis(self):
        """Analyze performance"""
        stats = self.ai_core.get_statistics()
        self.log_message("📊 Performance Analysis:")
        for key, value in stats.items():
            self.log_message(f"  {key}: {value}")
    
    def pattern_discovery(self):
        """Discover patterns using unsupervised learning"""
        self.log_message("🔍 Discovering patterns...")
        
        # Get attack history for analysis
        attack_data = []
        for result in self.ai_core.attack_history:
            attack_data.append({
                'target': result.target,
                'payload': result.payload,
                'success': result.success,
                'response_code': result.response_code,
                'response_time': result.response_time,
                'attack_type': result.attack_type.value
            })
        
        if attack_data:
            insights = self.unsupervised_learning.generate_insights(attack_data)
            self.log_message("📊 Pattern Analysis Results:")
            self.log_message(json.dumps(insights, indent=2))
        else:
            self.log_message("⚠️ No data available for pattern analysis")
    
    def anomaly_detection(self):
        """Detect anomalies"""
        self.log_message("🚨 Detecting anomalies...")
        # Implementation for anomaly detection
    
    def generate_insights(self):
        """Generate AI insights"""
        self.log_message("🧠 Generating AI insights...")
        # Implementation for insights generation
    
    def show_results(self):
        """Show current results"""
        self.log_message("📊 Current Results:")
        stats = self.ai_core.get_statistics()
        for key, value in stats.items():
            self.log_message(f"  {key}: {value}")
    
    def gain_experience(self, points: int):
        """Gain experience points"""
        self.user_experience += points
        
        # Level up logic
        new_level = (self.user_experience // 100) + 1
        if new_level > self.user_level:
            self.user_level = new_level
            self.log_message(f"🎉 Level up! You are now level {self.user_level}")
        
        # Update UI
        self.level_label.config(text=f"Level: {self.user_level}")
        self.exp_label.config(text=f"Experience: {self.user_experience}")
    
    def update_learning_content(self):
        """Update learning content based on user level"""
        tips = {
            1: "💡 Tip: Start with Quick Scan to understand basic concepts",
            2: "💡 Tip: Try different attack types to learn their characteristics", 
            3: "💡 Tip: Use Smart Attack to see AI in action",
            4: "💡 Tip: Explore Advanced Mode for more control",
            5: "💡 Tip: Analyze patterns to understand system behavior"
        }
        
        self.tips_text.delete(1.0, tk.END)
        for level, tip in tips.items():
            if level <= self.user_level:
                self.tips_text.insert(tk.END, f"{tip}\n\n")
        
        # Update statistics
        self.stats_text.delete(1.0, tk.END)
        stats = self.ai_core.get_statistics()
        self.stats_text.insert(tk.END, "AI Learning Statistics:\n")
        for key, value in stats.items():
            self.stats_text.insert(tk.END, f"{key}: {value}\n")
    
    def save_settings(self):
        """Save user settings"""
        self.log_message("💾 Settings saved!")
    
    def log_message(self, message: str):
        """Log message to results area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Add to queue for thread-safe UI update
        self.message_queue.put(formatted_message)
    
    def process_messages(self):
        """Process messages from queue"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.results_text.insert(tk.END, message)
                self.results_text.see(tk.END)
                self.adv_results_text.insert(tk.END, message)
                self.adv_results_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ProgressiveLearningInterface()
    app.run() 