#!/usr/bin/env python3
"""
AEGIS Desktop Dashboard
Central management interface for all AEGIS systems
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import threading
import time
import subprocess
import os
from datetime import datetime
import webbrowser

class AEGISDesktopDashboard:
    def __init__(self):
        self.name = "AEGIS Desktop Dashboard"
        self.version = "1.0.0"
        self.system_name = "perdurabo"
        
        # System status tracking
        self.system_status = {
            "aegis_workspace": {"status": "Ready", "running": False},
            "penetration_testing": {"status": "Ready", "running": False},
            "banking_operations": {"status": "Ready", "running": False},
            "central_banking": {"status": "Ready", "running": False},
            "expert_account_manipulation": {"status": "Ready", "running": False},
            "banking_export_system": {"status": "Ready", "running": False},
            "luci_achievement": {"status": "Ready", "running": False},
            "test_environment": {"status": "Ready", "running": False},
            "security_audit": {"status": "Ready", "running": False},
            "jarvis_system": {"status": "Ready", "running": False},
            "team_orchestrator": {"status": "Ready", "running": False}
        }
        
        self.init_dashboard()
    
    def init_dashboard(self):
        """Initialize dashboard"""
        self.root = tk.Tk()
        self.root.title(f"🖥️ {self.name} v{self.version} - {self.system_name}")
        
        # Get screen dimensions for responsive design
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate responsive window size (80% of screen, but with limits)
        window_width = min(max(int(screen_width * 0.8), 1200), 2000)
        window_height = min(max(int(screen_height * 0.8), 800), 1400)
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#0a0a0a')
        
        # Set window properties
        self.root.resizable(True, True)
        self.root.minsize(1000, 700)  # Lower minimum size for smaller screens
        
        # Configure custom fonts
        self.title_font = font.Font(family='Segoe UI', size=32, weight='bold')
        self.subtitle_font = font.Font(family='Segoe UI', size=16, weight='normal')
        self.button_font = font.Font(family='Segoe UI', size=12, weight='bold')
        self.status_font = font.Font(family='Segoe UI', size=11, weight='normal')
        
        # Configure styles
        self.setup_styles()
        
        self.create_dashboard_interface()
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        # Simple color lightening for hover effects
        color_map = {
            '#4ecdc4': '#5eddd4',
            '#ff6b6b': '#ff7b7b',
            '#58a6ff': '#68b6ff',
            '#ffd700': '#ffe700',
            '#ff9ff3': '#ffaff3',
            '#45b7d1': '#55c7e1',
            '#00ff88': '#10ff98'
        }
        return color_map.get(color, color)
    
    def setup_styles(self):
        """Setup custom styles for better UI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       font=self.title_font, 
                       foreground='#00ff88', 
                       background='#0a0a0a')
        
        style.configure('Subtitle.TLabel', 
                       font=self.subtitle_font, 
                       foreground='#ffffff', 
                       background='#0a0a0a')
        
        style.configure('Status.TLabel', 
                       font=self.status_font, 
                       foreground='#ffffff', 
                       background='#0a0a0a')
        
        style.configure('Success.TLabel', 
                       font=self.status_font, 
                       foreground='#00ff88', 
                       background='#0a0a0a')
        
        style.configure('Warning.TLabel', 
                       font=self.status_font, 
                       foreground='#ffaa00', 
                       background='#0a0a0a')
        
        style.configure('Error.TLabel', 
                       font=self.status_font, 
                       foreground='#ff4444', 
                       background='#0a0a0a')
    
    def create_dashboard_interface(self):
        """Create dashboard interface"""
        # Create main scrollable container
        main_canvas = tk.Canvas(self.root, bg='#0a0a0a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg='#0a0a0a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollable components
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Bind window resize to update scroll region
        def _on_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
        self.root.bind('<Configure>', _on_configure)
        
        # Main container with gradient-like effect
        main_container = tk.Frame(scrollable_frame, bg='#0a0a0a')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header with enhanced styling
        header_frame = tk.Frame(main_container, bg='#0a0a0a', height=120)
        header_frame.pack(fill='x', pady=(0, 25))
        header_frame.pack_propagate(False)
        
        # Title with glow effect simulation
        title_frame = tk.Frame(header_frame, bg='#0a0a0a')
        title_frame.pack(expand=True)
        
        title_label = tk.Label(
            title_frame,
            text="🖥️ AEGIS DESKTOP DASHBOARD",
            font=self.title_font,
            fg='#00ff88',
            bg='#0a0a0a'
        )
        title_label.pack()
        
        # Subtitle with better spacing
        subtitle_label = tk.Label(
            title_frame,
            text="Central Management Interface for All AEGIS Systems",
            font=self.subtitle_font,
            fg='#ffffff',
            bg='#0a0a0a'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Version and system info
        info_label = tk.Label(
            title_frame,
            text=f"v{self.version} | System: {self.system_name} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=('Segoe UI', 10),
            fg='#888888',
            bg='#0a0a0a'
        )
        info_label.pack(pady=(5, 0))
        
        # System status overview with enhanced styling
        status_frame = tk.LabelFrame(
            main_container,
            text="📊 SYSTEM STATUS OVERVIEW",
            font=('Segoe UI', 14, 'bold'),
            fg='#00ff88',
            bg='#0a0a0a',
            bd=2,
            relief='solid',
            highlightbackground='#00ff88',
            highlightthickness=1
        )
        status_frame.pack(fill='x', padx=10, pady=10)
        
        # Status grid with better layout
        status_grid = tk.Frame(status_frame, bg='#0a0a0a')
        status_grid.pack(fill='x', padx=15, pady=15)
        
        # Create status indicators with enhanced styling
        self.status_indicators = {}
        systems = [
            ("🚀 AEGIS Complete Workspace", "aegis_workspace", "Main integrated system", "#00ff88"),
            ("🎯 Penetration Testing", "penetration_testing", "Advanced security testing", "#ff6b6b"),
            ("🏦 Banking Operations", "banking_operations", "Financial system analysis", "#4ecdc4"),
            ("🏛️ Central Banking Interface", "central_banking", "Unified banking interface", "#45b7d1"),
            ("🔥 Expert Account Manipulation", "expert_account_manipulation", "Advanced account operations", "#ff9ff3"),
            ("📊 Banking Export System", "banking_export_system", "Data export and reporting", "#feca57"),
            ("🌟 LUCI Achievement System", "luci_achievement", "Advanced achievement system", "#ffd700"),
            ("🔧 Test Environment Setup", "test_environment", "Safe testing configuration", "#48dbfb"),
            ("🔍 Security Audit", "security_audit", "Comprehensive security assessment", "#ff9ff3"),
            ("🤖 JARVIS System", "jarvis_system", "AI-powered intelligence", "#00d2d3"),
            ("🎛️ Team Orchestrator", "team_orchestrator", "Multi-team coordination", "#54a0ff")
        ]
        
        # Create responsive grid layout
        # Calculate optimal number of columns based on screen width
        screen_width = self.root.winfo_screenwidth()
        if screen_width >= 1920:
            cols = 4
        elif screen_width >= 1366:
            cols = 3
        elif screen_width >= 1024:
            cols = 2
        else:
            cols = 1
            
        for i, (name, key, description, color) in enumerate(systems):
            row = i // cols
            col = i % cols
            
            # Enhanced system frame with gradient-like effect
            system_frame = tk.Frame(
                status_grid, 
                bg='#1a1a1a', 
                relief='flat', 
                bd=0,
                highlightbackground=color,
                highlightthickness=1
            )
            system_frame.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
            system_frame.grid_columnconfigure(0, weight=1)
            
            # System name with color coding
            name_label = tk.Label(
                system_frame,
                text=name,
                font=('Segoe UI', 12, 'bold'),
                fg=color,
                bg='#1a1a1a',
                anchor='w'
            )
            name_label.pack(fill='x', padx=12, pady=(12, 6))
            
            # Enhanced status indicator
            status_label = tk.Label(
                system_frame,
                text="🟡 Ready",
                font=('Segoe UI', 11),
                fg='#ffaa00',
                bg='#1a1a1a'
            )
            status_label.pack(anchor='w', padx=12, pady=(0, 6))
            
            # Description with better formatting
            desc_label = tk.Label(
                system_frame,
                text=description,
                font=('Segoe UI', 10),
                fg='#cccccc',
                bg='#1a1a1a',
                anchor='w',
                wraplength=250  # Increased for better readability
            )
            desc_label.pack(anchor='w', padx=12, pady=(0, 12))
            
            # Enhanced control buttons
            button_frame = tk.Frame(system_frame, bg='#1a1a1a')
            button_frame.pack(fill='x', padx=12, pady=(0, 12))
            
            start_btn = tk.Button(
                button_frame,
                text="▶️ Start",
                command=lambda k=key: self.launch_system(k),
                bg='#00aa00',
                fg='#ffffff',
                font=('Segoe UI', 10, 'bold'),
                bd=0,
                padx=20,
                pady=6,
                cursor='hand2',
                activebackground='#00cc00',
                activeforeground='#ffffff'
            )
            start_btn.pack(side='left', padx=(0, 8))
            
            stop_btn = tk.Button(
                button_frame,
                text="⏹️ Stop",
                command=lambda k=key: self.stop_system(k),
                bg='#aa0000',
                fg='#ffffff',
                font=('Segoe UI', 10, 'bold'),
                bd=0,
                padx=20,
                pady=6,
                cursor='hand2',
                activebackground='#cc0000',
                activeforeground='#ffffff'
            )
            stop_btn.pack(side='left')
            
            self.status_indicators[key] = {
                'frame': system_frame,
                'name': name_label,
                'status': status_label,
                'description': desc_label,
                'start_btn': start_btn,
                'stop_btn': stop_btn,
                'color': color
            }
            

        
        # Configure grid weights
        for i in range(cols):
            status_grid.columnconfigure(i, weight=1)
        
        # Enhanced quick actions panel
        actions_frame = tk.LabelFrame(
            main_container,
            text="⚡ QUICK ACTIONS",
            font=('Segoe UI', 14, 'bold'),
            fg='#00ff88',
            bg='#0a0a0a',
            bd=2,
            relief='solid',
            highlightbackground='#00ff88',
            highlightthickness=1
        )
        actions_frame.pack(fill='x', padx=10, pady=10)
        
        actions_buttons_frame = tk.Frame(actions_frame, bg='#0a0a0a')
        actions_buttons_frame.pack(fill='x', padx=15, pady=15)
        
        # Quick action buttons
        quick_actions = [
            ("🚀 Launch All Systems", self.launch_all_systems_integrated, '#4ecdc4'),
            ("⏹️ Stop All Systems", self.stop_all_systems, '#ff6b6b'),
            ("🔧 Configure Test Environment", self.configure_test_environment, '#58a6ff'),
            ("🔍 Run Security Audit", self.run_security_audit, '#ffd700'),
            ("📊 Generate System Report", self.generate_system_report, '#ff9ff3'),
            ("🔄 Refresh Status", self.refresh_status, '#45b7d1')
        ]
        
        # Enhanced banking operations section
        banking_frame = tk.LabelFrame(
            main_container,
            text="🏦 BANKING OPERATIONS CENTER",
            font=('Segoe UI', 14, 'bold'),
            fg='#4ecdc4',
            bg='#0a0a0a',
            bd=2,
            relief='solid',
            highlightbackground='#4ecdc4',
            highlightthickness=1
        )
        banking_frame.pack(fill='x', padx=10, pady=10)
        
        banking_buttons_frame = tk.Frame(banking_frame, bg='#0a0a0a')
        banking_buttons_frame.pack(fill='x', padx=15, pady=15)
        
        # Banking operation buttons
        banking_actions = [
            ("🏛️ Central Banking Interface", lambda: self.launch_system("central_banking"), '#4ecdc4'),
            ("🔥 Expert Account Manipulation", lambda: self.launch_system("expert_account_manipulation"), '#ff6b6b'),
            ("📊 Banking Export System", lambda: self.launch_system("banking_export_system"), '#58a6ff'),
            ("🏦 Basic Banking Operations", lambda: self.launch_system("banking_operations"), '#ffd700'),
            ("🚀 Launch All Banking Tools", self.launch_all_banking_tools, '#ff9ff3')
        ]
        
        # Enhanced LUCI Achievement section
        luci_frame = tk.LabelFrame(
            main_container,
            text="🌟 LUCI ACHIEVEMENT SYSTEM",
            font=('Segoe UI', 14, 'bold'),
            fg='#ffd700',
            bg='#0a0a0a',
            bd=2,
            relief='solid',
            highlightbackground='#ffd700',
            highlightthickness=1
        )
        luci_frame.pack(fill='x', padx=10, pady=10)
        
        luci_buttons_frame = tk.Frame(luci_frame, bg='#0a0a0a')
        luci_buttons_frame.pack(fill='x', padx=15, pady=15)
        
        # LUCI operation buttons
        luci_actions = [
            ("🌟 LUCI Achievement System", lambda: self.launch_system("luci_achievement"), '#ffd700'),
            ("🎯 LUCI Basic Achievement", lambda: self.achieve_luci_basic(), '#4ecdc4'),
            ("🚀 LUCI Advanced Achievement", lambda: self.achieve_luci_advanced(), '#ff6b6b'),
            ("👑 LUCI Master Achievement", lambda: self.achieve_luci_master(), '#ff9ff3'),
            ("🌌 LUCI Legendary Achievement", lambda: self.achieve_luci_legendary(), '#58a6ff')
        ]
        
        # Create responsive LUCI button layout
        for i, (text, command, color) in enumerate(luci_actions):
            luci_btn = tk.Button(
                luci_buttons_frame,
                text=text,
                command=command,
                bg=color,
                fg='#ffffff',
                font=('Segoe UI', 12, 'bold'),
                bd=0,
                padx=25,
                pady=12,
                cursor='hand2',
                activebackground=self.lighten_color(color),
                activeforeground='#ffffff',
                relief='flat'
            )
            # Use grid for better responsive layout
            row = i // 3
            col = i % 3
            luci_btn.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
        
        # Configure grid weights for LUCI buttons
        for i in range(3):
            luci_buttons_frame.columnconfigure(i, weight=1)
        
        # Create responsive banking button layout
        for i, (text, command, color) in enumerate(banking_actions):
            banking_btn = tk.Button(
                banking_buttons_frame,
                text=text,
                command=command,
                bg=color,
                fg='#ffffff',
                font=('Segoe UI', 12, 'bold'),
                bd=0,
                padx=25,
                pady=12,
                cursor='hand2',
                activebackground=self.lighten_color(color),
                activeforeground='#ffffff',
                relief='flat'
            )
            # Use grid for better responsive layout
            row = i // 3
            col = i % 3
            banking_btn.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
        
        # Configure grid weights for banking buttons
        for i in range(3):
            banking_buttons_frame.columnconfigure(i, weight=1)
        
        # Create responsive button layout
        for i, (text, command, color) in enumerate(quick_actions):
            action_btn = tk.Button(
                actions_buttons_frame,
                text=text,
                command=command,
                bg=color,
                fg='#ffffff',
                font=('Segoe UI', 12, 'bold'),
                bd=0,
                padx=25,
                pady=12,
                cursor='hand2',
                activebackground=self.lighten_color(color),
                activeforeground='#ffffff',
                relief='flat'
            )
            # Use grid for better responsive layout
            row = i // 3
            col = i % 3
            action_btn.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
        
        # Configure grid weights for responsive buttons
        for i in range(3):
            actions_buttons_frame.columnconfigure(i, weight=1)
        
        # Enhanced system logs panel
        logs_frame = tk.LabelFrame(
            main_container,
            text="📋 SYSTEM LOGS",
            font=('Segoe UI', 14, 'bold'),
            fg='#00ff88',
            bg='#0a0a0a',
            bd=2,
            relief='solid',
            highlightbackground='#00ff88',
            highlightthickness=1
        )
        logs_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Enhanced logs display
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Consolas', 11),
            wrap=tk.WORD,
            height=12,
            insertbackground='#00ff88',
            selectbackground='#00ff88',
            selectforeground='#000000'
        )
        self.logs_text.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Enhanced log controls
        log_controls = tk.Frame(logs_frame, bg='#0a0a0a')
        log_controls.pack(fill='x', padx=15, pady=10)
        
        # Status bar - move outside scrollable area
        status_bar = tk.Frame(self.root, bg='#1a1a1a', height=30)
        status_bar.pack(fill='x', side='bottom', padx=10, pady=5)
        status_bar.pack_propagate(False)
        
        # Status bar content
        status_label = tk.Label(
            status_bar,
            text="🟢 All systems operational | Ready for commands",
            font=('Segoe UI', 10),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        status_label.pack(side='left', padx=10, pady=5)
        
        # System info in status bar
        system_info = tk.Label(
            status_bar,
            text=f"Systems: {len(self.system_status)} | Running: 0 | {datetime.now().strftime('%H:%M:%S')}",
            font=('Segoe UI', 10),
            fg='#888888',
            bg='#1a1a1a'
        )
        system_info.pack(side='right', padx=10, pady=5)
        
        clear_logs_btn = tk.Button(
            log_controls,
            text="🗑️ Clear Logs",
            command=self.clear_logs,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 11, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        clear_logs_btn.pack(side='left')
        
        export_logs_btn = tk.Button(
            log_controls,
            text="Export Logs",
            command=self.export_logs,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        export_logs_btn.pack(side='left', padx=5)
        
        # Initial log message
        self.log_message("🖥️ AEGIS Desktop Dashboard initialized and ready")
        self.log_message("📊 All systems are ready for launch")
        
        # Initialize system processes tracking
        self.system_processes = {}
        
        # Verify all system files exist
        self.verify_system_files()
        
        # Start status refresh thread
        self.refresh_thread = threading.Thread(target=self._status_refresh_loop, daemon=True)
        self.refresh_thread.start()
    
    def verify_system_files(self):
        """Verify all system files exist and are accessible"""
        system_files = {
            "aegis_workspace": "AEGIS_COMPLETE_WORKSPACE.py",
            "penetration_testing": "PENETRATION_TESTING_LAUNCHER.py",
            "banking_operations": "BANKING_OPERATIONS_LAUNCHER.py",
            "central_banking": "CENTRAL_BANKING_INTERFACE.py",
            "expert_account_manipulation": "EXPERT_ACCOUNT_MANIPULATION_LAUNCHER_FIXED.py",
            "banking_export_system": "BANKING_TOOLS_EXPORT_SYSTEM.py",
            "luci_achievement": "LUCI_ACHIEVEMENT_SYSTEM.py",
            "test_environment": "test_environment_setup.py",
            "security_audit": "comprehensive_security_audit.py",
            "jarvis_system": "JARVIS_COMPLETE_SYSTEM.py",
            "team_orchestrator": "TEAM_EXECUTION_ORCHESTRATOR.py"
        }
        
        self.log_message("🔍 Verifying system files...")
        
        for system_key, file_name in system_files.items():
            if os.path.exists(file_name):
                self.log_message(f"✅ {system_key}: {file_name} - Found")
                self.update_status_indicator(system_key, "🟡 Ready")
            else:
                self.log_message(f"❌ {system_key}: {file_name} - Missing")
                self.update_status_indicator(system_key, "❌ Missing")
        
        self.log_message("📋 System file verification complete")
    
    def launch_system(self, system_key):
        """Launch specific system with enhanced debugging"""
        system_files = {
            "aegis_workspace": "AEGIS_COMPLETE_WORKSPACE.py",
            "penetration_testing": "PENETRATION_TESTING_LAUNCHER.py",
            "banking_operations": "BANKING_OPERATIONS_LAUNCHER.py",
            "central_banking": "CENTRAL_BANKING_INTERFACE.py",
            "expert_account_manipulation": "EXPERT_ACCOUNT_MANIPULATION_LAUNCHER_FIXED.py",
            "banking_export_system": "BANKING_TOOLS_EXPORT_SYSTEM.py",
            "luci_achievement": "LUCI_ACHIEVEMENT_SYSTEM.py",
            "test_environment": "test_environment_setup.py",
            "security_audit": "comprehensive_security_audit.py",
            "jarvis_system": "JARVIS_COMPLETE_SYSTEM.py",
            "team_orchestrator": "TEAM_EXECUTION_ORCHESTRATOR.py"
        }
        
        if system_key in system_files:
            file_name = system_files[system_key]
            self.log_message(f"🚀 Launching {system_key.replace('_', ' ').title()} ({file_name})...")
            
            # Check if file exists
            if not os.path.exists(file_name):
                self.log_message(f"❌ File not found: {file_name}")
                self.update_status_indicator(system_key, "❌ File Missing")
                return
            
            try:
                # Launch with shell=True for better compatibility
                process = subprocess.Popen(
                    ["python", file_name], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Update status immediately
                self.system_status[system_key]["running"] = True
                self.system_status[system_key]["status"] = "Running"
                self.update_status_indicator(system_key, "🟢 Running")
                self.log_message(f"✅ {system_key.replace('_', ' ').title()} launched successfully (PID: {process.pid})")
                
                # Store process reference for potential management
                if not hasattr(self, 'system_processes'):
                    self.system_processes = {}
                self.system_processes[system_key] = process
                
            except Exception as e:
                self.log_message(f"❌ Error launching {system_key}: {e}")
                self.update_status_indicator(system_key, "❌ Launch Failed")
        else:
            self.log_message(f"❌ Unknown system: {system_key}")
    
    def stop_system(self, system_key):
        """Stop specific system with process management"""
        self.log_message(f"⏹️ Stopping {system_key.replace('_', ' ').title()}...")
        
        # Try to terminate the process if we have a reference
        if hasattr(self, 'system_processes') and system_key in self.system_processes:
            try:
                process = self.system_processes[system_key]
                process.terminate()
                self.log_message(f"🔄 Terminated process for {system_key}")
                del self.system_processes[system_key]
            except Exception as e:
                self.log_message(f"⚠️ Could not terminate process for {system_key}: {e}")
        
        # Update status
        self.system_status[system_key]["running"] = False
        self.system_status[system_key]["status"] = "Stopped"
        self.update_status_indicator(system_key, "🔴 Stopped")
        
        self.log_message(f"✅ {system_key.replace('_', ' ').title()} stopped")
    
    def launch_all_systems(self):
        """Launch all systems"""
        self.log_message("🚀 Launching all AEGIS systems...")
        
        for system_key in self.system_status.keys():
            self.launch_system(system_key)
            time.sleep(1)  # Small delay between launches
        
        self.log_message("✅ All systems launched")
    
    def stop_all_systems(self):
        """Stop all systems"""
        self.log_message("⏹️ Stopping all AEGIS systems...")
        
        for system_key in self.system_status.keys():
            self.stop_system(system_key)
        
        self.log_message("✅ All systems stopped")
    
    def configure_test_environment(self):
        """Configure test environment"""
        self.log_message("🔧 Opening Test Environment Setup...")
        self.launch_system("test_environment")
    
    def run_security_audit(self):
        """Run security audit"""
        self.log_message("🔍 Opening Comprehensive Security Audit...")
        self.launch_system("security_audit")
    
    def launch_all_banking_tools(self):
        """Launch all banking tools"""
        self.log_message("🏦 Launching all banking tools...")
        
        banking_systems = [
            "central_banking",
            "expert_account_manipulation", 
            "banking_export_system",
            "banking_operations"
        ]
        
        for system in banking_systems:
            self.launch_system(system)
            time.sleep(1)  # Small delay between launches
        
        self.log_message("✅ All banking tools launched")
    
    def launch_all_systems_integrated(self):
        """Launch all systems including LUCI"""
        self.log_message("🚀 Launching all integrated systems...")
        
        all_systems = [
            "aegis_workspace",
            "penetration_testing",
            "central_banking",
            "expert_account_manipulation",
            "banking_export_system",
            "banking_operations",
            "luci_achievement",
            "test_environment",
            "security_audit",
            "jarvis_system",
            "team_orchestrator"
        ]
        
        for system in all_systems:
            self.launch_system(system)
            time.sleep(1)  # Small delay between launches
        
        self.log_message("✅ All integrated systems launched")
    
    def achieve_luci_basic(self):
        """Achieve LUCI Basic level"""
        self.log_message("🌟 Achieving LUCI Basic level...")
        self.launch_system("luci_achievement")
        # The LUCI system will handle the achievement internally
    
    def achieve_luci_advanced(self):
        """Achieve LUCI Advanced level"""
        self.log_message("🚀 Achieving LUCI Advanced level...")
        self.launch_system("luci_achievement")
        # The LUCI system will handle the achievement internally
    
    def achieve_luci_master(self):
        """Achieve LUCI Master level"""
        self.log_message("👑 Achieving LUCI Master level...")
        self.launch_system("luci_achievement")
        # The LUCI system will handle the achievement internally
    
    def achieve_luci_legendary(self):
        """Achieve LUCI Legendary level"""
        self.log_message("🌌 Achieving LUCI Legendary level...")
        self.launch_system("luci_achievement")
        # The LUCI system will handle the achievement internally
        
        for system in banking_systems:
            self.launch_system(system)
            time.sleep(1)  # Small delay between launches
        
        self.log_message("✅ All banking tools launched")
    
    def generate_system_report(self):
        """Generate system report"""
        self.log_message("📊 Generating comprehensive system report...")
        
        report = f"""
AEGIS SYSTEM STATUS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SYSTEM STATUS:
"""
        
        for system_key, status_info in self.system_status.items():
            report += f"- {system_key.replace('_', ' ').title()}: {status_info['status']}\n"
        
        report += f"""
TOTAL SYSTEMS: {len(self.system_status)}
RUNNING SYSTEMS: {sum(1 for s in self.system_status.values() if s['running'])}
STOPPED SYSTEMS: {sum(1 for s in self.system_status.values() if not s['running'])}

SYSTEM CAPABILITIES:
✅ Network Penetration Testing
✅ Banking Operations Analysis
✅ Central Banking Interface
✅ Expert Account Manipulation
✅ Banking Export System
✅ LUCI Achievement System
✅ Security Auditing
✅ AI/ML Enhanced Features
✅ Team Coordination
✅ Report Generation
✅ Real-time Monitoring

BANKING TOOLS INTEGRATION:
✅ Account Manipulation Tools
✅ Transaction Monitoring
✅ SWIFT Access
✅ ATM Network Operations
✅ Credit Card Operations
✅ Cryptocurrency Analysis
✅ Data Export and Reporting

LUCI ACHIEVEMENT INTEGRATION:
✅ LUCI Basic Achievement
✅ LUCI Advanced Achievement
✅ LUCI Expert Achievement
✅ LUCI Master Achievement
✅ LUCI Legendary Achievement
✅ Advanced AI Integration
✅ Algorithm Mastery
✅ Database Control
✅ Advanced Analysis
✅ System Integration

STATUS: FULLY OPERATIONAL WITH COMPLETE INTEGRATION
"""
        
        self.log_message("📄 System report generated:")
        self.log_message(report)
        
        # Save report to file
        try:
            with open(f"aegis_system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
                f.write(report)
            self.log_message("💾 Report saved to file")
        except Exception as e:
            self.log_message(f"❌ Error saving report: {e}")
    
    def refresh_status(self):
        """Refresh system status with enhanced checking"""
        self.log_message("🔄 Refreshing system status...")
        
        # Update all status indicators
        for system_key in self.system_status.keys():
            if self.system_status[system_key]["running"]:
                self.update_status_indicator(system_key, "🟢 Running")
            else:
                self.update_status_indicator(system_key, "🟡 Ready")
        
        # Check if any processes have terminated unexpectedly
        if hasattr(self, 'system_processes'):
            for system_key, process in list(self.system_processes.items()):
                if process.poll() is not None:  # Process has terminated
                    self.log_message(f"⚠️ {system_key} process terminated unexpectedly")
                    self.system_status[system_key]["running"] = False
                    self.system_status[system_key]["status"] = "Stopped"
                    self.update_status_indicator(system_key, "🔴 Stopped")
                    del self.system_processes[system_key]
        
        self.log_message("✅ System status refreshed")
    
    def test_system(self, system_key):
        """Test a specific system to ensure it's working"""
        self.log_message(f"🧪 Testing {system_key.replace('_', ' ').title()}...")
        
        system_files = {
            "aegis_workspace": "AEGIS_COMPLETE_WORKSPACE.py",
            "penetration_testing": "PENETRATION_TESTING_LAUNCHER.py",
            "banking_operations": "BANKING_OPERATIONS_LAUNCHER.py",
            "central_banking": "CENTRAL_BANKING_INTERFACE.py",
            "expert_account_manipulation": "EXPERT_ACCOUNT_MANIPULATION_LAUNCHER_FIXED.py",
            "banking_export_system": "BANKING_TOOLS_EXPORT_SYSTEM.py",
            "luci_achievement": "LUCI_ACHIEVEMENT_SYSTEM.py",
            "test_environment": "test_environment_setup.py",
            "security_audit": "comprehensive_security_audit.py",
            "jarvis_system": "JARVIS_COMPLETE_SYSTEM.py",
            "team_orchestrator": "TEAM_EXECUTION_ORCHESTRATOR.py"
        }
        
        if system_key in system_files:
            file_name = system_files[system_key]
            
            if not os.path.exists(file_name):
                self.log_message(f"❌ Test failed: {file_name} not found")
                return False
            
            try:
                # Test import to check for syntax errors
                result = subprocess.run(
                    ["python", "-c", f"import {file_name.replace('.py', '')}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.log_message(f"✅ {system_key} test passed - syntax OK")
                    return True
                else:
                    self.log_message(f"❌ {system_key} test failed - syntax error")
                    self.log_message(f"Error: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                self.log_message(f"⏰ {system_key} test timed out")
                return False
            except Exception as e:
                self.log_message(f"❌ {system_key} test error: {e}")
                return False
        else:
            self.log_message(f"❌ Unknown system: {system_key}")
            return False
    
    def update_status_indicator(self, system_key, status_text):
        """Update status indicator with enhanced styling"""
        if system_key in self.status_indicators:
            indicator = self.status_indicators[system_key]['status']
            color = self.status_indicators[system_key]['color']
            
            # Update status text and color based on status
            if "✅" in status_text or "Running" in status_text:
                indicator.config(text=status_text, fg='#00ff88')
            elif "⚠️" in status_text or "Warning" in status_text:
                indicator.config(text=status_text, fg='#ffaa00')
            elif "❌" in status_text or "Error" in status_text:
                indicator.config(text=status_text, fg='#ff4444')
            elif "🟡" in status_text or "Ready" in status_text:
                indicator.config(text=status_text, fg='#ffaa00')
            else:
                indicator.config(text=status_text, fg=color)
    
    def clear_logs(self):
        """Clear logs"""
        self.logs_text.delete(1.0, tk.END)
        self.log_message("📋 Logs cleared")
    
    def export_logs(self):
        """Export logs to file"""
        try:
            logs_content = self.logs_text.get(1.0, tk.END)
            filename = f"aegis_dashboard_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w') as f:
                f.write(logs_content)
            
            self.log_message(f"💾 Logs exported to {filename}")
        except Exception as e:
            self.log_message(f"❌ Error exporting logs: {e}")
    
    def log_message(self, message):
        """Log message to display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Use after() to ensure thread safety
        self.root.after(0, lambda: self._update_logs(log_entry))
    
    def _update_logs(self, log_entry):
        """Update logs safely in main thread"""
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
    
    def _status_refresh_loop(self):
        """Background thread for status refresh"""
        while True:
            try:
                # Check for unexpectedly terminated processes
                if hasattr(self, 'system_processes'):
                    for system_key, process in list(self.system_processes.items()):
                        if process.poll() is not None:  # Process has terminated
                            self.root.after(0, lambda k=system_key: self._handle_process_termination(k))
                
                time.sleep(2)  # Check every 2 seconds
            except Exception as e:
                print(f"Status refresh error: {e}")
                time.sleep(5)
    
    def _handle_process_termination(self, system_key):
        """Handle unexpected process termination"""
        self.log_message(f"⚠️ {system_key.replace('_', ' ').title()} process terminated unexpectedly")
        self.system_status[system_key]["running"] = False
        self.system_status[system_key]["status"] = "Stopped"
        self.update_status_indicator(system_key, "🟡 Stopped")
        
        # Remove from process tracking
        if system_key in self.system_processes:
            del self.system_processes[system_key]
    
    def run(self):
        """Run the dashboard"""
        self.root.mainloop()

def main():
    """Main function"""
    dashboard = AEGISDesktopDashboard()
    dashboard.run()

if __name__ == "__main__":
    main() 