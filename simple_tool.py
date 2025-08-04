#!/usr/bin/env python3
"""
Simple Penetration Testing Tool - Quick Demo Version
"""

import socket
import requests
import subprocess
import sys
import time
from datetime import datetime
from typing import List, Dict, Any

class SimplePenetrationTool:
    """Simple penetration testing tool with basic functionality."""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def banner(self):
        """Display tool banner."""
        print("🔐 Simple Penetration Testing Tool")
        print("=" * 50)
        print("Built with DevOps & Security as Code principles")
        print("=" * 50)
    
    def port_scan(self, target: str, ports: List[int] = None) -> Dict[str, Any]:
        """Basic port scanner."""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 5432, 8080]
        
        print(f"🔍 Scanning {target} for open ports...")
        open_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    service = self.get_service_name(port)
                    open_ports.append({
                        "port": port,
                        "service": service,
                        "status": "open"
                    })
                    print(f"✅ Port {port} ({service}) - OPEN")
                sock.close()
            except Exception as e:
                print(f"❌ Error scanning port {port}: {e}")
        
        return {
            "target": target,
            "scan_type": "port_scan",
            "open_ports": open_ports,
            "total_ports": len(ports),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_service_name(self, port: int) -> str:
        """Get service name for common ports."""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 5432: "PostgreSQL", 8080: "HTTP-Alt"
        }
        return services.get(port, "Unknown")
    
    def web_vulnerability_scan(self, url: str) -> Dict[str, Any]:
        """Basic web vulnerability scanner."""
        print(f"🌐 Scanning {url} for common vulnerabilities...")
        vulnerabilities = []
        
        # Check for common security headers
        try:
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            
            security_checks = [
                ("X-Frame-Options", "Clickjacking protection"),
                ("X-Content-Type-Options", "MIME type sniffing protection"),
                ("X-XSS-Protection", "XSS protection"),
                ("Strict-Transport-Security", "HSTS"),
                ("Content-Security-Policy", "CSP")
            ]
            
            for header, description in security_checks:
                if header not in headers:
                    vulnerabilities.append({
                        "type": "missing_security_header",
                        "header": header,
                        "description": description,
                        "severity": "medium"
                    })
                    print(f"⚠️  Missing security header: {header}")
            
            # Check for server information disclosure
            if "Server" in headers:
                print(f"ℹ️  Server: {headers['Server']}")
            
            # Check for directory listing
            if "Index of" in response.text or "Directory listing" in response.text:
                vulnerabilities.append({
                    "type": "directory_listing",
                    "description": "Directory listing enabled",
                    "severity": "high"
                })
                print("🚨 Directory listing enabled!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error scanning {url}: {e}")
        
        return {
            "target": url,
            "scan_type": "web_vulnerability",
            "vulnerabilities": vulnerabilities,
            "timestamp": datetime.now().isoformat()
        }
    
    def network_discovery(self, network: str) -> Dict[str, Any]:
        """Basic network discovery."""
        print(f"🌍 Discovering hosts in {network}...")
        active_hosts = []
        
        # Simple ping sweep (Windows compatible)
        base_ip = network.rsplit('.', 1)[0]
        
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            try:
                # Use ping command
                result = subprocess.run(
                    ["ping", "-n", "1", "-w", "1000", ip],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if result.returncode == 0:
                    active_hosts.append(ip)
                    print(f"✅ Host {ip} is active")
                    
            except Exception as e:
                continue
        
        return {
            "network": network,
            "scan_type": "network_discovery",
            "active_hosts": active_hosts,
            "total_hosts": 254,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate a simple text report."""
        report = []
        report.append("🔐 Penetration Testing Report")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Duration: {datetime.now() - self.start_time}")
        report.append("")
        
        for result in results:
            report.append(f"📋 {result['scan_type'].upper()}")
            report.append(f"Target: {result['target']}")
            report.append(f"Timestamp: {result['timestamp']}")
            
            if result['scan_type'] == 'port_scan':
                report.append(f"Open Ports: {len(result['open_ports'])}/{result['total_ports']}")
                for port in result['open_ports']:
                    report.append(f"  - Port {port['port']} ({port['service']})")
            
            elif result['scan_type'] == 'web_vulnerability':
                report.append(f"Vulnerabilities Found: {len(result['vulnerabilities'])}")
                for vuln in result['vulnerabilities']:
                    report.append(f"  - {vuln['type']}: {vuln['description']} ({vuln['severity']})")
            
            elif result['scan_type'] == 'network_discovery':
                report.append(f"Active Hosts: {len(result['active_hosts'])}/{result['total_hosts']}")
                for host in result['active_hosts']:
                    report.append(f"  - {host}")
            
            report.append("")
        
        return "\n".join(report)
    
    def save_report(self, report: str, filename: str = None):
        """Save report to file."""
        if filename is None:
            filename = f"pentest_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"📄 Report saved to: {filename}")

def main():
    """Main function."""
    tool = SimplePenetrationTool()
    tool.banner()
    
    print("Available scans:")
    print("1. Port Scan")
    print("2. Web Vulnerability Scan")
    print("3. Network Discovery")
    print("4. Run All Scans")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == "1":
                target = input("Enter target IP: ").strip()
                if target:
                    result = tool.port_scan(target)
                    tool.results.append(result)
            
            elif choice == "2":
                url = input("Enter target URL (e.g., http://example.com): ").strip()
                if url:
                    result = tool.web_vulnerability_scan(url)
                    tool.results.append(result)
            
            elif choice == "3":
                network = input("Enter network (e.g., 192.168.1.0): ").strip()
                if network:
                    result = tool.network_discovery(network)
                    tool.results.append(result)
            
            elif choice == "4":
                print("Running comprehensive scan...")
                target = input("Enter target IP: ").strip()
                url = input("Enter target URL: ").strip()
                network = input("Enter network: ").strip()
                
                if target:
                    result = tool.port_scan(target)
                    tool.results.append(result)
                
                if url:
                    result = tool.web_vulnerability_scan(url)
                    tool.results.append(result)
                
                if network:
                    result = tool.network_discovery(network)
                    tool.results.append(result)
            
            elif choice == "5":
                break
            
            else:
                print("Invalid option. Please select 1-5.")
                continue
            
            # Ask if user wants to generate report
            if tool.results:
                report_choice = input("\nGenerate report? (y/n): ").strip().lower()
                if report_choice == 'y':
                    report = tool.generate_report(tool.results)
                    print("\n" + report)
                    tool.save_report(report)
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 