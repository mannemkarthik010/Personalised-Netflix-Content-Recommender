import sys
from pathlib import Path
import streamlit as st
sys.path.append(str(Path(__file__).parent.parent))

# Then your other imports
from auth.users import authentication_flow
from data_manager import load_movie_data
from recommender import MovieRecommender
from ui_components import show_recommendations, movie_selector, show_header

# Configure page FIRST
st.set_page_config(
    page_title="NextFlix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Authentication check
    authentication_flow()
    
    # Load data with caching
    if 'movies_df' not in st.session_state:
        with st.spinner("Loading movie data..."):
            try:
                movies_df, similarity_matrix = load_movie_data()
                st.session_state.movies_df = movies_df
                st.session_state.similarity_matrix = similarity_matrix
                st.session_state.recommender = MovieRecommender(movies_df, similarity_matrix)
            except Exception as e:
                st.error(f"Failed to load data: {str(e)}")
                st.stop()
    
    # Get data from session state
    movies_df = st.session_state.movies_df
    recommender = st.session_state.recommender
    
    # Navigation sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Recommendations", "Watchlist", "Watched"]
    )
    
    # Show selected page
    if page == "Recommendations":
        show_recommendation_interface(movies_df, recommender)
    elif page == "Watchlist":
        show_watchlist(st.session_state.user)
    elif page == "Watched":
        show_watched(st.session_state.user)

def show_recommendation_interface(movies_df, recommender):
    """Main recommendation interface"""
    show_header()
    
    # Layout columns
    left_col, right_col = st.columns([1, 3])
    
    with left_col:
        st.subheader("⚙️ Controls")
        selected_movie = movie_selector(movies_df['title'].tolist())
        num_recs = st.slider("Number of Recommendations", 3, 10, 5)
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    with right_col:
        if selected_movie:
            with st.spinner("Finding recommendations..."):
                recommendations, scores = recommender.get_recommendations(selected_movie, num_recs)
                
                if recommendations is not None:
                    st.subheader(f"Recommendations for: {selected_movie}")
                    show_recommendations(recommendations, scores)
                else:
                    st.error("No recommendations found")
def show_watchlist(user):
    """Display user's watchlist"""
    st.header("⭐ Your Watchlist")
    from app.auth.database import auth_db
    watchlist_ids = auth_db.get_watchlist(user)
    
    if not watchlist_ids:
        st.info("Your watchlist is empty. Add movies from recommendations!")
        return
        
    watchlist_movies = movies_df[movies_df['id'].isin(watchlist_ids)]
    cols = st.columns(4)
    for idx, (_, movie) in enumerate(watchlist_movies.iterrows()):
        with cols[idx % 4]:
            movie_card(movie.to_dict(), 1.0, user)  # Full score for watchlist

def show_watched(user):
    """Display user's watched movies"""
    st.header("✅ Watched Movies")
    from app.auth.database import auth_db
    watched_ids = auth_db.get_watched(user)
    
    if not watched_ids:
        st.info("You haven't watched any movies yet!")
        return
        
    watched_movies = movies_df[movies_df['id'].isin(watched_ids)]
    cols = st.columns(4)
    for idx, (_, movie) in enumerate(watched_movies.iterrows()):
        with cols[idx % 4]:
            movie_card(movie.to_dict(), 1.0, user)  # Full score for watched

if __name__ == "__main__":
    main()
