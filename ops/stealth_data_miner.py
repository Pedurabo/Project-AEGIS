"""
OPERATIONAL SILO - Stealth Data Mining
Advanced data mining capabilities with detection avoidance
"""

import requests
import time
import random
import hashlib
import json
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from urllib.parse import urljoin, urlparse
import re

logger = logging.getLogger(__name__)


class StealthDataMiner:
    """Advanced stealth data mining with detection avoidance"""
    
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
        ]
        self.proxy_list = []
        self.current_proxy = None
        self.request_delay = (1, 3)  # Random delay between requests
        self.max_retries = 3
        self.detected_patterns = []
        self.mined_data = []
        
        # Setup stealth session
        self._setup_stealth_session()
    
    def _setup_stealth_session(self):
        """Setup session with stealth capabilities"""
        # Random user agent
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Add random headers to avoid fingerprinting
        self._add_random_headers()
    
    def _add_random_headers(self):
        """Add random headers to avoid detection"""
        random_headers = {
            'DNT': random.choice(['0', '1']),
            'Sec-Fetch-Dest': random.choice(['document', 'empty']),
            'Sec-Fetch-Mode': random.choice(['navigate', 'cors']),
            'Sec-Fetch-Site': random.choice(['none', 'same-origin']),
            'Cache-Control': random.choice(['max-age=0', 'no-cache']),
        }
        self.session.headers.update(random_headers)
    
    def _rotate_user_agent(self):
        """Rotate user agent to avoid detection"""
        self.session.headers['User-Agent'] = random.choice(self.user_agents)
    
    def _add_proxy(self, proxy: str):
        """Add proxy for request rotation"""
        self.proxy_list.append(proxy)
    
    def _get_random_proxy(self) -> Optional[Dict]:
        """Get random proxy from list"""
        if not self.proxy_list:
            return None
        
        proxy = random.choice(self.proxy_list)
        return {
            'http': proxy,
            'https': proxy
        }
    
    def _stealth_delay(self):
        """Add random delay to avoid rate limiting"""
        delay = random.uniform(*self.request_delay)
        time.sleep(delay)
    
    def _is_detected(self, response: requests.Response) -> bool:
        """Check if request was detected as suspicious"""
        detection_indicators = [
            'blocked', 'forbidden', 'access denied', 'rate limit',
            'captcha', 'security check', 'suspicious activity',
            '403', '429', '503'
        ]
        
        response_text = response.text.lower()
        status_code = response.status_code
        
        # Check status codes
        if status_code in [403, 429, 503]:
            return True
        
        # Check response content
        for indicator in detection_indicators:
            if indicator in response_text:
                return True
        
        return False
    
    def mine_api_endpoints(self, base_url: str) -> List[Dict]:
        """Mine API endpoints stealthily"""
        print(f"🔍 Mining API endpoints from {base_url}")
        
        common_endpoints = [
            '/api', '/api/v1', '/api/v2', '/rest', '/graphql',
            '/swagger', '/docs', '/openapi', '/health', '/status',
            '/admin', '/user', '/auth', '/login', '/register',
            '/data', '/users', '/posts', '/comments', '/files'
        ]
        
        discovered_endpoints = []
        
        for endpoint in common_endpoints:
            try:
                url = urljoin(base_url, endpoint)
                
                # Add stealth delay
                self._stealth_delay()
                
                # Rotate user agent
                self._rotate_user_agent()
                
                # Make request
                response = self.session.get(url, timeout=10)
                
                if not self._is_detected(response):
                    endpoint_info = {
                        'url': url,
                        'status_code': response.status_code,
                        'content_type': response.headers.get('content-type', ''),
                        'content_length': len(response.text),
                        'discovered_at': datetime.now().isoformat()
                    }
                    
                    # Analyze response
                    if response.status_code == 200:
                        endpoint_info['accessible'] = True
                        endpoint_info['data_structure'] = self._analyze_data_structure(response.text)
                    elif response.status_code in [401, 403]:
                        endpoint_info['requires_auth'] = True
                    elif response.status_code == 404:
                        endpoint_info['not_found'] = True
                    
                    discovered_endpoints.append(endpoint_info)
                    print(f"✅ Discovered: {url} ({response.status_code})")
                
            except Exception as e:
                logger.debug(f"Error mining endpoint {endpoint}: {e}")
                continue
        
        return discovered_endpoints
    
    def _analyze_data_structure(self, content: str) -> Dict:
        """Analyze data structure of response"""
        structure = {
            'is_json': False,
            'is_xml': False,
            'is_html': False,
            'fields': [],
            'arrays': [],
            'nested_objects': []
        }
        
        # Check if JSON
        try:
            json_data = json.loads(content)
            structure['is_json'] = True
            structure['fields'] = self._extract_json_fields(json_data)
        except:
            pass
        
        # Check if XML
        if content.strip().startswith('<?xml') or content.strip().startswith('<'):
            structure['is_xml'] = True
        
        # Check if HTML
        if '<html' in content.lower():
            structure['is_html'] = True
        
        return structure
    
    def _extract_json_fields(self, data: Any, prefix: str = '') -> List[str]:
        """Extract field names from JSON data"""
        fields = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                field_name = f"{prefix}.{key}" if prefix else key
                fields.append(field_name)
                
                if isinstance(value, (dict, list)):
                    fields.extend(self._extract_json_fields(value, field_name))
        
        elif isinstance(data, list) and data:
            fields.extend(self._extract_json_fields(data[0], f"{prefix}[0]"))
        
        return fields
    
    def mine_database_info(self, target_url: str) -> Dict:
        """Mine database information stealthily"""
        print(f"🗄️ Mining database information from {target_url}")
        
        db_indicators = {
            'mysql': ['mysql', 'mysqli', 'mysql_error', 'mysql_connect'],
            'postgresql': ['postgres', 'postgresql', 'pg_', 'psql'],
            'sqlite': ['sqlite', 'sqlite3', '.db', '.sqlite'],
            'mongodb': ['mongodb', 'mongo', 'ObjectId', 'MongoDB'],
            'redis': ['redis', 'Redis', 'redis_connect'],
            'oracle': ['oracle', 'oci_', 'Oracle', 'ORA-']
        }
        
        discovered_info = {
            'database_type': None,
            'connection_strings': [],
            'error_messages': [],
            'config_files': [],
            'backup_files': []
        }
        
        # Common error patterns
        error_patterns = [
            r'ORA-\d+',  # Oracle errors
            r'MySQL.*error',  # MySQL errors
            r'PostgreSQL.*error',  # PostgreSQL errors
            r'SQLite.*error',  # SQLite errors
            r'MongoDB.*error',  # MongoDB errors
            r'Redis.*error',  # Redis errors
        ]
        
        try:
            # Add stealth delay
            self._stealth_delay()
            
            # Make request
            response = self.session.get(target_url, timeout=10)
            
            if not self._is_detected(response):
                content = response.text.lower()
                
                # Check for database indicators
                for db_type, indicators in db_indicators.items():
                    for indicator in indicators:
                        if indicator in content:
                            discovered_info['database_type'] = db_type
                            break
                    if discovered_info['database_type']:
                        break
                
                # Check for error messages
                for pattern in error_patterns:
                    matches = re.findall(pattern, response.text, re.IGNORECASE)
                    discovered_info['error_messages'].extend(matches)
                
                # Look for config files
                config_files = [
                    '/config.php', '/config.json', '/.env', '/wp-config.php',
                    '/database.yml', '/config.yml', '/settings.py'
                ]
                
                for config_file in config_files:
                    try:
                        config_url = urljoin(target_url, config_file)
                        self._stealth_delay()
                        config_response = self.session.get(config_url, timeout=5)
                        
                        if config_response.status_code == 200:
                            discovered_info['config_files'].append({
                                'file': config_file,
                                'url': config_url,
                                'size': len(config_response.text)
                            })
                    except:
                        continue
                
        except Exception as e:
            logger.debug(f"Error mining database info: {e}")
        
        return discovered_info
    
    def mine_user_data(self, target_url: str) -> List[Dict]:
        """Mine user data stealthily"""
        print(f"👥 Mining user data from {target_url}")
        
        user_data = []
        
        # Common user data endpoints
        user_endpoints = [
            '/users', '/user', '/profile', '/account', '/members',
            '/admin/users', '/api/users', '/api/user', '/api/profiles'
        ]
        
        for endpoint in user_endpoints:
            try:
                url = urljoin(target_url, endpoint)
                
                # Add stealth delay
                self._stealth_delay()
                
                # Rotate user agent
                self._rotate_user_agent()
                
                # Make request
                response = self.session.get(url, timeout=10)
                
                if not self._is_detected(response) and response.status_code == 200:
                    # Parse user data
                    users = self._parse_user_data(response.text)
                    user_data.extend(users)
                    
                    print(f"✅ Found {len(users)} users from {endpoint}")
                
            except Exception as e:
                logger.debug(f"Error mining user data from {endpoint}: {e}")
                continue
        
        return user_data
    
    def _parse_user_data(self, content: str) -> List[Dict]:
        """Parse user data from response"""
        users = []
        
        # Try to parse as JSON
        try:
            data = json.loads(content)
            if isinstance(data, list):
                for user in data:
                    if isinstance(user, dict):
                        users.append({
                            'id': user.get('id'),
                            'username': user.get('username', user.get('name')),
                            'email': user.get('email'),
                            'role': user.get('role', user.get('type')),
                            'created_at': user.get('created_at', user.get('created')),
                            'source': 'json'
                        })
            elif isinstance(data, dict) and 'users' in data:
                users.extend(self._parse_user_data(json.dumps(data['users'])))
        except:
            pass
        
        # Try to parse HTML for user information
        if not users:
            # Look for user patterns in HTML
            user_patterns = [
                r'user["\']?\s*:\s*["\']([^"\']+)["\']',
                r'username["\']?\s*:\s*["\']([^"\']+)["\']',
                r'email["\']?\s*:\s*["\']([^"\']+)["\']',
                r'<span[^>]*class="[^"]*user[^"]*"[^>]*>([^<]+)</span>',
                r'<div[^>]*class="[^"]*username[^"]*"[^>]*>([^<]+)</div>'
            ]
            
            for pattern in user_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    users.append({
                        'username': match,
                        'source': 'html_pattern'
                    })
        
        return users
    
    def mine_system_info(self, target_url: str) -> Dict:
        """Mine system information stealthily"""
        print(f"🖥️ Mining system information from {target_url}")
        
        system_info = {
            'server': None,
            'framework': None,
            'languages': [],
            'technologies': [],
            'headers': {},
            'ports': [],
            'services': []
        }
        
        try:
            # Add stealth delay
            self._stealth_delay()
            
            # Make request
            response = self.session.get(target_url, timeout=10)
            
            if not self._is_detected(response):
                # Extract server information
                server_header = response.headers.get('Server', '')
                if server_header:
                    system_info['server'] = server_header
                
                # Extract all headers
                system_info['headers'] = dict(response.headers)
                
                # Detect framework and technologies
                content = response.text.lower()
                
                # Framework detection
                frameworks = {
                    'django': ['csrf_token', 'django', 'admin/login'],
                    'flask': ['flask', 'jinja2', 'werkzeug'],
                    'laravel': ['laravel', 'csrf_token', 'laravel_session'],
                    'rails': ['rails', 'ruby', 'erb'],
                    'asp.net': ['asp.net', 'viewstate', '__viewstate'],
                    'php': ['php', 'phpmyadmin', 'wordpress'],
                    'node.js': ['node.js', 'express', 'npm'],
                    'angular': ['ng-', 'angular', 'ng-app'],
                    'react': ['react', 'jsx', 'createelement'],
                    'vue': ['vue', 'v-', 'vue.js']
                }
                
                for framework, indicators in frameworks.items():
                    for indicator in indicators:
                        if indicator in content:
                            system_info['framework'] = framework
                            break
                    if system_info['framework']:
                        break
                
                # Technology detection
                technologies = [
                    'jquery', 'bootstrap', 'font-awesome', 'google-analytics',
                    'cloudflare', 'aws', 'azure', 'heroku', 'nginx', 'apache',
                    'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'
                ]
                
                for tech in technologies:
                    if tech in content:
                        system_info['technologies'].append(tech)
                
        except Exception as e:
            logger.debug(f"Error mining system info: {e}")
        
        return system_info
    
    def mine_vulnerabilities(self, target_url: str) -> List[Dict]:
        """Mine potential vulnerabilities stealthily"""
        print(f"🔓 Mining vulnerabilities from {target_url}")
        
        vulnerabilities = []
        
        # Common vulnerability patterns
        vuln_patterns = [
            # SQL Injection
            (r'sql.*error|mysql.*error|oracle.*error', 'SQL Injection'),
            # XSS
            (r'<script[^>]*>.*</script>', 'XSS'),
            # Directory Traversal
            (r'\.\./|\.\.\\', 'Directory Traversal'),
            # Information Disclosure
            (r'stack trace|error.*line|debug.*info', 'Information Disclosure'),
            # Default Credentials
            (r'admin.*admin|root.*root|guest.*guest', 'Default Credentials'),
            # Exposed Files
            (r'\.git|\.svn|\.env|\.htaccess', 'Exposed Files'),
            # CORS Issues
            (r'access-control-allow-origin.*\*', 'CORS Misconfiguration')
        ]
        
        try:
            # Add stealth delay
            self._stealth_delay()
            
            # Make request
            response = self.session.get(target_url, timeout=10)
            
            if not self._is_detected(response):
                content = response.text
                
                # Check for vulnerability patterns
                for pattern, vuln_type in vuln_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        vulnerabilities.append({
                            'type': vuln_type,
                            'pattern': pattern,
                            'matches': matches[:5],  # Limit matches
                            'url': target_url,
                            'discovered_at': datetime.now().isoformat()
                        })
                
                # Check response headers for security issues
                security_headers = {
                    'X-Frame-Options': 'Clickjacking Protection',
                    'X-Content-Type-Options': 'MIME Sniffing Protection',
                    'X-XSS-Protection': 'XSS Protection',
                    'Strict-Transport-Security': 'HSTS',
                    'Content-Security-Policy': 'CSP'
                }
                
                for header, description in security_headers.items():
                    if header not in response.headers:
                        vulnerabilities.append({
                            'type': f'Missing {description}',
                            'header': header,
                            'url': target_url,
                            'discovered_at': datetime.now().isoformat()
                        })
                
        except Exception as e:
            logger.debug(f"Error mining vulnerabilities: {e}")
        
        return vulnerabilities
    
    def comprehensive_mining(self, target_url: str) -> Dict:
        """Perform comprehensive data mining"""
        print(f"🚀 Starting comprehensive data mining on {target_url}")
        
        mining_results = {
            'target_url': target_url,
            'timestamp': datetime.now().isoformat(),
            'api_endpoints': [],
            'database_info': {},
            'user_data': [],
            'system_info': {},
            'vulnerabilities': [],
            'summary': {}
        }
        
        try:
            # Mine API endpoints
            mining_results['api_endpoints'] = self.mine_api_endpoints(target_url)
            
            # Mine database information
            mining_results['database_info'] = self.mine_database_info(target_url)
            
            # Mine user data
            mining_results['user_data'] = self.mine_user_data(target_url)
            
            # Mine system information
            mining_results['system_info'] = self.mine_system_info(target_url)
            
            # Mine vulnerabilities
            mining_results['vulnerabilities'] = self.mine_vulnerabilities(target_url)
            
            # Generate summary
            mining_results['summary'] = {
                'total_endpoints': len(mining_results['api_endpoints']),
                'total_users': len(mining_results['user_data']),
                'total_vulnerabilities': len(mining_results['vulnerabilities']),
                'database_detected': mining_results['database_info']['database_type'] is not None,
                'framework_detected': mining_results['system_info']['framework'] is not None
            }
            
            print(f"✅ Comprehensive mining completed!")
            print(f"📊 Found: {mining_results['summary']['total_endpoints']} endpoints, "
                  f"{mining_results['summary']['total_users']} users, "
                  f"{mining_results['summary']['total_vulnerabilities']} vulnerabilities")
            
        except Exception as e:
            logger.error(f"Error in comprehensive mining: {e}")
        
        return mining_results
    
    def save_mining_results(self, results: Dict, filename: str = None):
        """Save mining results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mining_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Mining results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def get_mining_statistics(self) -> Dict:
        """Get mining statistics"""
        return {
            'total_requests': len(self.mined_data),
            'detected_patterns': len(self.detected_patterns),
            'successful_mining_sessions': len([d for d in self.mined_data if d.get('success', False)]),
            'average_response_time': sum([d.get('response_time', 0) for d in self.mined_data]) / len(self.mined_data) if self.mined_data else 0
        } 