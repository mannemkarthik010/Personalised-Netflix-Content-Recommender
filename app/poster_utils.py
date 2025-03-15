
import requests
import streamlit as st
from io import BytesIO
from functools import lru_cache

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

def get_movie_poster(title):
    """Fetch movie poster with timeout"""
    try:
        with requests.Session() as session:
            response = session.get(
                f"https://api.themoviedb.org/3/search/movie",
                params={
                    "api_key": st.secrets["TMDB_API_KEY"],
                    "query": title
                },
                timeout=3  
            )
    except (requests.Timeout, ConnectionError):
        return "assets/default_poster.png"

def display_poster(url):
    """Display poster with loading state"""
    with st.spinner("Loading poster..."):
        try:
            response = requests.get(url)
            img = BytesIO(response.content)
            st.image(img, use_column_width=True)
        except:
            st.image("assets/default_poster.png")
