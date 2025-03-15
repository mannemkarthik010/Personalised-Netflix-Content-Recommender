import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load the dataset
@st.cache_data
def load_data():
    movies_df = pd.read_csv('movies_df.csv')
    movies_sim = np.load('movies_sim.npz')['m']
    return movies_df, movies_sim

movies_df, movies_sim = load_data()

# Recommendation function
def recommend_movie(title):
    if title in movies_df['title'].values:
        index = movies_df[movies_df['title'] == title].index.item()
        scores = list(enumerate(movies_sim[index]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Get top 5 recommendations (excluding the movie itself)
        top_indices = [i[0] for i in sorted_scores[1:6]]
        return movies_df.iloc[top_indices]
    else:
        return None

# Streamlit app
st.title("Netflix Movie Recommendation System")
st.write("Welcome to the Netflix Movie Recommendation System! Enter a movie title to get recommendations.")

# User input
movie_list = movies_df['title'].tolist()
selected_movie = st.selectbox("Select a movie", movie_list)

# Display recommendations
if st.button("Get Recommendations"):
    recommendations = recommend_movie(selected_movie)
    if recommendations is not None:
        st.subheader("Top 5 Recommendations")
        st.dataframe(recommendations[['title', 'genres', 'description']])
    else:
        st.error("Movie not found in the dataset. Please try another title.")