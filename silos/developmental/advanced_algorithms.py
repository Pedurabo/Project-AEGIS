#!/usr/bin/env python3
"""
ADVANCED ALGORITHMS
Team 2: Data Science & Analytics - Advanced Algorithm Implementation
"""

import heapq
from collections import deque, defaultdict
from typing import List, Dict, Any, Tuple, Optional, Set
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AdvancedAlgorithms:
    def __init__(self):
        self.name = "Advanced Algorithms Engine"
        self.version = "1.0.0"
        self.algorithms = {
            "greedy": self.greedy_algorithm,
            "dfs": self.depth_first_search,
            "bfs": self.breadth_first_search,
            "dijkstra": self.dijkstra_algorithm,
            "a_star": self.a_star_algorithm,
            "kmeans": self.kmeans_clustering,
            "genetic": self.genetic_algorithm
        }
    
    def greedy_algorithm(self, data: Dict[str, Any], target: str = "balance") -> Dict[str, Any]:
        """
        Greedy algorithm for banking optimization
        Optimizes account selection based on balance, transaction frequency, etc.
        """
        print(f"🎯 Executing Greedy Algorithm for {target} optimization...")
        
        accounts = data.get("accounts", [])
        if not accounts:
            return {"error": "No accounts data provided"}
        
        # Sort accounts by target criteria (greedy approach)
        if target == "balance":
            sorted_accounts = sorted(accounts, key=lambda x: x.get("balance", 0), reverse=True)
        elif target == "transaction_frequency":
            sorted_accounts = sorted(accounts, key=lambda x: len(x.get("transactions", [])), reverse=True)
        elif target == "activity":
            sorted_accounts = sorted(accounts, key=lambda x: x.get("last_activity", ""), reverse=True)
        else:
            sorted_accounts = sorted(accounts, key=lambda x: x.get("balance", 0), reverse=True)
        
        # Select top accounts (greedy selection)
        selected_accounts = sorted_accounts[:min(5, len(sorted_accounts))]
        
        total_value = sum(acc.get("balance", 0) for acc in selected_accounts)
        
        return {
            "algorithm": "Greedy",
            "target": target,
            "selected_accounts": selected_accounts,
            "total_value": total_value,
            "selection_count": len(selected_accounts),
            "optimization_ratio": total_value / sum(acc.get("balance", 0) for acc in accounts) if accounts else 0,
            "execution_time": datetime.now().isoformat()
        }
    
    def depth_first_search(self, data: Dict[str, Any], start_account: str) -> Dict[str, Any]:
        """
        Depth First Search for account relationship analysis
        Finds connected accounts and transaction paths
        """
        print(f"🔍 Executing Depth First Search from account {start_account}...")
        
        accounts = data.get("accounts", [])
        transactions = data.get("transactions", [])
        
        # Build adjacency list
        graph = defaultdict(list)
        for trans in transactions:
            from_acc = trans.get("from_account")
            to_acc = trans.get("to_account")
            if from_acc and to_acc:
                graph[from_acc].append(to_acc)
        
        # DFS implementation
        visited = set()
        path = []
        connected_accounts = []
        
        def dfs(account):
            if account in visited:
                return
            
            visited.add(account)
            path.append(account)
            connected_accounts.append(account)
            
            # Find account details
            account_info = next((acc for acc in accounts if acc.get("account_number") == account), None)
            if account_info:
                connected_accounts[-1] = account_info
            
            # Explore neighbors
            for neighbor in graph[account]:
                dfs(neighbor)
        
        # Start DFS
        dfs(start_account)
        
        return {
            "algorithm": "Depth First Search",
            "start_account": start_account,
            "visited_accounts": list(visited),
            "path": path,
            "connected_accounts": connected_accounts,
            "total_connections": len(visited),
            "max_depth": len(path),
            "execution_time": datetime.now().isoformat()
        }
    
    def breadth_first_search(self, data: Dict[str, Any], start_account: str, max_depth: int = 3) -> Dict[str, Any]:
        """
        Breadth First Search for account network analysis
        Finds accounts within specified distance
        """
        print(f"🌐 Executing Breadth First Search from account {start_account}...")
        
        accounts = data.get("accounts", [])
        transactions = data.get("transactions", [])
        
        # Build adjacency list
        graph = defaultdict(list)
        for trans in transactions:
            from_acc = trans.get("from_account")
            to_acc = trans.get("to_account")
            if from_acc and to_acc:
                graph[from_acc].append(to_acc)
        
        # BFS implementation
        visited = set()
        queue = deque([(start_account, 0)])  # (account, depth)
        levels = defaultdict(list)
        
        while queue:
            current_account, depth = queue.popleft()
            
            if current_account in visited or depth > max_depth:
                continue
            
            visited.add(current_account)
            levels[depth].append(current_account)
            
            # Add neighbors to queue
            for neighbor in graph[current_account]:
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        
        # Get account details for each level
        detailed_levels = {}
        for depth, account_list in levels.items():
            detailed_levels[depth] = []
            for acc_num in account_list:
                account_info = next((acc for acc in accounts if acc.get("account_number") == acc_num), None)
                if account_info:
                    detailed_levels[depth].append(account_info)
        
        return {
            "algorithm": "Breadth First Search",
            "start_account": start_account,
            "max_depth": max_depth,
            "levels": detailed_levels,
            "total_accounts_found": len(visited),
            "network_coverage": len(visited) / len(accounts) if accounts else 0,
            "execution_time": datetime.now().isoformat()
        }
    
    def dijkstra_algorithm(self, data: Dict[str, Any], start_account: str, end_account: str) -> Dict[str, Any]:
        """
        Dijkstra's algorithm for finding shortest transaction path
        """
        print(f"🛣️ Executing Dijkstra's Algorithm from {start_account} to {end_account}...")
        
        transactions = data.get("transactions", [])
        
        # Build weighted graph
        graph = defaultdict(list)
        for trans in transactions:
            from_acc = trans.get("from_account")
            to_acc = trans.get("to_account")
            amount = abs(trans.get("amount", 1))
            if from_acc and to_acc:
                graph[from_acc].append((to_acc, amount))
        
        # Dijkstra implementation
        distances = defaultdict(lambda: float('inf'))
        distances[start_account] = 0
        previous = {}
        pq = [(0, start_account)]
        
        while pq:
            current_distance, current_account = heapq.heappop(pq)
            
            if current_distance > distances[current_account]:
                continue
            
            if current_account == end_account:
                break
            
            for neighbor, weight in graph[current_account]:
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_account
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end_account
        while current in previous:
            path.append(current)
            current = previous[current]
        path.append(start_account)
        path.reverse()
        
        return {
            "algorithm": "Dijkstra",
            "start_account": start_account,
            "end_account": end_account,
            "shortest_path": path,
            "total_distance": distances[end_account] if distances[end_account] != float('inf') else None,
            "path_length": len(path),
            "execution_time": datetime.now().isoformat()
        }
    
    def a_star_algorithm(self, data: Dict[str, Any], start_account: str, end_account: str) -> Dict[str, Any]:
        """
        A* algorithm for intelligent pathfinding in banking networks
        """
        print(f"⭐ Executing A* Algorithm from {start_account} to {end_account}...")
        
        accounts = data.get("accounts", [])
        transactions = data.get("transactions", [])
        
        # Build graph with heuristic
        graph = defaultdict(list)
        account_locations = {}
        
        for acc in accounts:
            account_locations[acc.get("account_number")] = acc.get("location", "")
        
        for trans in transactions:
            from_acc = trans.get("from_account")
            to_acc = trans.get("to_account")
            amount = abs(trans.get("amount", 1))
            if from_acc and to_acc:
                graph[from_acc].append((to_acc, amount))
        
        # Heuristic function (simplified - could be based on location, bank, etc.)
        def heuristic(account1, account2):
            # Simple heuristic based on account number difference
            try:
                num1 = int(account1)
                num2 = int(account2)
                return abs(num1 - num2) / 1000000
            except:
                return 1
        
        # A* implementation
        open_set = [(0, start_account)]
        came_from = {}
        g_score = defaultdict(lambda: float('inf'))
        g_score[start_account] = 0
        f_score = defaultdict(lambda: float('inf'))
        f_score[start_account] = heuristic(start_account, end_account)
        
        while open_set:
            current_f, current_account = heapq.heappop(open_set)
            
            if current_account == end_account:
                # Reconstruct path
                path = []
                while current_account in came_from:
                    path.append(current_account)
                    current_account = came_from[current_account]
                path.append(start_account)
                path.reverse()
                
                return {
                    "algorithm": "A*",
                    "start_account": start_account,
                    "end_account": end_account,
                    "optimal_path": path,
                    "path_cost": g_score[end_account],
                    "path_length": len(path),
                    "execution_time": datetime.now().isoformat()
                }
            
            for neighbor, weight in graph[current_account]:
                tentative_g = g_score[current_account] + weight
                
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current_account
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end_account)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return {
            "algorithm": "A*",
            "start_account": start_account,
            "end_account": end_account,
            "error": "No path found",
            "execution_time": datetime.now().isoformat()
        }
    
    def kmeans_clustering(self, data: Dict[str, Any], k: int = 3) -> Dict[str, Any]:
        """
        K-means clustering for customer segmentation
        """
        print(f"🎯 Executing K-means Clustering with {k} clusters...")
        
        accounts = data.get("accounts", [])
        if not accounts:
            return {"error": "No accounts data provided"}
        
        # Extract features for clustering
        features = []
        account_ids = []
        
        for acc in accounts:
            balance = acc.get("balance", 0)
            transaction_count = len(acc.get("transactions", []))
            account_age = (datetime.now() - datetime.strptime(acc.get("created_date", "2023-01-01"), "%Y-%m-%d")).days
            
            features.append([balance, transaction_count, account_age])
            account_ids.append(acc.get("account_number"))
        
        if len(features) < k:
            return {"error": f"Not enough data for {k} clusters"}
        
        # Convert to numpy array
        X = np.array(features)
        
        # Simple K-means implementation
        # Initialize centroids randomly
        centroids = X[np.random.choice(len(X), k, replace=False)]
        
        for iteration in range(100):
            # Assign points to nearest centroid
            distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
            labels = np.argmin(distances, axis=0)
            
            # Update centroids
            new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
            
            # Check convergence
            if np.all(centroids == new_centroids):
                break
            
            centroids = new_centroids
        
        # Organize results
        clusters = {}
        for i in range(k):
            cluster_accounts = [account_ids[j] for j in range(len(labels)) if labels[j] == i]
            clusters[f"cluster_{i+1}"] = {
                "centroid": centroids[i].tolist(),
                "accounts": cluster_accounts,
                "size": len(cluster_accounts),
                "avg_balance": np.mean([acc.get("balance", 0) for acc in accounts if acc.get("account_number") in cluster_accounts])
            }
        
        return {
            "algorithm": "K-means Clustering",
            "k": k,
            "clusters": clusters,
            "total_accounts": len(accounts),
            "iterations": iteration + 1,
            "execution_time": datetime.now().isoformat()
        }
    
    def genetic_algorithm(self, data: Dict[str, Any], population_size: int = 50, generations: int = 100) -> Dict[str, Any]:
        """
        Genetic algorithm for portfolio optimization
        """
        print(f"🧬 Executing Genetic Algorithm with population {population_size}, generations {generations}...")
        
        accounts = data.get("accounts", [])
        if not accounts:
            return {"error": "No accounts data provided"}
        
        # Fitness function - maximize return while minimizing risk
        def fitness_function(individual):
            total_balance = 0
            total_risk = 0
            
            for i, selected in enumerate(individual):
                if selected and i < len(accounts):
                    balance = accounts[i].get("balance", 0)
                    transactions = accounts[i].get("transactions", [])
                    risk = len(transactions) * 0.1  # Simple risk metric
                    
                    total_balance += balance
                    total_risk += risk
            
            if total_risk == 0:
                return 0
            
            return total_balance / total_risk
        
        # Initialize population
        population = []
        for _ in range(population_size):
            individual = [np.random.choice([0, 1]) for _ in range(len(accounts))]
            population.append(individual)
        
        best_fitness = 0
        best_individual = None
        
        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = [fitness_function(ind) for ind in population]
            
            # Find best individual
            max_fitness_idx = np.argmax(fitness_scores)
            if fitness_scores[max_fitness_idx] > best_fitness:
                best_fitness = fitness_scores[max_fitness_idx]
                best_individual = population[max_fitness_idx].copy()
            
            # Selection (tournament selection)
            new_population = []
            for _ in range(population_size):
                tournament = np.random.choice(len(population), 3, replace=False)
                winner = tournament[np.argmax([fitness_scores[i] for i in tournament])]
                new_population.append(population[winner].copy())
            
            # Crossover and mutation
            for i in range(0, population_size, 2):
                if i + 1 < population_size:
                    # Crossover
                    crossover_point = np.random.randint(1, len(accounts))
                    new_population[i][crossover_point:], new_population[i+1][crossover_point:] = \
                        new_population[i+1][crossover_point:], new_population[i][crossover_point:]
                    
                    # Mutation
                    for j in range(len(accounts)):
                        if np.random.random() < 0.01:  # 1% mutation rate
                            new_population[i][j] = 1 - new_population[i][j]
                        if np.random.random() < 0.01:
                            new_population[i+1][j] = 1 - new_population[i+1][j]
            
            population = new_population
        
        # Get selected accounts
        selected_accounts = []
        if best_individual:
            for i, selected in enumerate(best_individual):
                if selected and i < len(accounts):
                    selected_accounts.append(accounts[i])
        
        return {
            "algorithm": "Genetic Algorithm",
            "population_size": population_size,
            "generations": generations,
            "best_fitness": best_fitness,
            "selected_accounts": selected_accounts,
            "selection_count": len(selected_accounts),
            "total_balance": sum(acc.get("balance", 0) for acc in selected_accounts),
            "execution_time": datetime.now().isoformat()
        }
    
    def run_algorithm(self, algorithm_name: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Run specified algorithm with data"""
        if algorithm_name not in self.algorithms:
            return {"error": f"Algorithm '{algorithm_name}' not found"}
        
        try:
            return self.algorithms[algorithm_name](data, **kwargs)
        except Exception as e:
            return {"error": f"Algorithm execution failed: {str(e)}"}
    
    def get_available_algorithms(self) -> List[str]:
        """Get list of available algorithms"""
        return list(self.algorithms.keys())
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "name": self.name,
            "version": self.version,
            "status": "Active",
            "available_algorithms": len(self.algorithms),
            "algorithm_list": list(self.algorithms.keys()),
            "timestamp": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    algorithms = AdvancedAlgorithms()
    
    # Sample data
    sample_data = {
        "accounts": [
            {"account_number": "1000000001", "balance": 25000, "transactions": [1, 2, 3], "created_date": "2023-01-15"},
            {"account_number": "1000000002", "balance": 15000, "transactions": [1], "created_date": "2023-02-20"},
            {"account_number": "1000000003", "balance": 75000, "transactions": [1, 2, 3, 4, 5], "created_date": "2023-03-10"}
        ],
        "transactions": [
            {"from_account": "1000000001", "to_account": "1000000002", "amount": 1000},
            {"from_account": "1000000002", "to_account": "1000000003", "amount": 500},
            {"from_account": "1000000003", "to_account": "1000000001", "amount": 2000}
        ]
    }
    
    # Test algorithms
    print("🧪 Testing Advanced Algorithms...")
    
    # Greedy
    result = algorithms.run_algorithm("greedy", sample_data, target="balance")
    print(f"🎯 Greedy Result: {result}")
    
    # DFS
    result = algorithms.run_algorithm("dfs", sample_data, start_account="1000000001")
    print(f"🔍 DFS Result: {result}")
    
    # BFS
    result = algorithms.run_algorithm("bfs", sample_data, start_account="1000000001", max_depth=2)
    print(f"🌐 BFS Result: {result}")
    
    # K-means
    result = algorithms.run_algorithm("kmeans", sample_data, k=2)
    print(f"🎯 K-means Result: {result}")
    
    print("✅ Advanced Algorithms testing completed!") 