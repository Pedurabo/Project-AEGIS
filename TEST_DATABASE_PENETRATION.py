#!/usr/bin/env python3
"""
TEST DATABASE PENETRATION
Testing database penetration capabilities
"""

import json
from datetime import datetime
from silos.security.database_penetration_fixed import DatabasePenetration

def test_database_penetration():
    """Test database penetration capabilities"""
    print("🛡️ TESTING DATABASE PENETRATION")
    print("=" * 60)
    
    # Initialize penetration engine
    penetration = DatabasePenetration()
    
    # Test 1: SQLite Penetration
    print("\n🗄️ TEST 1: SQLite Database Penetration")
    print("-" * 40)
    
    sqlite_config = {
        "type": "sqlite",
        "path": ":memory:"
    }
    
    # Scan vulnerabilities
    print("🔍 Scanning SQLite vulnerabilities...")
    vulnerabilities = penetration.scan_database_vulnerabilities(sqlite_config)
    print(f"📊 Vulnerabilities found: {vulnerabilities['vulnerabilities_found']}")
    print(f"⚠️ Risk level: {vulnerabilities['risk_level']}")
    
    # Penetrate database
    print("\n🔥 Penetrating SQLite database...")
    result = penetration.penetrate_database(sqlite_config, "comprehensive")
    
    print(f"📋 Tables found: {len(result.get('tables_found', []))}")
    print(f"📊 Data extracted: {len(result.get('data_extracted', {}))}")
    print(f"🔧 Exploits attempted: {len(result.get('exploits_attempted', []))}")
    
    # Show sample data
    if 'data_extracted' in result:
        for table, data in result['data_extracted'].items():
            if isinstance(data, list) and len(data) > 0:
                print(f"📋 {table}: {len(data)} records")
                if len(data) > 0:
                    print(f"   Sample: {data[0]}")
    
    # Test 2: PostgreSQL (if available)
    if 'postgresql' in penetration.supported_databases:
        print("\n🗄️ TEST 2: PostgreSQL Database Penetration")
        print("-" * 40)
        
        postgresql_config = {
            "type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "password": "",
            "database": "postgres"
        }
        
        print("🔍 Scanning PostgreSQL vulnerabilities...")
        vulnerabilities = penetration.scan_database_vulnerabilities(postgresql_config)
        print(f"📊 Vulnerabilities found: {vulnerabilities['vulnerabilities_found']}")
        print(f"⚠️ Risk level: {vulnerabilities['risk_level']}")
        
        print("\n🔥 Attempting PostgreSQL penetration...")
        result = penetration.penetrate_database(postgresql_config, "comprehensive")
        
        if 'error' in result:
            print(f"❌ PostgreSQL error: {result['error']}")
        else:
            print(f"✅ PostgreSQL penetration successful")
            print(f"📋 Databases found: {len(result.get('databases_found', []))}")
            print(f"📊 Tables found: {len(result.get('tables_found', []))}")
    
    # Test 3: Redis (if available)
    if 'redis' in penetration.supported_databases:
        print("\n🗄️ TEST 3: Redis Database Penetration")
        print("-" * 40)
        
        redis_config = {
            "type": "redis",
            "host": "localhost",
            "port": 6379,
            "password": "",
            "database": 0
        }
        
        print("🔍 Scanning Redis vulnerabilities...")
        vulnerabilities = penetration.scan_database_vulnerabilities(redis_config)
        print(f"📊 Vulnerabilities found: {vulnerabilities['vulnerabilities_found']}")
        print(f"⚠️ Risk level: {vulnerabilities['risk_level']}")
        
        print("\n🔥 Attempting Redis penetration...")
        result = penetration.penetrate_database(redis_config, "comprehensive")
        
        if 'error' in result:
            print(f"❌ Redis error: {result['error']}")
        else:
            print(f"✅ Redis penetration successful")
            print(f"🔑 Keys found: {len(result.get('keys_found', []))}")
            print(f"📊 Data extracted: {len(result.get('data_extracted', {}))}")
    
    # System status
    print("\n📊 SYSTEM STATUS")
    print("-" * 40)
    status = penetration.get_system_status()
    print(f"🏗️ Supported databases: {status['supported_databases']}")
    print(f"📈 Database availability: {status['database_availability']}")
    print(f"🔗 Active connections: {status['active_connections']}")
    
    print("\n✅ Database Penetration Testing Completed!")

if __name__ == "__main__":
    test_database_penetration() 