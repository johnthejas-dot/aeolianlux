import streamlit as st

# --- CONFIGURATION (Must be the first Streamlit command) ---
st.set_page_config(page_title="Aeolianlux", page_icon="⚜️", layout="wide")

# --- 1. REMOVE FOOTER & 2. FIX TEXT COLOR ---
# We use 'unsafe_allow_html' to inject CSS that forces text to be readable
hide_styles = """
    <style>
    /* Hides the Streamlit Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Forces all standard text to be White/Light for readability on dark backgrounds */
    .stMarkdown, p, div {
        color: #E0E0E0 !important; /* Light Grey/White */
    }
    
    /* Optional: Makes the User Input text visible if that is also dark */
    .stTextInput input {
        color: #ffffff !important;
    }
    </style>
"""
st.markdown(hide_styles, unsafe_allow_html=True)

# --- 3. SESSION PRIVACY FIX ---
# Instead of loading data immediately, check if the user is 'new' to this session.
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest" # Default to Guest, not "Thejas 5"
    st.session_state.chat_history = []   # Start with an empty chat

# --- YOUR APP LOGIC STARTS HERE ---
# (Only show the specific user's name if they have actually logged in)

if st.session_state.user_name == "Guest":
    st.title("Welcome to Dubai Luxury Living")
    # You can add your Sidebar Lead Capture form here later
else:
    st.title(f"Welcome back, {st.session_state.user_name}")

# ... (Rest of your existing code) ...
