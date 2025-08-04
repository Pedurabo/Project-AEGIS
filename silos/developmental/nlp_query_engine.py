#!/usr/bin/env python3
"""
NLP QUERY ENGINE
Team 1: AI Research Core - Natural Language Processing Engine
"""

import re
import json
import sqlite3
from datetime import datetime
import pandas as pd
from typing import Dict, List, Any, Optional

class NLPQueryEngine:
    def __init__(self):
        self.name = "NLP Query Engine"
        self.version = "1.0.0"
        self.knowledge_base = self.initialize_knowledge_base()
        self.query_patterns = self.initialize_query_patterns()
        self.database_connection = None
        
        # Initialize banking database
        self.initialize_banking_database()
    
    def initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize expert knowledge base"""
        return {
            "banking_terms": {
                "account": ["account", "bank account", "savings", "checking", "deposit"],
                "balance": ["balance", "money", "funds", "amount", "total"],
                "transaction": ["transaction", "transfer", "payment", "withdrawal", "deposit"],
                "customer": ["customer", "account holder", "user", "client", "person"],
                "bank": ["bank", "financial institution", "branch", "atm"],
                "location": ["location", "address", "city", "state", "country", "branch"]
            },
            "query_types": {
                "retrieve": ["show", "get", "find", "display", "retrieve", "access"],
                "modify": ["change", "update", "modify", "edit", "alter"],
                "analyze": ["analyze", "examine", "study", "investigate", "check"],
                "monitor": ["monitor", "track", "watch", "observe", "follow"]
            },
            "banking_entities": {
                "chase": ["chase", "jp morgan", "chase bank"],
                "bank_of_america": ["bank of america", "boa", "bofa"],
                "wells_fargo": ["wells fargo", "wells", "wf"],
                "citibank": ["citibank", "citi", "citigroup"]
            }
        }
    
    def initialize_query_patterns(self) -> Dict[str, str]:
        """Initialize query pattern matching"""
        return {
            "account_info": r"(show|get|find|display).*?(account|balance|info).*?(\d+)",
            "customer_data": r"(show|get|find|display).*?(customer|person|holder).*?(\w+)",
            "transaction_history": r"(show|get|find|display).*?(transaction|history|activity).*?(\d+)",
            "location_data": r"(show|get|find|display).*?(location|address|branch).*?(\w+)",
            "balance_modification": r"(change|modify|update).*?(balance|amount).*?(\d+).*?(\d+)",
            "account_creation": r"(create|add|new).*?(account).*?(\w+)",
            "security_check": r"(check|verify|validate).*?(security|access|permission).*?(\w+)"
        }
    
    def initialize_banking_database(self):
        """Initialize banking database with sample data"""
        try:
            self.database_connection = sqlite3.connect(':memory:')
            cursor = self.database_connection.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE accounts (
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
                CREATE TABLE transactions (
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
                CREATE TABLE customers (
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
            
            cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_accounts)
            cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)", sample_transactions)
            cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample_customers)
            
            self.database_connection.commit()
            print(f"✅ {self.name}: Banking database initialized with sample data")
            
        except Exception as e:
            print(f"❌ {self.name}: Database initialization error: {e}")
    
    def process_natural_language_query(self, query: str) -> Dict[str, Any]:
        """Process natural language query and return structured response"""
        query_lower = query.lower()
        
        # Analyze query intent
        intent = self.analyze_query_intent(query_lower)
        
        # Extract entities
        entities = self.extract_entities(query_lower)
        
        # Generate SQL query
        sql_query = self.generate_sql_query(intent, entities)
        
        # Execute query
        results = self.execute_query(sql_query)
        
        # Format response
        response = self.format_response(intent, results, query)
        
        return {
            "original_query": query,
            "intent": intent,
            "entities": entities,
            "sql_query": sql_query,
            "results": results,
            "formatted_response": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_query_intent(self, query: str) -> str:
        """Analyze the intent of the query"""
        if any(word in query for word in self.knowledge_base["query_types"]["retrieve"]):
            if any(word in query for word in ["account", "balance", "info"]):
                return "retrieve_account_info"
            elif any(word in query for word in ["customer", "person", "holder"]):
                return "retrieve_customer_data"
            elif any(word in query for word in ["transaction", "history", "activity"]):
                return "retrieve_transaction_history"
            elif any(word in query for word in ["location", "address", "branch"]):
                return "retrieve_location_data"
        elif any(word in query for word in self.knowledge_base["query_types"]["modify"]):
            return "modify_data"
        elif any(word in query for word in self.knowledge_base["query_types"]["analyze"]):
            return "analyze_data"
        elif any(word in query for word in self.knowledge_base["query_types"]["monitor"]):
            return "monitor_data"
        
        return "general_query"
    
    def extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities from the query"""
        entities = {
            "account_number": None,
            "customer_name": None,
            "bank_name": None,
            "location": None,
            "amount": None,
            "transaction_type": None
        }
        
        # Extract account number
        account_match = re.search(r'\b(\d{10})\b', query)
        if account_match:
            entities["account_number"] = account_match.group(1)
        
        # Extract customer name
        name_match = re.search(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b', query)
        if name_match:
            entities["customer_name"] = name_match.group(1)
        
        # Extract bank name
        for bank, aliases in self.knowledge_base["banking_entities"].items():
            if any(alias in query for alias in aliases):
                entities["bank_name"] = bank
                break
        
        # Extract amount
        amount_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', query)
        if amount_match:
            entities["amount"] = float(amount_match.group(1).replace(',', ''))
        
        # Extract transaction type
        transaction_types = ["deposit", "withdrawal", "transfer", "payment"]
        for trans_type in transaction_types:
            if trans_type in query:
                entities["transaction_type"] = trans_type
                break
        
        return entities
    
    def generate_sql_query(self, intent: str, entities: Dict[str, Any]) -> str:
        """Generate SQL query based on intent and entities"""
        if intent == "retrieve_account_info":
            if entities["account_number"]:
                return f"""
                SELECT * FROM accounts 
                WHERE account_number = '{entities['account_number']}'
                """
            elif entities["customer_name"]:
                return f"""
                SELECT * FROM accounts 
                WHERE customer_name LIKE '%{entities['customer_name']}%'
                """
            else:
                return "SELECT * FROM accounts LIMIT 10"
        
        elif intent == "retrieve_customer_data":
            if entities["customer_name"]:
                return f"""
                SELECT * FROM customers 
                WHERE customer_name LIKE '%{entities['customer_name']}%'
                """
            else:
                return "SELECT * FROM customers LIMIT 10"
        
        elif intent == "retrieve_transaction_history":
            if entities["account_number"]:
                return f"""
                SELECT * FROM transactions 
                WHERE account_number = '{entities['account_number']}'
                ORDER BY timestamp DESC
                """
            else:
                return "SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 10"
        
        elif intent == "retrieve_location_data":
            return "SELECT DISTINCT location, bank_name FROM accounts"
        
        elif intent == "analyze_data":
            return """
            SELECT 
                bank_name,
                COUNT(*) as account_count,
                AVG(balance) as avg_balance,
                SUM(balance) as total_balance
            FROM accounts 
            GROUP BY bank_name
            """
        
        else:
            return "SELECT * FROM accounts LIMIT 5"
    
    def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        try:
            cursor = self.database_connection.cursor()
            cursor.execute(sql_query)
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Fetch results
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            return results
            
        except Exception as e:
            print(f"❌ {self.name}: Query execution error: {e}")
            return []
    
    def format_response(self, intent: str, results: List[Dict[str, Any]], original_query: str) -> str:
        """Format response based on intent and results"""
        if not results:
            return f"No data found for query: '{original_query}'"
        
        if intent == "retrieve_account_info":
            response = "🏦 **ACCOUNT INFORMATION**\n\n"
            for result in results:
                response += f"**Account Number:** {result.get('account_number', 'N/A')}\n"
                response += f"**Customer:** {result.get('customer_name', 'N/A')}\n"
                response += f"**Type:** {result.get('account_type', 'N/A')}\n"
                response += f"**Balance:** ${result.get('balance', 0):,.2f}\n"
                response += f"**Bank:** {result.get('bank_name', 'N/A')}\n"
                response += f"**Location:** {result.get('location', 'N/A')}\n"
                response += f"**Status:** {result.get('status', 'N/A')}\n"
                response += "─" * 40 + "\n"
        
        elif intent == "retrieve_customer_data":
            response = "👤 **CUSTOMER INFORMATION**\n\n"
            for result in results:
                response += f"**Name:** {result.get('customer_name', 'N/A')}\n"
                response += f"**SSN:** {result.get('ssn', 'N/A')}\n"
                response += f"**Address:** {result.get('address', 'N/A')}\n"
                response += f"**Phone:** {result.get('phone', 'N/A')}\n"
                response += f"**Email:** {result.get('email', 'N/A')}\n"
                response += f"**Bank:** {result.get('bank_name', 'N/A')}\n"
                response += f"**Accounts:** {result.get('account_count', 0)}\n"
                response += "─" * 40 + "\n"
        
        elif intent == "retrieve_transaction_history":
            response = "📊 **TRANSACTION HISTORY**\n\n"
            for result in results:
                response += f"**Transaction ID:** {result.get('transaction_id', 'N/A')}\n"
                response += f"**Account:** {result.get('account_number', 'N/A')}\n"
                response += f"**Type:** {result.get('transaction_type', 'N/A')}\n"
                response += f"**Amount:** ${result.get('amount', 0):,.2f}\n"
                response += f"**Description:** {result.get('description', 'N/A')}\n"
                response += f"**Timestamp:** {result.get('timestamp', 'N/A')}\n"
                response += f"**Status:** {result.get('status', 'N/A')}\n"
                response += "─" * 40 + "\n"
        
        elif intent == "analyze_data":
            response = "📈 **BANKING ANALYSIS**\n\n"
            for result in results:
                response += f"**Bank:** {result.get('bank_name', 'N/A')}\n"
                response += f"**Accounts:** {result.get('account_count', 0)}\n"
                response += f"**Average Balance:** ${result.get('avg_balance', 0):,.2f}\n"
                response += f"**Total Balance:** ${result.get('total_balance', 0):,.2f}\n"
                response += "─" * 40 + "\n"
        
        else:
            response = "📋 **GENERAL RESULTS**\n\n"
            for result in results:
                for key, value in result.items():
                    response += f"**{key.title()}:** {value}\n"
                response += "─" * 40 + "\n"
        
        return response
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "name": self.name,
            "version": self.version,
            "status": "Active",
            "database_connected": self.database_connection is not None,
            "knowledge_base_size": len(self.knowledge_base),
            "query_patterns_count": len(self.query_patterns),
            "timestamp": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    nlp_engine = NLPQueryEngine()
    
    # Test queries
    test_queries = [
        "Show me account information for 1000000001",
        "Get customer data for John Smith",
        "Display transaction history for account 1000000001",
        "Analyze banking data by bank",
        "Find all accounts at Chase Bank"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result = nlp_engine.process_natural_language_query(query)
        print(f"📊 Response:\n{result['formatted_response']}")
        print("─" * 60) 