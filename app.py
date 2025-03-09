import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load the dataset with better caching
@st.cache_data(show_spinner=False)
def load_data():
    movies_df = pd.read_csv('movies_df.csv')
    movies_sim = np.load('movies_sim.npz')['m']
    return movies_df, movies_sim

movies_df, movies_sim = load_data()

# Enhanced recommendation function
def recommend_movie(title, num_recommendations=5):
    if title in movies_df['title'].values:
        index = movies_df[movies_df['title'] == title].index.item()
        scores = list(enumerate(movies_sim[index]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Get recommendations with scores
        top_indices = [i[0] for i in sorted_scores[1:num_recommendations+1]]
        top_scores = [i[1] for i in sorted_scores[1:num_recommendations+1]]
        return movies_df.iloc[top_indices], top_scores
    else:
        return None, None

# Streamlit app
st.title("🎬 Netflix Movie Recommendation System")
st.write("Discover your next favorite movie based on content similarity!")

# Improved layout
col1, col2 = st.columns([3, 1])
with col1:
    # Search with autocomplete
    selected_movie = st.selectbox(
        "Search for a movie", 
        movies_df['title'].tolist(),
        placeholder="Start typing...",
        index=None
    )
with col2:
    # Recommendation number selector
    num_recs = st.slider("Number of recommendations", 3, 10, 5)

# Add visual separator
st.divider()

if selected_movie:
    if st.button("Get Recommendations 🍿", type="primary"):
        recommendations, scores = recommend_movie(selected_movie, num_recs)
        
        if recommendations is not None:
            # Display recommendations in styled cards
            st.subheader(f"Top {num_recs} Recommendations for '{selected_movie}'")
            
            # Create columns for recommendations
            cols = st.columns(num_recs)
            for idx, (_, row) in enumerate(recommendations.iterrows()):
                with cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"**{row['title']}**")
                        st.caption(f"Similarity score: {scores[idx]:.2f}")
                        st.write(f"**Genres:** {row['genres']}")
                        st.write(row['description'][:100] + "...")
            
            # Add visualization
            st.subheader("Similarity Scores")
            chart_data = pd.DataFrame({
                'Movie': recommendations['title'],
                'Similarity': scores
            })
            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X('Similarity:Q', scale=alt.Scale(domain=[0, 1])),
                y=alt.Y('Movie:N', sort='-x'),
                tooltip=['Movie', 'Similarity']
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
            
            # Add download button
            csv = recommendations[['title', 'genres', 'description']].to_csv(index=False)
            st.download_button(
                label="Download Recommendations 📥",
                data=csv,
                file_name='movie_recommendations.csv',
                mime='text/csv'
            )
            
            # Technical details expander
            with st.expander("Show technical details"):
                st.write("**Algorithm:** Content-based filtering using Cosine Similarity")
                st.write("**Feature extraction:** TF-IDF Vectorizer")
                st.write(f"**Dataset size:** {len(movies_df)} movies")
        else:
            st.error("Movie not found in the dataset. Please try another title.")
else:
    st.info("👆 Please select a movie to get recommendations")

# Add footer
st.markdown("---")
st.markdown("### Recently Added Movies")
st.dataframe(movies_df[['title', 'genres']].tail(5), hide_index=True)
