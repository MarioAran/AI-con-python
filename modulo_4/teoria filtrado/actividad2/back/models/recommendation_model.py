import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
import warnings
warnings.filterwarnings('ignore')

class AnimeRecommendationModel:
    def __init__(self):
        self.user_similarity = None
        self.anime_similarity = None
        self.user_item_matrix = None
        self.anime_features = None
        self.user_features = None
        self.anime_df = None
        self.ratings_df = None
        self.user_mapper = None
        self.anime_mapper = None
        self.model_type = "collaborative_filtering"
        
    def fit(self, ratings_df, anime_df, min_ratings=100):
        self.ratings_df = ratings_df.copy()
        self.anime_df = anime_df.copy()
        
        # Filtrar usuarios y animes con suficientes ratings
        user_rating_count = ratings_df['user_id'].value_counts()
        anime_rating_count = ratings_df['anime_id'].value_counts()
        
        filtered_users = user_rating_count[user_rating_count >= min_ratings].index
        filtered_animes = anime_rating_count[anime_rating_count >= min_ratings].index
        
        filtered_ratings = ratings_df[
            (ratings_df['user_id'].isin(filtered_users)) & 
            (ratings_df['anime_id'].isin(filtered_animes))
        ]
        
        # Crear matriz usuario-item
        self.user_item_matrix = filtered_ratings.pivot_table(
            index='user_id', 
            columns='anime_id', 
            values='rating', 
            fill_value=0
        )
        
        # Mapeos de índices
        self.user_mapper = {user: idx for idx, user in enumerate(self.user_item_matrix.index)}
        self.anime_mapper = {anime: idx for idx, anime in enumerate(self.user_item_matrix.columns)}
        
        # Calcular similitud entre usuarios
        user_matrix = self.user_item_matrix.values
        self.user_similarity = cosine_similarity(user_matrix)
        
        # Calcular similitud entre animes (transpuesta)
        anime_matrix = self.user_item_matrix.T.values
        self.anime_similarity = cosine_similarity(anime_matrix)
        
        # Reducción de dimensionalidad con SVD
        self.svd = TruncatedSVD(n_components=50, random_state=42)
        self.anime_features = self.svd.fit_transform(self.user_item_matrix.T)
        self.user_features = self.svd.fit_transform(self.user_item_matrix)
        
        return (f"Modelo entrenado con {len(filtered_users)} usuarios y {len(filtered_animes)} animes")
        
    def recommend(self, user_id, n_recommendations=10):
        """
        Generar recomendaciones para un usuario
        """
        if user_id not in self.user_mapper:
            raise ValueError(f"Usuario {user_id} no encontrado en el modelo")
        
        user_idx = self.user_mapper[user_id]
        
        # Obtener animes que el usuario ya ha visto
        user_ratings = self.user_item_matrix.iloc[user_idx]
        watched_animes = user_ratings[user_ratings > 0].index.tolist()
        
        # Calcular scores de recomendación basados en similitud de usuarios
        user_similarities = self.user_similarity[user_idx]
        
        # Promedio ponderado de ratings de usuarios similares
        similar_users_ratings = self.user_item_matrix.values.T * user_similarities
        recommendation_scores = similar_users_ratings.sum(axis=1) / (np.abs(user_similarities).sum() + 1e-8)
        
        # Crear DataFrame de scores
        anime_scores = pd.DataFrame({
            'anime_id': self.user_item_matrix.columns,
            'score': recommendation_scores
        })
        
        # Filtrar animes ya vistos
        anime_scores = anime_scores[~anime_scores['anime_id'].isin(watched_animes)]
        
        # Ordenar por score y tomar los mejores
        top_recommendations = anime_scores.nlargest(n_recommendations, 'score')
        
        # Enriquecer con información del anime
        recommendations = []
        for _, row in top_recommendations.iterrows():
            anime_id = row['anime_id']
            anime_info = self.anime_df[self.anime_df['anime_id'] == anime_id]
            
            if not anime_info.empty:
                anime_data = anime_info.iloc[0]
                recommendations.append({
                    'anime_id': int(anime_id),
                    'title': anime_data.get('name', 'Desconocido'),
                    'genre': anime_data.get('genre', 'Desconocido'),
                    'type': anime_data.get('type', 'Desconocido'),
                    'score': float(anime_data.get('score', 0)),
                    'recommendation_score': round(float(row['score']), 4)
                })
        
        return recommendations
    
    def get_similar_animes(self, anime_id, n_similar=5):
        """
        Obtener animes similares a uno dado
        """
        if anime_id not in self.anime_mapper:
            raise ValueError(f"Anime {anime_id} no encontrado")
        
        anime_idx = self.anime_mapper[anime_id]
        similar_indices = self.anime_similarity[anime_idx].argsort()[-n_similar-1:-1][::-1]
        
        similar_animes = []
        for idx in similar_indices:
            similar_anime_id = self.user_item_matrix.columns[idx]
            anime_info = self.anime_df[self.anime_df['anime_id'] == similar_anime_id]
            
            if not anime_info.empty:
                anime_data = anime_info.iloc[0]
                similarity_score = self.anime_similarity[anime_idx][idx]
                
                similar_animes.append({
                    'anime_id': int(similar_anime_id),
                    'title': anime_data.get('title', 'Desconocido'),
                    'similarity_score': round(float(similarity_score), 4)
                })
        
        return similar_animes
