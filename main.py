import streamlit as st
from pymongo import MongoClient
from PIL import Image
import os
import logging
import Report
import base64
import traceback


# Set page configuration at the top level
icon = Image.open(r'Picture3.png')
st.set_page_config(
    page_title="Urbs System",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded"
)
# Configure logging
logging.basicConfig(level=logging.INFO)

@st.cache_data  # Updated from st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")
img2 = get_img_as_base64("photo-1501426026826-31c667bdf23d.jpg")


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img2}");
background-size: 300%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


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
        .button-container {
            display: flex;
            justify-content: center; /* Center the button */
        }
        .hover-button {
            background-color: #4CAF50; /* Green */
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .hover-button:hover {
            background-color: #45a049; /* Darker green on hover */
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
            st.markdown('<div class="button-container">', unsafe_allow_html=True)  # Center button
            submit_button = st.form_submit_button(label="Login")  # Removed css_class argument
            st.markdown('</div>', unsafe_allow_html=True)  # Close button container
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
                
                try:
                    Report.main()  # Call to Report
                except Exception as e:
                    st.error("Error loading report: " + str(e))
                    logging.error("Error loading report: " + str(e))
                    logging.error(traceback.format_exc())
                st.stop()
            else:
                st.error("Invalid username or password")
    else:
        st.success(f"Welcome back, {st.session_state.name}!")
        try:
            Report.main()  # Call to Report
        except Exception as e:
            st.error("Error loading report: " + str(e))
            logging.error("Error loading report: " + str(e))
            logging.error(traceback.format_exc())

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
