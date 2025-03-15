# app/ui_components.py
import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app.poster_utils import display_poster
def show_header():
    """Display application header"""
    st.markdown("""
    <style>
        .header {
            background-color: #E50914;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
    </style>
    <div class="header">
        <h1 style='color:white; text-align:center'>🍿 NextFlix Recommendations</h1>
    </div>
    """, unsafe_allow_html=True)

def show_recommendations(recommendations, scores, user):
    """Display recommendations in a vertical layout (one by one)"""
    st.subheader("Top Recommendations")
    
    # Loop through each recommendation and display it vertically
    for idx, (_, row) in enumerate(recommendations.iterrows()):
        # Convert the row to a dictionary and pass it to movie_card
        movie_card(row.to_dict(), scores[idx], user, idx)
def movie_card(movie, score, user, idx):
    """Interactive movie card with watchlist, watched status, and Netflix redirect"""
    with st.container(border=True):
        # Display the movie title and match score
        st.markdown(f"### {movie['title']}")
        st.caption(f"**{movie['genres']}** | ⭐ {movie.get('rating', 'N/A')}")
        st.progress(score, text=f"Match: {score*100:.1f}%")
        
        # Display the poster
        poster_url = movie.get("poster_url", "assets/default_poster.png")
        display_poster(poster_url)
        
        # Display the movie description
        st.write(f"{movie['description'][:150]}...")
        
        # Action buttons (Add to Watchlist, Mark as Watched, Watch Now)
        col1, col2, col3 = st.columns(3)
        
        # Add to Watchlist button
        with col1:
            if st.button("+ Watchlist", key=f"wl_{movie.get('show_id', f'unknown_{idx}')}"):
                from app.auth.database import auth_db
                auth_db.add_to_watchlist(user, movie.get('show_id'))
                st.toast(f"Added '{movie['title']}' to your watchlist!")
        
        # Mark as Watched button
        with col2:
            if st.button("✔️ Watched", key=f"wd_{movie.get('show_id', f'unknown_{idx}')}"):
                from app.auth.database import auth_db
                auth_db.mark_as_watched(user, movie.get('show_id'))
                st.toast(f"Marked '{movie['title']}' as watched!")
        
        # Watch Now button (Netflix redirect)
        with col3:
            if st.button("▶️ Watch Now", key=f"wn_{movie.get('show_id', f'unknown_{idx}')}"):
                redirect_to_netflix(movie['title'])

def redirect_to_netflix(movie_title):
    """Redirect to Netflix search for the movie"""
    import urllib.parse
    query = urllib.parse.quote(movie_title)
    st.markdown(f"[▶️ Watch Now on Netflix](https://www.netflix.com/search?q={query})", unsafe_allow_html=True)
def movie_selector(movie_titles):
    """Interactive movie search with validation"""
    if not movie_titles:
        st.error("No movies available")
        return None
        
    return st.selectbox(
        "🔍 Search Movies:",
        options=movie_titles,
        index=None,
        placeholder="Type to search...",
        help="Start typing to find movies from our database"
    )
def movie_selector(movie_titles):
    """Interactive movie search"""
    return st.selectbox(
        "🔍 Search Movies:",
        options=movie_titles,
        index=None,
        placeholder="Type to search...",
        help="Start typing to find movies from our database"
    )

def recommendation_grid(recommendations, scores, user):
    """Responsive grid layout"""
    cols = st.columns(4)
    for idx, ((_, movie), score) in enumerate(zip(recommendations.iterrows(), scores)):
        with cols[idx % 4]:
            movie_card(movie.to_dict(), score, user)

