import streamlit as st
from pymongo import MongoClient
from PIL import Image
import os
import logging
import Report

# Set page configuration at the top level
icon = Image.open(r'Picture3.png')
st.set_page_config(
    page_title="Urbs System",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize MongoDB client
    client = MongoClient(r"mongodb://urbsdbsyestem:0yKSD1jkhHHka0b8rW4LfOcz31wLDfNiwRF8VIF82WHYWj3MeEHyqXDqcgWmNWiqBoDAwW85u1ZOACDbE8vu5g==@urbsdbsyestem.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@urbsdbsyestem@")
    db = client["urbs_project"]
    user_collection = db["login"]

    # Initialize session state for login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Add image above the title and center it
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        .form-container {
            width: 700px;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title of the app
    # st.markdown("<h1 style='text-align: center;'>URBS SYSTEMS</h1>", unsafe_allow_html=True)
    
    # Create the login form
    if not st.session_state.logged_in:
        st.markdown('<div class="center form-container">', unsafe_allow_html=True)
        with st.form("login_form"):
            st.image(r"urbs+logo+narrow+(transparent).png", width=180)
            name = st.text_input("Name")  # Added name input field
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")
        st.markdown('</div>', unsafe_allow_html=True)

        # Handle form submission
        if submit_button:
            # Check if name and username are filled
            if not name or not username:
                st.error("Name and Username are required.")
            # Hardcoded username and password
            elif password == "8i4onk96rs":
                st.session_state.logged_in = True
                st.session_state.name = "Admin"  # Assuming the name is "Admin"
                st.success("Login successful! Welcome, Admin!")  # Updated success message
                
                # Store user details in MongoDB collection
                user_collection.insert_one({
                    "loginid": username,  # Assuming 'loginid' is the shard key
                    "name": name,
                    "username": username,
                    "password": password
                })
                
                # Directly call the main function from Report
                Report.main()
                st.stop()
            else:
                st.error("Invalid username or password")
    else:
        st.success(f"Welcome back, {st.session_state.name}!")
        Report.main()

if __name__ == "__main__":
    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .icon.bi-cast {
            visibility: hidden;
            display: none;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        #stDecoration {display:none;}
    </style>
    """, unsafe_allow_html=True)
    # load Style css
    css_file_path = r'style.css'
    try:
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file_path}")
        logging.error(f"CSS file not found: {css_file_path}")
    main()