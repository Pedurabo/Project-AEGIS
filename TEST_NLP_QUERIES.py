#!/usr/bin/env python3
"""
TEST NLP QUERIES
Testing natural language query processing
"""

import json
from datetime import datetime
from silos.developmental.nlp_query_engine import NLPQueryEngine

def test_nlp_queries():
    """Test NLP query processing"""
    print("🤖 TESTING NATURAL LANGUAGE QUERIES")
    print("=" * 60)
    
    # Initialize NLP engine
    nlp_engine = NLPQueryEngine()
    
    # Test queries
    test_queries = [
        "Show me account information for 1000000001",
        "Get customer data for John Smith",
        "Display transaction history for account 1000000001",
        "Analyze banking data by bank",
        "Find all accounts at Chase Bank",
        "Show me the balance for account 1000000002",
        "What transactions happened on account 1000000003",
        "Get customer information for Sarah Johnson"
    ]
    
    print(f"🧪 Testing {len(test_queries)} natural language queries...")
    print()
    
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 TEST {i}: {query}")
        print("-" * 50)
        
        try:
            # Process query
            result = nlp_engine.process_natural_language_query(query)
            
            # Display results
            print(f"🎯 Intent: {result['intent']}")
            print(f"📋 Entities: {result['entities']}")
            print(f"🗄️ SQL Query: {result['sql_query']}")
            print(f"📊 Results found: {len(result['results'])}")
            
            # Show formatted response
            print(f"📝 Response:")
            print(result['formatted_response'])
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print()
    
    # Test system status
    print("📊 NLP SYSTEM STATUS")
    print("-" * 40)
    status = nlp_engine.get_system_status()
    print(f"🤖 Name: {status['name']}")
    print(f"📦 Version: {status['version']}")
    print(f"🟢 Status: {status['status']}")
    print(f"🗄️ Database connected: {status['database_connected']}")
    print(f"📚 Knowledge base size: {status['knowledge_base_size']}")
    print(f"🔍 Query patterns: {status['query_patterns_count']}")
    
    print("\n✅ NLP Query Testing Completed!")

if __name__ == "__main__":
    test_nlp_queries() 