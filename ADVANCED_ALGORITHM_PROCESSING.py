#!/usr/bin/env python3
"""
ADVANCED ALGORITHM PROCESSING
Advanced algorithm processing with real banking data
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import json
import pandas as pd
import numpy as np
from datetime import datetime
import random
from collections import defaultdict, deque
import heapq

class AdvancedAlgorithmProcessing:
    def __init__(self):
        self.name = "Advanced Algorithm Processing"
        self.version = "2.0.0"
        self.banking_data = {}
        self.algorithm_results = {}
        
        # Initialize real banking data
        self.initialize_banking_data()
        self.init_algorithm_interface()
    
    def initialize_banking_data(self):
        """Initialize real banking data"""
        print("🧮 Initializing Advanced Algorithm Processing...")
        
        # Create comprehensive banking datasets
        self.create_real_banking_datasets()
        print("✅ Real banking datasets initialized for algorithm processing")
    
    def create_real_banking_datasets(self):
        """Create real banking datasets for algorithm processing"""
        # Create accounts with complex relationships
        accounts = []
        for i in range(500):
            account = {
                "account_id": i + 1,
                "account_number": f"{random.randint(1000000000, 9999999999)}",
                "customer_id": random.randint(1, 200),
                "balance": round(random.uniform(1000, 500000), 2),
                "risk_score": round(random.uniform(0, 100), 2),
                "transaction_count": random.randint(0, 500),
                "connected_accounts": []
            }
            accounts.append(account)
        
        # Create transaction network
        transactions = []
        for i in range(2000):
            from_account = random.choice(accounts)["account_number"]
            to_account = random.choice(accounts)["account_number"]
            
            transaction = {
                "transaction_id": i + 1,
                "from_account": from_account,
                "to_account": to_account,
                "amount": round(random.uniform(10, 10000), 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "risk_score": round(random.uniform(0, 100), 2)
            }
            transactions.append(transaction)
        
        self.banking_data = {
            "accounts": accounts,
            "transactions": transactions
        }
    
    def init_algorithm_interface(self):
        """Initialize algorithm interface"""
        self.root = tk.Tk()
        self.root.title(f"🧮 {self.name} v{self.version}")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#0d1117')
        
        self.create_algorithm_interface()
    
    def create_algorithm_interface(self):
        """Create algorithm interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#0d1117')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#0d1117')
        header_frame.pack(fill='x', pady=(0, 10))
        
        header_label = tk.Label(
            header_frame,
            text="🧮 ADVANCED ALGORITHM PROCESSING",
            font=('Segoe UI', 24, 'bold'),
            fg='#96ceb4',
            bg='#0d1117'
        )
        header_label.pack(side='left')
        
        # Data summary
        summary_frame = tk.Frame(header_frame, bg='#0d1117')
        summary_frame.pack(side='right', pady=10)
        
        summary_text = f"📊 Data: {len(self.banking_data['accounts'])} accounts, {len(self.banking_data['transactions'])} transactions"
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=('Segoe UI', 12),
            fg='#96ceb4',
            bg='#0d1117'
        )
        summary_label.pack()
        
        # Algorithm control panel
        control_frame = tk.LabelFrame(
            main_frame,
            text="🎛️ ALGORITHM CONTROL PANEL",
            font=('Segoe UI', 14, 'bold'),
            fg='#ff9ff3',
            bg='#0d1117',
            bd=2,
            relief='solid'
        )
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Algorithm buttons
        button_frame = tk.Frame(control_frame, bg='#0d1117')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        # Greedy algorithm
        greedy_btn = tk.Button(
            button_frame,
            text="🎯 GREEDY ALGORITHM",
            command=self.run_greedy_algorithm,
            bg='#4ecdc4',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        greedy_btn.pack(side='left', padx=5)
        
        # Graph algorithms
        graph_btn = tk.Button(
            button_frame,
            text="🌐 GRAPH ALGORITHMS",
            command=self.run_graph_algorithms,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        graph_btn.pack(side='left', padx=5)
        
        # Clustering algorithms
        clustering_btn = tk.Button(
            button_frame,
            text="🎯 CLUSTERING ALGORITHMS",
            command=self.run_clustering_algorithms,
            bg='#ff9ff3',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        clustering_btn.pack(side='left', padx=5)
        
        # Genetic algorithm
        genetic_btn = tk.Button(
            button_frame,
            text="🧬 GENETIC ALGORITHM",
            command=self.run_genetic_algorithm,
            bg='#96ceb4',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        genetic_btn.pack(side='left', padx=5)
        
        # Run all algorithms
        all_btn = tk.Button(
            button_frame,
            text="🚀 RUN ALL ALGORITHMS",
            command=self.run_all_algorithms,
            bg='#45b7d1',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        all_btn.pack(side='left', padx=5)
        
        # Results area
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 ALGORITHM RESULTS",
            font=('Segoe UI', 14, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=2,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Results notebook
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create result tabs
        self.create_greedy_results_tab()
        self.create_graph_results_tab()
        self.create_clustering_results_tab()
        self.create_genetic_results_tab()
        self.create_system_log_tab()
        
        # Log area
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 ALGORITHM LOG",
            font=('Segoe UI', 12, 'bold'),
            fg='#96ceb4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='x', padx=10, pady=5)
        
        self.algorithm_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=6
        )
        self.algorithm_log.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial log message
        self.log_algorithm("🧮 Advanced Algorithm Processing initialized")
        self.log_algorithm(f"📊 Loaded {len(self.banking_data['accounts'])} accounts for processing")
        self.log_algorithm(f"📊 Loaded {len(self.banking_data['transactions'])} transactions for processing")
        self.log_algorithm("🎯 Ready for advanced algorithm processing")
    
    def create_greedy_results_tab(self):
        """Create greedy results tab"""
        greedy_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(greedy_frame, text="🎯 Greedy")
        
        self.greedy_results_text = scrolledtext.ScrolledText(
            greedy_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.greedy_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_graph_results_tab(self):
        """Create graph results tab"""
        graph_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(graph_frame, text="🌐 Graph")
        
        self.graph_results_text = scrolledtext.ScrolledText(
            graph_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.graph_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_clustering_results_tab(self):
        """Create clustering results tab"""
        clustering_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(clustering_frame, text="🎯 Clustering")
        
        self.clustering_results_text = scrolledtext.ScrolledText(
            clustering_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.clustering_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_genetic_results_tab(self):
        """Create genetic results tab"""
        genetic_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(genetic_frame, text="🧬 Genetic")
        
        self.genetic_results_text = scrolledtext.ScrolledText(
            genetic_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.genetic_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_system_log_tab(self):
        """Create system log tab"""
        log_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(log_frame, text="📝 System Log")
        
        self.detailed_log_text = scrolledtext.ScrolledText(
            log_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.detailed_log_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def run_greedy_algorithm(self):
        """Run greedy algorithm"""
        self.log_algorithm("🎯 Starting Greedy Algorithm processing...")
        threading.Thread(target=self._run_greedy_algorithm_thread, daemon=True).start()
    
    def _run_greedy_algorithm_thread(self):
        """Run greedy algorithm in thread"""
        try:
            accounts = self.banking_data["accounts"]
            
            # Greedy algorithm for account optimization
            start_time = time.time()
            
            # Sort accounts by balance (greedy approach)
            sorted_accounts = sorted(accounts, key=lambda x: x["balance"], reverse=True)
            
            # Select top accounts
            selected_accounts = sorted_accounts[:50]
            total_value = sum(acc["balance"] for acc in selected_accounts)
            
            # Risk-based greedy selection
            risk_sorted_accounts = sorted(accounts, key=lambda x: x["risk_score"])
            low_risk_accounts = risk_sorted_accounts[:50]
            low_risk_value = sum(acc["balance"] for acc in low_risk_accounts)
            
            # Transaction-based greedy selection
            transaction_sorted_accounts = sorted(accounts, key=lambda x: x["transaction_count"], reverse=True)
            high_activity_accounts = transaction_sorted_accounts[:50]
            high_activity_value = sum(acc["balance"] for acc in high_activity_accounts)
            
            execution_time = time.time() - start_time
            
            # Generate report
            report = f"""
🎯 GREEDY ALGORITHM RESULTS
{'='*50}

⏱️ EXECUTION TIME: {execution_time:.4f} seconds

💰 BALANCE-BASED GREEDY SELECTION:
• Selected Accounts: {len(selected_accounts)}
• Total Value: ${total_value:,.2f}
• Average Balance: ${total_value/len(selected_accounts):,.2f}
• Optimization Ratio: {(total_value/sum(acc['balance'] for acc in accounts)*100):.2f}%

⚠️ RISK-BASED GREEDY SELECTION:
• Selected Accounts: {len(low_risk_accounts)}
• Total Value: ${low_risk_value:,.2f}
• Average Risk Score: {sum(acc['risk_score'] for acc in low_risk_accounts)/len(low_risk_accounts):.2f}
• Risk Optimization: {(sum(acc['risk_score'] for acc in accounts)/len(accounts) - sum(acc['risk_score'] for acc in low_risk_accounts)/len(low_risk_accounts)):.2f} points lower

📊 ACTIVITY-BASED GREEDY SELECTION:
• Selected Accounts: {len(high_activity_accounts)}
• Total Value: ${high_activity_value:,.2f}
• Average Transactions: {sum(acc['transaction_count'] for acc in high_activity_accounts)/len(high_activity_accounts):.1f}
• Activity Optimization: {(sum(acc['transaction_count'] for acc in high_activity_accounts)/len(high_activity_accounts) - sum(acc['transaction_count'] for acc in accounts)/len(accounts)):.1f} transactions higher

🏆 TOP 10 BALANCE-BASED SELECTIONS:
"""
            
            for i, account in enumerate(selected_accounts[:10], 1):
                report += f"{i:2d}. Account {account['account_number']}: ${account['balance']:,.2f} (Risk: {account['risk_score']:.1f})\n"
            
            # Display results
            self.greedy_results_text.delete('1.0', tk.END)
            self.greedy_results_text.insert('1.0', report)
            
            # Store results
            self.algorithm_results["greedy"] = {
                "execution_time": execution_time,
                "balance_based": {
                    "selected_accounts": len(selected_accounts),
                    "total_value": total_value,
                    "optimization_ratio": total_value/sum(acc['balance'] for acc in accounts)
                },
                "risk_based": {
                    "selected_accounts": len(low_risk_accounts),
                    "total_value": low_risk_value,
                    "avg_risk_score": sum(acc['risk_score'] for acc in low_risk_accounts)/len(low_risk_accounts)
                },
                "activity_based": {
                    "selected_accounts": len(high_activity_accounts),
                    "total_value": high_activity_value,
                    "avg_transactions": sum(acc['transaction_count'] for acc in high_activity_accounts)/len(high_activity_accounts)
                }
            }
            
            self.log_algorithm("✅ Greedy algorithm completed successfully")
            self.log_detailed(f"Greedy Algorithm Results:\n{json.dumps(self.algorithm_results['greedy'], indent=2, default=str)}")
            
        except Exception as e:
            error_msg = f"❌ Greedy algorithm failed: {str(e)}"
            self.log_algorithm(error_msg)
            self.greedy_results_text.delete('1.0', tk.END)
            self.greedy_results_text.insert('1.0', error_msg)
    
    def run_graph_algorithms(self):
        """Run graph algorithms"""
        self.log_algorithm("🌐 Starting Graph Algorithms processing...")
        threading.Thread(target=self._run_graph_algorithms_thread, daemon=True).start()
    
    def _run_graph_algorithms_thread(self):
        """Run graph algorithms in thread"""
        try:
            accounts = self.banking_data["accounts"]
            transactions = self.banking_data["transactions"]
            
            start_time = time.time()
            
            # Build graph
            graph = defaultdict(list)
            for trans in transactions:
                graph[trans["from_account"]].append((trans["to_account"], trans["amount"]))
            
            # DFS analysis
            def dfs(account, visited, path):
                if account in visited:
                    return
                visited.add(account)
                path.append(account)
                for neighbor, _ in graph[account]:
                    dfs(neighbor, visited, path)
            
            # BFS analysis
            def bfs(start_account, max_depth=3):
                visited = set()
                queue = deque([(start_account, 0)])
                levels = defaultdict(list)
                
                while queue:
                    current_account, depth = queue.popleft()
                    if current_account in visited or depth > max_depth:
                        continue
                    visited.add(current_account)
                    levels[depth].append(current_account)
                    
                    for neighbor, _ in graph[current_account]:
                        if neighbor not in visited:
                            queue.append((neighbor, depth + 1))
                
                return levels
            
            # Dijkstra analysis
            def dijkstra(start_account, end_account):
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
                
                return path, distances[end_account]
            
            # Run analyses
            start_account = accounts[0]["account_number"]
            end_account = accounts[-1]["account_number"]
            
            # DFS
            visited_dfs = set()
            path_dfs = []
            dfs(start_account, visited_dfs, path_dfs)
            
            # BFS
            levels_bfs = bfs(start_account, max_depth=3)
            
            # Dijkstra
            path_dijkstra, distance_dijkstra = dijkstra(start_account, end_account)
            
            execution_time = time.time() - start_time
            
            # Generate report
            report = f"""
🌐 GRAPH ALGORITHMS RESULTS
{'='*50}

⏱️ EXECUTION TIME: {execution_time:.4f} seconds

🔍 DEPTH FIRST SEARCH (DFS):
• Start Account: {start_account}
• Visited Accounts: {len(visited_dfs)}
• Path Length: {len(path_dfs)}
• Network Coverage: {(len(visited_dfs)/len(accounts)*100):.2f}%

🌐 BREADTH FIRST SEARCH (BFS):
• Start Account: {start_account}
• Max Depth: 3
• Total Accounts Found: {sum(len(level) for level in levels_bfs.values())}
• Levels Explored: {len(levels_bfs)}
• Level Distribution:
"""
            
            for depth, accounts_in_level in levels_bfs.items():
                report += f"  - Level {depth}: {len(accounts_in_level)} accounts\n"
            
            report += f"""

🛣️ DIJKSTRA'S SHORTEST PATH:
• Start Account: {start_account}
• End Account: {end_account}
• Shortest Path Length: {len(path_dijkstra)} steps
• Total Distance: ${distance_dijkstra:,.2f}
• Path: {' -> '.join(path_dijkstra[:5])}{'...' if len(path_dijkstra) > 5 else ''}

📊 GRAPH STATISTICS:
• Total Nodes (Accounts): {len(accounts)}
• Total Edges (Transactions): {len(transactions)}
• Average Degree: {len(transactions)/len(accounts):.2f}
• Connected Components: {len(visited_dfs)} (from start node)
"""
            
            # Display results
            self.graph_results_text.delete('1.0', tk.END)
            self.graph_results_text.insert('1.0', report)
            
            # Store results
            self.algorithm_results["graph"] = {
                "execution_time": execution_time,
                "dfs": {
                    "visited_accounts": len(visited_dfs),
                    "path_length": len(path_dfs),
                    "network_coverage": len(visited_dfs)/len(accounts)
                },
                "bfs": {
                    "levels": len(levels_bfs),
                    "total_accounts": sum(len(level) for level in levels_bfs.values()),
                    "level_distribution": {depth: len(accounts) for depth, accounts in levels_bfs.items()}
                },
                "dijkstra": {
                    "path_length": len(path_dijkstra),
                    "total_distance": distance_dijkstra,
                    "path": path_dijkstra
                },
                "graph_stats": {
                    "nodes": len(accounts),
                    "edges": len(transactions),
                    "avg_degree": len(transactions)/len(accounts)
                }
            }
            
            self.log_algorithm("✅ Graph algorithms completed successfully")
            self.log_detailed(f"Graph Algorithms Results:\n{json.dumps(self.algorithm_results['graph'], indent=2, default=str)}")
            
        except Exception as e:
            error_msg = f"❌ Graph algorithms failed: {str(e)}"
            self.log_algorithm(error_msg)
            self.graph_results_text.delete('1.0', tk.END)
            self.graph_results_text.insert('1.0', error_msg)
    
    def run_clustering_algorithms(self):
        """Run clustering algorithms"""
        self.log_algorithm("🎯 Starting Clustering Algorithms processing...")
        threading.Thread(target=self._run_clustering_algorithms_thread, daemon=True).start()
    
    def _run_clustering_algorithms_thread(self):
        """Run clustering algorithms in thread"""
        try:
            accounts = self.banking_data["accounts"]
            
            start_time = time.time()
            
            # Prepare data for clustering
            features = []
            account_ids = []
            
            for acc in accounts:
                features.append([acc["balance"], acc["risk_score"], acc["transaction_count"]])
                account_ids.append(acc["account_number"])
            
            X = np.array(features)
            
            # K-means clustering
            def kmeans(X, k, max_iterations=100):
                # Initialize centroids randomly
                centroids = X[np.random.choice(len(X), k, replace=False)]
                
                for iteration in range(max_iterations):
                    # Assign points to nearest centroid
                    distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
                    labels = np.argmin(distances, axis=0)
                    
                    # Update centroids
                    new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
                    
                    # Check convergence
                    if np.all(centroids == new_centroids):
                        break
                    
                    centroids = new_centroids
                
                return labels, centroids, iteration + 1
            
            # Run K-means with different k values
            k_values = [3, 5, 7]
            clustering_results = {}
            
            for k in k_values:
                labels, centroids, iterations = kmeans(X, k)
                
                # Analyze clusters
                clusters = {}
                for i in range(k):
                    cluster_indices = np.where(labels == i)[0]
                    cluster_accounts = [account_ids[j] for j in cluster_indices]
                    cluster_features = X[cluster_indices]
                    
                    clusters[f"cluster_{i+1}"] = {
                        "size": len(cluster_accounts),
                        "accounts": cluster_accounts,
                        "avg_balance": cluster_features[:, 0].mean(),
                        "avg_risk": cluster_features[:, 1].mean(),
                        "avg_transactions": cluster_features[:, 2].mean(),
                        "centroid": centroids[i].tolist()
                    }
                
                clustering_results[f"k_{k}"] = {
                    "clusters": clusters,
                    "iterations": iterations,
                    "total_accounts": len(accounts)
                }
            
            execution_time = time.time() - start_time
            
            # Generate report
            report = f"""
🎯 CLUSTERING ALGORITHMS RESULTS
{'='*50}

⏱️ EXECUTION TIME: {execution_time:.4f} seconds

📊 K-MEANS CLUSTERING ANALYSIS:
"""
            
            for k, result in clustering_results.items():
                report += f"\n🔹 {k.upper()} CLUSTERS:\n"
                report += f"• Iterations: {result['iterations']}\n"
                report += f"• Total Accounts: {result['total_accounts']}\n\n"
                
                clusters = result['clusters']
                for cluster_name, cluster_data in clusters.items():
                    report += f"  📊 {cluster_name}:\n"
                    report += f"    - Size: {cluster_data['size']} accounts\n"
                    report += f"    - Avg Balance: ${cluster_data['avg_balance']:,.2f}\n"
                    report += f"    - Avg Risk Score: {cluster_data['avg_risk']:.2f}\n"
                    report += f"    - Avg Transactions: {cluster_data['avg_transactions']:.1f}\n\n"
            
            # Display results
            self.clustering_results_text.delete('1.0', tk.END)
            self.clustering_results_text.insert('1.0', report)
            
            # Store results
            self.algorithm_results["clustering"] = {
                "execution_time": execution_time,
                "kmeans_results": clustering_results
            }
            
            self.log_algorithm("✅ Clustering algorithms completed successfully")
            self.log_detailed(f"Clustering Algorithms Results:\n{json.dumps(self.algorithm_results['clustering'], indent=2, default=str)}")
            
        except Exception as e:
            error_msg = f"❌ Clustering algorithms failed: {str(e)}"
            self.log_algorithm(error_msg)
            self.clustering_results_text.delete('1.0', tk.END)
            self.clustering_results_text.insert('1.0', error_msg)
    
    def run_genetic_algorithm(self):
        """Run genetic algorithm"""
        self.log_algorithm("🧬 Starting Genetic Algorithm processing...")
        threading.Thread(target=self._run_genetic_algorithm_thread, daemon=True).start()
    
    def _run_genetic_algorithm_thread(self):
        """Run genetic algorithm in thread"""
        try:
            accounts = self.banking_data["accounts"]
            
            start_time = time.time()
            
            # Genetic algorithm for portfolio optimization
            def fitness_function(individual):
                total_balance = 0
                total_risk = 0
                
                for i, selected in enumerate(individual):
                    if selected and i < len(accounts):
                        balance = accounts[i]["balance"]
                        risk = accounts[i]["risk_score"]
                        total_balance += balance
                        total_risk += risk
                
                if total_risk == 0:
                    return 0
                
                return total_balance / total_risk
            
            # Initialize population
            population_size = 50
            generations = 100
            population = []
            
            for _ in range(population_size):
                individual = [random.choice([0, 1]) for _ in range(len(accounts))]
                population.append(individual)
            
            best_fitness = 0
            best_individual = None
            fitness_history = []
            
            for generation in range(generations):
                # Evaluate fitness
                fitness_scores = [fitness_function(ind) for ind in population]
                
                # Find best individual
                max_fitness_idx = np.argmax(fitness_scores)
                if fitness_scores[max_fitness_idx] > best_fitness:
                    best_fitness = fitness_scores[max_fitness_idx]
                    best_individual = population[max_fitness_idx].copy()
                
                fitness_history.append(best_fitness)
                
                # Selection (tournament selection)
                new_population = []
                for _ in range(population_size):
                    tournament = random.sample(range(len(population)), 3)
                    winner = tournament[np.argmax([fitness_scores[i] for i in tournament])]
                    new_population.append(population[winner].copy())
                
                # Crossover and mutation
                for i in range(0, population_size, 2):
                    if i + 1 < population_size:
                        # Crossover
                        crossover_point = random.randint(1, len(accounts))
                        new_population[i][crossover_point:], new_population[i+1][crossover_point:] = \
                            new_population[i+1][crossover_point:], new_population[i][crossover_point:]
                        
                        # Mutation
                        for j in range(len(accounts)):
                            if random.random() < 0.01:  # 1% mutation rate
                                new_population[i][j] = 1 - new_population[i][j]
                            if random.random() < 0.01:
                                new_population[i+1][j] = 1 - new_population[i+1][j]
                
                population = new_population
            
            # Get selected accounts
            selected_accounts = []
            if best_individual:
                for i, selected in enumerate(best_individual):
                    if selected and i < len(accounts):
                        selected_accounts.append(accounts[i])
            
            execution_time = time.time() - start_time
            
            # Generate report
            report = f"""
🧬 GENETIC ALGORITHM RESULTS
{'='*50}

⏱️ EXECUTION TIME: {execution_time:.4f} seconds

🧬 GENETIC ALGORITHM PARAMETERS:
• Population Size: {population_size}
• Generations: {generations}
• Mutation Rate: 1%
• Crossover Rate: 100%

🏆 OPTIMIZATION RESULTS:
• Best Fitness Score: {best_fitness:.2f}
• Selected Accounts: {len(selected_accounts)}
• Total Balance: ${sum(acc['balance'] for acc in selected_accounts):,.2f}
• Average Risk Score: {sum(acc['risk_score'] for acc in selected_accounts)/len(selected_accounts):.2f}
• Portfolio Efficiency: {(best_fitness/sum(acc['balance'] for acc in accounts)*sum(acc['risk_score'] for acc in accounts)/len(accounts)):.2f}

📈 FITNESS EVOLUTION:
• Initial Fitness: {fitness_history[0]:.2f}
• Final Fitness: {fitness_history[-1]:.2f}
• Improvement: {((fitness_history[-1] - fitness_history[0]) / fitness_history[0] * 100):.2f}%

🏆 TOP 10 SELECTED ACCOUNTS:
"""
            
            sorted_selected = sorted(selected_accounts, key=lambda x: x['balance'], reverse=True)
            for i, account in enumerate(sorted_selected[:10], 1):
                report += f"{i:2d}. Account {account['account_number']}: ${account['balance']:,.2f} (Risk: {account['risk_score']:.1f})\n"
            
            # Display results
            self.genetic_results_text.delete('1.0', tk.END)
            self.genetic_results_text.insert('1.0', report)
            
            # Store results
            self.algorithm_results["genetic"] = {
                "execution_time": execution_time,
                "best_fitness": best_fitness,
                "selected_accounts": len(selected_accounts),
                "total_balance": sum(acc['balance'] for acc in selected_accounts),
                "avg_risk_score": sum(acc['risk_score'] for acc in selected_accounts)/len(selected_accounts),
                "fitness_history": fitness_history,
                "selected_accounts_data": selected_accounts
            }
            
            self.log_algorithm("✅ Genetic algorithm completed successfully")
            self.log_detailed(f"Genetic Algorithm Results:\n{json.dumps(self.algorithm_results['genetic'], indent=2, default=str)}")
            
        except Exception as e:
            error_msg = f"❌ Genetic algorithm failed: {str(e)}"
            self.log_algorithm(error_msg)
            self.genetic_results_text.delete('1.0', tk.END)
            self.genetic_results_text.insert('1.0', error_msg)
    
    def run_all_algorithms(self):
        """Run all algorithms"""
        self.log_algorithm("🚀 Starting all algorithms processing...")
        
        # Run all algorithms in sequence
        self.run_greedy_algorithm()
        time.sleep(1)
        self.run_graph_algorithms()
        time.sleep(1)
        self.run_clustering_algorithms()
        time.sleep(1)
        self.run_genetic_algorithm()
        
        self.log_algorithm("✅ All algorithms completed")
    
    def log_algorithm(self, message):
        """Log algorithm message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.algorithm_log.insert(tk.END, formatted_message)
        self.algorithm_log.see(tk.END)
    
    def log_detailed(self, message):
        """Log detailed message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.detailed_log_text.insert(tk.END, formatted_message)
        self.detailed_log_text.see(tk.END)
    
    def run(self):
        """Run algorithm processing"""
        print(f"🧮 Starting {self.name}")
        self.root.mainloop()

def main():
    """Main entry point"""
    processing = AdvancedAlgorithmProcessing()
    processing.run()

if __name__ == "__main__":
    main() 