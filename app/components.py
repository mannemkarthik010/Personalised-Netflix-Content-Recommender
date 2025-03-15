import streamlit as st

def show_auth_ui():
    """Display styled authentication container"""
    st.markdown("""
    <style>
        .auth-box {
            max-width: 400px;
            margin: 5rem auto;
            padding: 2rem;
            border-radius: 10px;
            background: #1a1a1a;
            border: 1px solid #E50914;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-box">', unsafe_allow_html=True)
    st.markdown("## 🍿 NextFlix Login")
    return

def hide_main_ui():
    """Hide Streamlit default elements"""
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
