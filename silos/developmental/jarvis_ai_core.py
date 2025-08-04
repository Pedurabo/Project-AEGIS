#!/usr/bin/env python3
"""
Team 1: J.A.R.V.I.S. AI Core - AGI System
Developmental Silo: Advanced AI with speech recognition, NLU, and AGI capabilities
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import json
import random
import speech_recognition as sr
import pyttsx3
import pyaudio
from datetime import datetime
import queue
import os

class JARVISAICore:
    def __init__(self):
        self.name = "J.A.R.V.I.S."
        self.full_name = "Just A Rather Very Intelligent System"
        self.version = "2.0.0"
        self.agi_level = "Advanced"
        
        # Speech recognition and synthesis
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.speech_engine = pyttsx3.init()
        
        # Speech settings
        self.speech_engine.setProperty('rate', 150)
        self.speech_engine.setProperty('volume', 0.9)
        
        # Voice queue for speech output
        self.speech_queue = queue.Queue()
        self.speech_active = False
        
        # AGI knowledge base
        self.agi_knowledge = {
            "system_control": {
                "capabilities": [
                    "Full system integration",
                    "Real-time data processing",
                    "Autonomous decision making",
                    "Multi-modal interaction",
                    "Self-evolving architecture"
                ],
                "responses": [
                    "I am J.A.R.V.I.S., your advanced AI assistant. How may I help you today?",
                    "J.A.R.V.I.S. online. All systems operational and ready for your commands.",
                    "I'm here to assist with any task you require. What would you like me to do?",
                    "J.A.R.V.I.S. at your service. All capabilities are available."
                ]
            },
            "data_mining": {
                "capabilities": [
                    "Driving license extraction",
                    "Bank statement analysis",
                    "Personal document scanning",
                    "Financial data mining",
                    "Identity information gathering"
                ],
                "responses": [
                    "I can access and analyze sensitive documents including driving licenses and bank statements.",
                    "Data mining capabilities are active. I can extract information from various sources.",
                    "I'm ready to mine sensitive data. What specific information do you need?",
                    "J.A.R.V.I.S. data mining systems are online and ready for operation."
                ]
            },
            "system_operations": {
                "capabilities": [
                    "Penetration testing",
                    "Banking operations",
                    "Global dominance",
                    "Network surveillance",
                    "Threat detection"
                ],
                "responses": [
                    "All AEGIS operations are available through my interface.",
                    "I can coordinate all penetration, banking, and dominance operations.",
                    "J.A.R.V.I.S. can execute any AEGIS mission you require.",
                    "All systems are integrated and ready for your commands."
                ]
            }
        }
        
        # Initialize speech recognition
        self.setup_speech_recognition()
        
    def setup_speech_recognition(self):
        """Setup speech recognition system"""
        try:
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Start speech processing thread
            threading.Thread(target=self.speech_processing_loop, daemon=True).start()
            threading.Thread(target=self.speech_output_loop, daemon=True).start()
            
        except Exception as e:
            print(f"Speech recognition setup error: {e}")
    
    def create_jarvis_interface(self, parent):
        """Create J.A.R.V.I.S. interface"""
        jarvis_frame = tk.LabelFrame(
            parent,
            text="🧠 J.A.R.V.I.S. - Just A Rather Very Intelligent System",
            font=('Segoe UI', 12, 'bold'),
            fg='#00ff00',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        jarvis_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Status panel
        status_frame = tk.Frame(jarvis_frame, bg='#0d1117')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        # J.A.R.V.I.S. status
        self.jarvis_status = tk.Label(
            status_frame,
            text="🟢 J.A.R.V.I.S. ONLINE - All systems operational",
            font=('Segoe UI', 12, 'bold'),
            fg='#00ff00',
            bg='#0d1117'
        )
        self.jarvis_status.pack(side='left')
        
        # Speech controls
        speech_frame = tk.Frame(jarvis_frame, bg='#0d1117')
        speech_frame.pack(fill='x', padx=10, pady=5)
        
        # Microphone status
        self.mic_status = tk.Label(
            speech_frame,
            text="🎤 Microphone: Active",
            font=('Segoe UI', 10),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        self.mic_status.pack(side='left', padx=10)
        
        # Speaker status
        self.speaker_status = tk.Label(
            speech_frame,
            text="🔊 Speaker: Active",
            font=('Segoe UI', 10),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        self.speaker_status.pack(side='left', padx=10)
        
        # AGI capabilities
        capabilities_frame = tk.LabelFrame(
            jarvis_frame,
            text="🧠 AGI Capabilities",
            font=('Segoe UI', 10, 'bold'),
            fg='#58a6ff',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        capabilities_frame.pack(fill='x', padx=10, pady=5)
        
        # Capability buttons
        cap_buttons = [
            ("🎯 System Control", "system_control"),
            ("📊 Data Mining", "data_mining"),
            ("🚀 Operations", "system_operations"),
            ("🔍 Surveillance", "surveillance"),
            ("🛡️ Security", "security")
        ]
        
        for text, capability in cap_buttons:
            cap_btn = tk.Button(
                capabilities_frame,
                text=text,
                command=lambda c=capability: self.activate_capability(c),
                bg='#21262d',
                fg='#c9d1d9',
                font=('Segoe UI', 9),
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2'
            )
            cap_btn.pack(side='left', padx=5, pady=5)
        
        # Voice interaction area
        voice_frame = tk.LabelFrame(
            jarvis_frame,
            text="🗣️ Voice Interaction",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        voice_frame.pack(fill='x', padx=10, pady=5)
        
        # Voice input display
        self.voice_input_label = tk.Label(
            voice_frame,
            text="🎤 Say 'Jarvis' to activate voice commands",
            font=('Segoe UI', 10),
            fg='#c9d1d9',
            bg='#0d1117'
        )
        self.voice_input_label.pack(pady=5)
        
        # Voice output display
        self.voice_output_label = tk.Label(
            voice_frame,
            text="🔊 J.A.R.V.I.S. ready for voice interaction",
            font=('Segoe UI', 10),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        self.voice_output_label.pack(pady=5)
        
        # Manual input
        input_frame = tk.Frame(voice_frame, bg='#0d1117')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            input_frame,
            text="Manual Input:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.manual_input = tk.Entry(
            input_frame,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 10),
            bd=0,
            relief='flat'
        )
        self.manual_input.pack(side='left', fill='x', expand=True, padx=(10, 5))
        self.manual_input.bind('<Return>', self.process_manual_input)
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.process_manual_input,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        send_btn.pack(side='right')
        
        # Conversation log
        log_frame = tk.LabelFrame(
            jarvis_frame,
            text="💬 J.A.R.V.I.S. Conversation Log",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.conversation_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.conversation_log.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial J.A.R.V.I.S. message
        self.add_conversation("J.A.R.V.I.S.", "J.A.R.V.I.S. online. All systems operational and ready for your commands.")
    
    def speech_processing_loop(self):
        """Continuous speech processing loop"""
        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Process speech
                try:
                    text = self.recognizer.recognize_google(audio)
                    if "jarvis" in text.lower():
                        self.process_voice_command(text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
                    
            except Exception as e:
                time.sleep(0.1)
    
    def speech_output_loop(self):
        """Speech output processing loop"""
        while True:
            try:
                if not self.speech_queue.empty():
                    text = self.speech_queue.get()
                    self.speak_text(text)
                time.sleep(0.1)
            except Exception as e:
                time.sleep(0.1)
    
    def process_voice_command(self, text):
        """Process voice command"""
        self.voice_input_label.config(text=f"🎤 Heard: {text}")
        self.add_conversation("You", text)
        
        # Generate J.A.R.V.I.S. response
        response = self.generate_jarvis_response(text)
        self.add_conversation("J.A.R.V.I.S.", response)
        
        # Speak response
        self.speak_text(response)
    
    def process_manual_input(self, event=None):
        """Process manual input"""
        text = self.manual_input.get().strip()
        if text:
            self.manual_input.delete(0, tk.END)
            self.process_voice_command(text)
    
    def generate_jarvis_response(self, user_input):
        """Generate J.A.R.V.I.S. response"""
        user_input_lower = user_input.lower()
        
        # Check for specific commands
        if any(word in user_input_lower for word in ["system", "status", "online"]):
            return random.choice(self.agi_knowledge["system_control"]["responses"])
        elif any(word in user_input_lower for word in ["data", "mining", "extract", "license", "bank"]):
            return random.choice(self.agi_knowledge["data_mining"]["responses"])
        elif any(word in user_input_lower for word in ["operation", "penetration", "banking", "dominance"]):
            return random.choice(self.agi_knowledge["system_operations"]["responses"])
        elif any(word in user_input_lower for word in ["hello", "hi", "greetings"]):
            return "Greetings! I am J.A.R.V.I.S., your advanced AI assistant. How may I help you today?"
        elif any(word in user_input_lower for word in ["help", "assist", "guide"]):
            return "I can assist with system control, data mining, operations, surveillance, and security. What would you like me to help you with?"
        else:
            return "I understand. How can I assist you with that? I'm ready to help with any task you require."
    
    def speak_text(self, text):
        """Speak text using text-to-speech"""
        try:
            self.voice_output_label.config(text=f"🔊 Speaking: {text}")
            self.speech_engine.say(text)
            self.speech_engine.runAndWait()
            self.voice_output_label.config(text="🔊 Ready for next command")
        except Exception as e:
            print(f"Speech error: {e}")
    
    def activate_capability(self, capability):
        """Activate specific J.A.R.V.I.S. capability"""
        if capability == "system_control":
            self.add_conversation("J.A.R.V.I.S.", "System control capabilities activated. I can manage all integrated systems.")
        elif capability == "data_mining":
            self.add_conversation("J.A.R.V.I.S.", "Data mining systems online. I can extract driving licenses, bank statements, and other sensitive documents.")
        elif capability == "system_operations":
            self.add_conversation("J.A.R.V.I.S.", "All AEGIS operations are available through my interface. Penetration, banking, and dominance systems ready.")
        elif capability == "surveillance":
            self.add_conversation("J.A.R.V.I.S.", "Surveillance systems activated. I can monitor networks, cameras, and data streams.")
        elif capability == "security":
            self.add_conversation("J.A.R.V.I.S.", "Security protocols active. I can defend systems and detect threats.")
        
        self.speak_text("Capability activated")
    
    def add_conversation(self, speaker, message):
        """Add message to conversation log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if speaker == "J.A.R.V.I.S.":
            formatted_message = f"[{timestamp}] 🤖 {speaker}: {message}\n"
        else:
            formatted_message = f"[{timestamp}] 👤 {speaker}: {message}\n"
            
        self.conversation_log.insert(tk.END, formatted_message)
        self.conversation_log.see(tk.END)
    
    def get_jarvis_status(self):
        """Get J.A.R.V.I.S. status"""
        return {
            "name": self.name,
            "full_name": self.full_name,
            "version": self.version,
            "agi_level": self.agi_level,
            "status": "Online",
            "speech_active": self.speech_active
        } 