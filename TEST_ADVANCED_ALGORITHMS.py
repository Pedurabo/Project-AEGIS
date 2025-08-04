#!/usr/bin/env python3
"""
TEST ADVANCED ALGORITHMS
Testing advanced algorithms for data analysis
"""

import json
from datetime import datetime
from silos.developmental.advanced_algorithms import AdvancedAlgorithms

def test_advanced_algorithms():
    """Test advanced algorithms"""
    print("🧮 TESTING ADVANCED ALGORITHMS")
    print("=" * 60)
    
    # Initialize algorithms engine
    algorithms = AdvancedAlgorithms()
    
    # Sample banking data
    sample_data = {
        "accounts": [
            {"account_number": "1000000001", "balance": 25000, "transactions": [1, 2, 3], "created_date": "2023-01-15"},
            {"account_number": "1000000002", "balance": 15000, "transactions": [1], "created_date": "2023-02-20"},
            {"account_number": "1000000003", "balance": 75000, "transactions": [1, 2, 3, 4, 5], "created_date": "2023-03-10"},
            {"account_number": "1000000004", "balance": 45000, "transactions": [1, 2], "created_date": "2023-04-05"},
            {"account_number": "1000000005", "balance": 32000, "transactions": [1, 2, 3, 4], "created_date": "2023-05-12"}
        ],
        "transactions": [
            {"from_account": "1000000001", "to_account": "1000000002", "amount": 1000},
            {"from_account": "1000000002", "to_account": "1000000003", "amount": 500},
            {"from_account": "1000000003", "to_account": "1000000001", "amount": 2000},
            {"from_account": "1000000004", "to_account": "1000000005", "amount": 1500},
            {"from_account": "1000000005", "to_account": "1000000001", "amount": 800}
        ]
    }
    
    # Test 1: Greedy Algorithm
    print("\n🎯 TEST 1: Greedy Algorithm")
    print("-" * 40)
    result = algorithms.run_algorithm("greedy", sample_data, target="balance")
    print(f"📊 Selected accounts: {result.get('selection_count', 0)}")
    print(f"💰 Total value: ${result.get('total_value', 0):,}")
    print(f"📈 Optimization ratio: {result.get('optimization_ratio', 0):.2%}")
    
    # Test 2: Depth First Search
    print("\n🔍 TEST 2: Depth First Search")
    print("-" * 40)
    result = algorithms.run_algorithm("dfs", sample_data, start_account="1000000001")
    print(f"📋 Visited accounts: {result.get('total_connections', 0)}")
    print(f"🛤️ Path length: {result.get('max_depth', 0)}")
    print(f"🔗 Connected accounts: {len(result.get('connected_accounts', []))}")
    
    # Test 3: Breadth First Search
    print("\n🌐 TEST 3: Breadth First Search")
    print("-" * 40)
    result = algorithms.run_algorithm("bfs", sample_data, start_account="1000000001", max_depth=2)
    print(f"📋 Accounts found: {result.get('total_accounts_found', 0)}")
    print(f"🌐 Network coverage: {result.get('network_coverage', 0):.2%}")
    print(f"📊 Levels explored: {len(result.get('levels', {}))}")
    
    # Test 4: Dijkstra's Algorithm
    print("\n🛣️ TEST 4: Dijkstra's Algorithm")
    print("-" * 40)
    result = algorithms.run_algorithm("dijkstra", sample_data, start_account="1000000001", end_account="1000000003")
    print(f"🛤️ Shortest path: {result.get('path_length', 0)} steps")
    print(f"💰 Total distance: {result.get('total_distance', 0)}")
    print(f"📍 Path: {' -> '.join(result.get('shortest_path', []))}")
    
    # Test 5: A* Algorithm
    print("\n⭐ TEST 5: A* Algorithm")
    print("-" * 40)
    result = algorithms.run_algorithm("a_star", sample_data, start_account="1000000001", end_account="1000000003")
    if 'error' not in result:
        print(f"🛤️ Optimal path: {result.get('path_length', 0)} steps")
        print(f"💰 Path cost: {result.get('path_cost', 0)}")
        print(f"📍 Path: {' -> '.join(result.get('optimal_path', []))}")
    else:
        print(f"❌ A* error: {result.get('error', 'Unknown error')}")
    
    # Test 6: K-means Clustering
    print("\n🎯 TEST 6: K-means Clustering")
    print("-" * 40)
    result = algorithms.run_algorithm("kmeans", sample_data, k=3)
    print(f"📊 Clusters created: {result.get('k', 0)}")
    print(f"📋 Total accounts: {result.get('total_accounts', 0)}")
    print(f"🔄 Iterations: {result.get('iterations', 0)}")
    
    # Show cluster details
    clusters = result.get('clusters', {})
    for cluster_name, cluster_data in clusters.items():
        print(f"  📊 {cluster_name}: {cluster_data.get('size', 0)} accounts, "
              f"Avg balance: ${cluster_data.get('avg_balance', 0):,.2f}")
    
    # Test 7: Genetic Algorithm
    print("\n🧬 TEST 7: Genetic Algorithm")
    print("-" * 40)
    result = algorithms.run_algorithm("genetic", sample_data, population_size=20, generations=50)
    print(f"🧬 Population size: {result.get('population_size', 0)}")
    print(f"🔄 Generations: {result.get('generations', 0)}")
    print(f"🏆 Best fitness: {result.get('best_fitness', 0):.2f}")
    print(f"📊 Selected accounts: {result.get('selection_count', 0)}")
    print(f"💰 Total balance: ${result.get('total_balance', 0):,}")
    
    # System status
    print("\n📊 ALGORITHM SYSTEM STATUS")
    print("-" * 40)
    status = algorithms.get_system_status()
    print(f"🧮 Available algorithms: {status['available_algorithms']}")
    print(f"📋 Algorithm list: {status['algorithm_list']}")
    
    print("\n✅ Advanced Algorithms Testing Completed!")

if __name__ == "__main__":
    test_advanced_algorithms() 