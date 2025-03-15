import streamlit as st

# Custom HTML & CSS for Netflix-style logo
html_code = """
<style>
    .netflix-logo {
        font-size: 100px;
        font-weight: bold;
        color: #E50914;
        text-shadow: 4px 4px 10px rgba(0, 0, 0, 0.7);
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin-top: 100px;
    }
    .background {
        background-color: black;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
<div class='background'>
    <div class='netflix-logo'>N</div>
</div>
"""

# Streamlit app
def main():
    st.set_page_config(page_title='Netflix Logo', layout='wide')
    st.markdown(html_code, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
