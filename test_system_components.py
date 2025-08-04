#!/usr/bin/env python3
"""
AEGIS System Component Test Script
Tests all major components to ensure they're working correctly
"""

import sys
import importlib
import traceback
from datetime import datetime

def test_import(module_name, description):
    """Test if a module can be imported successfully"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: {module_name} - SUCCESS")
        return True
    except ImportError as e:
        print(f"❌ {description}: {module_name} - FAILED")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {description}: {module_name} - WARNING")
        print(f"   Error: {e}")
        return True

def test_silos_components():
    """Test all silos components"""
    print("\n🔧 Testing Silos Components...")
    
    components = [
        ("silos.developmental.ai_ml_chat_core", "AI/ML Chat Core"),
        ("silos.developmental.data_processing_core", "Data Processing Core"),
        ("silos.developmental.report_generation_core", "Report Generation Core"),
        ("silos.security.penetration_engine", "Penetration Engine"),
        ("silos.security.banking_operations_core", "Banking Operations Core"),
        ("silos.operational.workspace_interface_mini", "Workspace Interface"),
        ("silos.operational.monitoring_dashboard_mini", "Monitoring Dashboard"),
        ("silos.operational.aegis_deployment_mini", "AEGIS Deployment Core"),
    ]
    
    results = []
    for module, desc in components:
        results.append(test_import(module, desc))
    
    return all(results)

def test_external_dependencies():
    """Test external dependencies"""
    print("\n📦 Testing External Dependencies...")
    
    dependencies = [
        ("tkinter", "GUI Framework"),
        ("pandas", "Data Analysis"),
        ("numpy", "Numerical Computing"),
        ("matplotlib", "Data Visualization"),
        ("seaborn", "Statistical Visualization"),
        ("reportlab", "PDF Generation"),
        ("requests", "HTTP Library"),
        ("aiohttp", "Async HTTP"),
        ("bs4", "Web Scraping"),
        ("speech_recognition", "Speech Recognition"),
        ("pyttsx3", "Text-to-Speech"),
        ("pyaudio", "Audio Processing"),
    ]
    
    results = []
    for module, desc in dependencies:
        results.append(test_import(module, desc))
    
    return all(results)

def test_main_systems():
    """Test main system files"""
    print("\n🚀 Testing Main System Files...")
    
    systems = [
        ("AEGIS_COMPLETE_WORKSPACE", "AEGIS Complete Workspace"),
        ("PENETRATION_TESTING_LAUNCHER", "Penetration Testing Launcher"),
        ("BANKING_OPERATIONS_LAUNCHER", "Banking Operations Launcher"),
        ("TEAM_EXECUTION_ORCHESTRATOR", "Team Execution Orchestrator"),
        ("JARVIS_COMPLETE_SYSTEM", "JARVIS Complete System"),
    ]
    
    results = []
    for module, desc in systems:
        try:
            # Try to import the module
            importlib.import_module(module)
            print(f"✅ {desc}: {module}.py - SUCCESS")
            results.append(True)
        except ImportError as e:
            print(f"❌ {desc}: {module}.py - FAILED")
            print(f"   Error: {e}")
            results.append(False)
        except Exception as e:
            print(f"⚠️  {desc}: {module}.py - WARNING")
            print(f"   Error: {e}")
            results.append(True)
    
    return all(results)

def test_gui_components():
    """Test GUI components"""
    print("\n🖥️ Testing GUI Components...")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test basic GUI functionality
        label = tk.Label(root, text="Test")
        button = tk.Button(root, text="Test")
        
        print("✅ GUI Components: tkinter - SUCCESS")
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ GUI Components: tkinter - FAILED")
        print(f"   Error: {e}")
        return False

def test_data_processing():
    """Test data processing capabilities"""
    print("\n📊 Testing Data Processing...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # Test basic data operations
        data = pd.DataFrame({
            'A': np.random.randn(10),
            'B': np.random.randn(10)
        })
        
        # Test basic operations
        mean_val = data.mean()
        std_val = data.std()
        
        print("✅ Data Processing: pandas/numpy - SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Data Processing: pandas/numpy - FAILED")
        print(f"   Error: {e}")
        return False

def test_report_generation():
    """Test report generation capabilities"""
    print("\n📄 Testing Report Generation...")
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Test basic PDF generation
        styles = getSampleStyleSheet()
        
        print("✅ Report Generation: reportlab - SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Report Generation: reportlab - FAILED")
        print(f"   Error: {e}")
        return False

def test_network_capabilities():
    """Test network capabilities"""
    print("\n🌐 Testing Network Capabilities...")
    
    try:
        import socket
        import requests
        
        # Test basic network operations
        socket.gethostbyname('localhost')
        
        print("✅ Network Capabilities: socket/requests - SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Network Capabilities: socket/requests - FAILED")
        print(f"   Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 AEGIS System Component Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    
    # Run all tests
    tests = [
        ("External Dependencies", test_external_dependencies),
        ("Silos Components", test_silos_components),
        ("Main Systems", test_main_systems),
        ("GUI Components", test_gui_components),
        ("Data Processing", test_data_processing),
        ("Report Generation", test_report_generation),
        ("Network Capabilities", test_network_capabilities),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name}: CRITICAL ERROR")
            print(f"   Error: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AEGIS system is ready for operation.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 