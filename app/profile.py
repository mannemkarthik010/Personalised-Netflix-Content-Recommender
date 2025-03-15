def show_profile(username):
    from auth.database import auth_db
    
    st.header("👤 Your Profile")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Preferences")
        prefs = auth_db.get_user_profile(username).get('preferences', {})
        st.write("**Favorite Genres:**", ", ".join(prefs.get('fav_genres', [])))
        
        if st.button("Edit Preferences"):
            show_preference_form(username)
    
    with col2:
        st.subheader("Recently Viewed")
        history = auth_db.get_user_profile(username).get('history', [])[-5:]
        for item in reversed(history):
            movie = movies_df[movies_df['id'] == item['movie_id']].iloc[0]
            st.write(f"📅 {item['timestamp']}: {movie['title']}")