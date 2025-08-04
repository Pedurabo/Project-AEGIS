#!/usr/bin/env python3
"""
AEGIS System Status Checker
Quick verification of all system components
"""

import subprocess
import sys
import time
from datetime import datetime

def check_system_status():
    """Check status of all AEGIS systems"""
    print("🔍 AEGIS System Status Checker")
    print("=" * 50)
    print(f"Check started at: {datetime.now()}")
    print()
    
    # Systems to check
    systems = [
        ("AEGIS Complete Workspace", "AEGIS_COMPLETE_WORKSPACE.py"),
        ("Penetration Testing Launcher", "PENETRATION_TESTING_LAUNCHER.py"),
        ("Banking Operations Launcher", "BANKING_OPERATIONS_LAUNCHER.py"),
        ("Test Environment Setup", "test_environment_setup.py"),
        ("Comprehensive Security Audit", "comprehensive_security_audit.py"),
        ("JARVIS Complete System", "JARVIS_COMPLETE_SYSTEM.py"),
        ("Team Execution Orchestrator", "TEAM_EXECUTION_ORCHESTRATOR.py"),
        ("Desktop Dashboard", "AEGIS_DESKTOP_DASHBOARD.py")
    ]
    
    results = []
    
    for name, file in systems:
        print(f"🔍 Checking {name}...")
        
        try:
            # Try to import the module to check for syntax errors
            result = subprocess.run([sys.executable, "-c", f"import {file.replace('.py', '')}"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"✅ {name}: Ready to launch")
                results.append((name, "Ready"))
            else:
                print(f"⚠️  {name}: Import issues detected")
                print(f"   Error: {result.stderr.strip()}")
                results.append((name, "Issues"))
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {name}: Timeout during check")
            results.append((name, "Timeout"))
        except Exception as e:
            print(f"❌ {name}: Error during check")
            print(f"   Error: {e}")
            results.append((name, "Error"))
        
        print()
    
    # Summary
    print("📊 STATUS SUMMARY")
    print("=" * 50)
    
    ready_count = sum(1 for _, status in results if status == "Ready")
    total_count = len(results)
    
    for name, status in results:
        status_icon = "✅" if status == "Ready" else "⚠️" if status == "Issues" else "❌"
        print(f"{status_icon} {name}: {status}")
    
    print()
    print(f"Overall: {ready_count}/{total_count} systems ready")
    
    if ready_count == total_count:
        print("🎉 All AEGIS systems are ready for operation!")
        return True
    else:
        print("⚠️  Some systems have issues that need attention.")
        return False

if __name__ == "__main__":
    check_system_status() 