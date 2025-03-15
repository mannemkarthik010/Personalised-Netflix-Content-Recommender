import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_movie_data():
    """Load and validate movie dataset"""
    try:
        # Load movies data
        movies_df = pd.read_csv('data/movies_df.csv')
        movies_df['title'] = movies_df['title'].str.strip()
        
        # Load similarity matrix
        with np.load('data/movies_sim.npz') as data:
            similarity_matrix = data['m']
            
        # Basic validation
        if len(movies_df) == 0 or similarity_matrix.shape[0] == 0:
            st.error("Empty dataset loaded")
            st.stop()
            
        return movies_df, similarity_matrix
        
    except FileNotFoundError:
        st.error("❌ Data files not found! Please ensure:")
        st.markdown("- `data/movies_df.csv` exists")
        st.markdown("- `data/movies_sim.npz` exists")
        st.stop()
    except Exception as e:
        st.error(f"🚨 Error loading data: {str(e)}")
        st.stop()

# Export the function
__all__ = ['load_movie_data']
