import numpy as np
import pandas as pd

class MovieRecommender:
    def __init__(self, movies_df, similarity_matrix, user_prefs=None):
        self.movies = movies_df
        self.similarity = similarity_matrix
        self.user_prefs = user_prefs or {}
        self.title_to_index = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()
        
    def get_recommendations(self, title, num=5):
        """Get top N similar movies"""
        try:
            idx = self.title_to_index[title]
            sim_scores = list(enumerate(self.similarity[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            top_indices = [i[0] for i in sim_scores[1:num+1]]
            return self.movies.iloc[top_indices], [i[1] for i in sim_scores[1:num+1]]
        except KeyError:
            return None, None
        
    def _genre_score(self, movie_genres):
        """Calculate genre match score"""
        if not self.user_prefs.get('fav_genres'):
            return 1  # Neutral score if no prefs
            
        movie_genres = set(movie_genres.split('|'))
        preferred = set(self.user_prefs['fav_genres'])
        
        # Jaccard similarity between user prefs and movie genres
        intersection = len(movie_genres & preferred)
        union = len(movie_genres | preferred)
        return intersection / union if union > 0 else 0

    def get_personalized_recommendations(self, title, num=5):
        """Hybrid recommendation engine"""
        base_recs, scores = self.get_recommendations(title, num*2)  # Get extra
        
        # Enhance with genre scoring
        enhanced = []
        for (_, movie), score in zip(base_recs.iterrows(), scores):
            genre_score = self._genre_score(movie['genres'])
            final_score = 0.7*score + 0.3*genre_score  # Weighted combination
            enhanced.append((movie, final_score))
        
        # Sort and return top N
        enhanced.sort(key=lambda x: x[1], reverse=True)
        return pd.DataFrame([m for m, _ in enhanced[:num]]), [s for _, s in enhanced[:num]]
