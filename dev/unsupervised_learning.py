"""
DEVELOPMENTAL SILO - Unsupervised Learning Methods
Pattern Discovery, Clustering, and Anomaly Detection
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA, NMF
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
# Try to import visualization libraries
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class UnsupervisedLearning:
    """Unsupervised Learning Engine for Pattern Discovery"""
    
    def __init__(self):
        self.clusters = {}
        self.anomalies = {}
        self.patterns = {}
        self.scaler = StandardScaler()
        
    def discover_patterns(self, attack_data: List[Dict]) -> Dict[str, Any]:
        """Discover patterns in attack data using clustering"""
        if not attack_data:
            return {"message": "No data available"}
        
        # Convert to DataFrame
        df = pd.DataFrame(attack_data)
        
        # Extract numerical features
        features = self._extract_numerical_features(df)
        
        if len(features) < 2:
            return {"message": "Insufficient data for clustering"}
        
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Apply multiple clustering algorithms
        results = {}
        
        # K-Means Clustering
        results['kmeans'] = self._kmeans_clustering(features_scaled)
        
        # DBSCAN Clustering
        results['dbscan'] = self._dbscan_clustering(features_scaled)
        
        # Hierarchical Clustering
        results['hierarchical'] = self._hierarchical_clustering(features_scaled)
        
        # Dimensionality Reduction for visualization
        results['pca'] = self._pca_analysis(features_scaled)
        results['tsne'] = self._tsne_analysis(features_scaled)
        
        # Pattern Analysis
        results['patterns'] = self._analyze_patterns(df)
        
        return results
    
    def _extract_numerical_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract numerical features for clustering"""
        features = []
        
        for _, row in df.iterrows():
            feature_vector = [
                len(str(row.get('target', ''))),
                len(str(row.get('payload', ''))),
                row.get('response_code', 0),
                row.get('response_time', 0),
                row.get('confidence_score', 0),
                1 if row.get('success', False) else 0,
                str(row.get('payload', '')).count("'"),
                str(row.get('payload', '')).count('"'),
                str(row.get('payload', '')).count(';'),
                str(row.get('target', '')).count('.'),
                str(row.get('target', '')).count('/'),
                str(row.get('target', '')).count('?'),
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def _kmeans_clustering(self, features: np.ndarray) -> Dict[str, Any]:
        """K-Means clustering analysis"""
        try:
            # Find optimal number of clusters
            inertias = []
            silhouette_scores = []
            K_range = range(2, min(10, len(features)))
            
            for k in K_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(features)
                inertias.append(kmeans.inertia_)
                silhouette_scores.append(silhouette_score(features, kmeans.labels_))
            
            # Choose optimal K
            optimal_k = K_range[np.argmax(silhouette_scores)]
            
            # Final clustering
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(features)
            
            return {
                'method': 'K-Means',
                'optimal_clusters': optimal_k,
                'cluster_labels': cluster_labels.tolist(),
                'inertia': kmeans.inertia_,
                'silhouette_score': silhouette_score(features, cluster_labels),
                'cluster_centers': kmeans.cluster_centers_.tolist()
            }
        except Exception as e:
            logger.error(f"K-Means clustering error: {e}")
            return {'error': str(e)}
    
    def _dbscan_clustering(self, features: np.ndarray) -> Dict[str, Any]:
        """DBSCAN clustering for density-based pattern discovery"""
        try:
            # Try different epsilon values
            eps_values = [0.1, 0.5, 1.0, 2.0, 5.0]
            best_score = -1
            best_result = None
            
            for eps in eps_values:
                dbscan = DBSCAN(eps=eps, min_samples=2)
                labels = dbscan.fit_predict(features)
                
                # Skip if all points are noise
                if len(set(labels)) < 2:
                    continue
                
                # Calculate silhouette score (excluding noise points)
                non_noise_mask = labels != -1
                if np.sum(non_noise_mask) > 1:
                    score = silhouette_score(features[non_noise_mask], labels[non_noise_mask])
                    if score > best_score:
                        best_score = score
                        best_result = {
                            'method': 'DBSCAN',
                            'epsilon': eps,
                            'cluster_labels': labels.tolist(),
                            'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
                            'n_noise': list(labels).count(-1),
                            'silhouette_score': score
                        }
            
            return best_result if best_result else {'error': 'No valid clusters found'}
            
        except Exception as e:
            logger.error(f"DBSCAN clustering error: {e}")
            return {'error': str(e)}
    
    def _hierarchical_clustering(self, features: np.ndarray) -> Dict[str, Any]:
        """Hierarchical clustering analysis"""
        try:
            # Use Agglomerative Clustering
            n_clusters = min(5, len(features) // 2)
            hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
            cluster_labels = hierarchical.fit_predict(features)
            
            return {
                'method': 'Hierarchical',
                'n_clusters': n_clusters,
                'cluster_labels': cluster_labels.tolist(),
                'silhouette_score': silhouette_score(features, cluster_labels),
                'linkage': 'ward'
            }
        except Exception as e:
            logger.error(f"Hierarchical clustering error: {e}")
            return {'error': str(e)}
    
    def _pca_analysis(self, features: np.ndarray) -> Dict[str, Any]:
        """PCA for dimensionality reduction and pattern discovery"""
        try:
            pca = PCA(n_components=min(3, features.shape[1]))
            features_pca = pca.fit_transform(features)
            
            return {
                'method': 'PCA',
                'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
                'cumulative_variance': np.cumsum(pca.explained_variance_ratio_).tolist(),
                'reduced_features': features_pca.tolist(),
                'n_components': pca.n_components_
            }
        except Exception as e:
            logger.error(f"PCA analysis error: {e}")
            return {'error': str(e)}
    
    def _tsne_analysis(self, features: np.ndarray) -> Dict[str, Any]:
        """t-SNE for non-linear dimensionality reduction"""
        try:
            tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(features)-1))
            features_tsne = tsne.fit_transform(features)
            
            return {
                'method': 't-SNE',
                'reduced_features': features_tsne.tolist(),
                'perplexity': tsne.perplexity
            }
        except Exception as e:
            logger.error(f"t-SNE analysis error: {e}")
            return {'error': str(e)}
    
    def _analyze_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze patterns in the data"""
        patterns = {}
        
        # Success rate patterns
        if 'success' in df.columns:
            patterns['success_rate'] = df['success'].mean()
            patterns['success_by_type'] = df.groupby('attack_type')['success'].mean().to_dict()
        
        # Response time patterns
        if 'response_time' in df.columns:
            patterns['avg_response_time'] = df['response_time'].mean()
            patterns['response_time_distribution'] = {
                'min': df['response_time'].min(),
                'max': df['response_time'].max(),
                'std': df['response_time'].std()
            }
        
        # Payload patterns
        if 'payload' in df.columns:
            payload_lengths = df['payload'].str.len()
            patterns['payload_length'] = {
                'mean': payload_lengths.mean(),
                'std': payload_lengths.std(),
                'distribution': payload_lengths.describe().to_dict()
            }
        
        return patterns
    
    def detect_anomalies(self, attack_data: List[Dict]) -> Dict[str, Any]:
        """Detect anomalies in attack data"""
        if not attack_data:
            return {"message": "No data available"}
        
        features = self._extract_numerical_features(pd.DataFrame(attack_data))
        
        if len(features) < 2:
            return {"message": "Insufficient data for anomaly detection"}
        
        features_scaled = self.scaler.fit_transform(features)
        
        results = {}
        
        # Isolation Forest
        results['isolation_forest'] = self._isolation_forest_detection(features_scaled)
        
        # Local Outlier Factor
        results['lof'] = self._lof_detection(features_scaled)
        
        return results
    
    def _isolation_forest_detection(self, features: np.ndarray) -> Dict[str, Any]:
        """Isolation Forest for anomaly detection"""
        try:
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = iso_forest.fit_predict(features)
            
            return {
                'method': 'Isolation Forest',
                'anomaly_labels': anomaly_labels.tolist(),
                'n_anomalies': list(anomaly_labels).count(-1),
                'anomaly_ratio': list(anomaly_labels).count(-1) / len(anomaly_labels)
            }
        except Exception as e:
            logger.error(f"Isolation Forest error: {e}")
            return {'error': str(e)}
    
    def _lof_detection(self, features: np.ndarray) -> Dict[str, Any]:
        """Local Outlier Factor for anomaly detection"""
        try:
            lof = LocalOutlierFactor(contamination=0.1)
            anomaly_labels = lof.fit_predict(features)
            
            return {
                'method': 'Local Outlier Factor',
                'anomaly_labels': anomaly_labels.tolist(),
                'n_anomalies': list(anomaly_labels).count(-1),
                'anomaly_ratio': list(anomaly_labels).count(-1) / len(anomaly_labels)
            }
        except Exception as e:
            logger.error(f"LOF error: {e}")
            return {'error': str(e)}
    
    def generate_insights(self, attack_data: List[Dict]) -> Dict[str, Any]:
        """Generate insights from unsupervised learning"""
        insights = {}
        
        # Pattern discovery
        pattern_results = self.discover_patterns(attack_data)
        insights['patterns'] = pattern_results
        
        # Anomaly detection
        anomaly_results = self.detect_anomalies(attack_data)
        insights['anomalies'] = anomaly_results
        
        # Key insights
        insights['key_findings'] = self._extract_key_insights(pattern_results, anomaly_results)
        
        return insights
    
    def _extract_key_insights(self, patterns: Dict, anomalies: Dict) -> List[str]:
        """Extract key insights from analysis results"""
        insights = []
        
        # Pattern insights
        if 'kmeans' in patterns and 'optimal_clusters' in patterns['kmeans']:
            insights.append(f"Data naturally clusters into {patterns['kmeans']['optimal_clusters']} groups")
        
        if 'patterns' in patterns and 'success_rate' in patterns['patterns']:
            success_rate = patterns['patterns']['success_rate']
            insights.append(f"Overall success rate: {success_rate:.2%}")
        
        # Anomaly insights
        if 'isolation_forest' in anomalies and 'anomaly_ratio' in anomalies['isolation_forest']:
            anomaly_ratio = anomalies['isolation_forest']['anomaly_ratio']
            insights.append(f"Anomaly detection rate: {anomaly_ratio:.2%}")
        
        return insights 