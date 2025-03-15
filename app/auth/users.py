import streamlit as st
from .database import auth_db
from .components import show_auth_ui, hide_main_ui
def authentication_flow():
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None

    if not st.session_state.authenticated:
        show_auth_ui()  
        handle_auth_forms()  
        st.stop()  
    else:
        return  

def handle_auth_forms():
    
    auth_tab, reg_tab = st.tabs(["Login", "Register"])
    
    with auth_tab:
        with st.form("Login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                user = auth_db.authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = username
                    st.rerun() 
                else:
                    st.error("Invalid credentials")

    with reg_tab:
        with st.form("Register"):
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Create Account"):
                if new_pass != confirm_pass:
                    st.error("Passwords don't match")
                elif auth_db.create_user(new_user, new_pass):
                    st.success("Account created! Please login")
                    st.rerun()
                else:
                    st.error("Username exists")
