import streamlit as st

# --- 1. CUSTOMIZE YOUR BOOKMARK HERE ---
st.set_page_config(
    page_title="Aeolianlux | Dubai Luxury",  # <--- This is the Bookmark Text
    page_icon="⚜️",                          # <--- This is the Bookmark Icon
    layout="wide"
)

# --- 2. CUSTOM CSS: FORCE DARK THEME & HIDE FOOTER ---
st.markdown("""
    <style>
    /* Force the main app background to be Dark Navy/Black */
    .stApp {
        background-color: #0E1117;
    }

    /* Force all text to be White or Gold */
    h1, h2, h3 {
        color: #D4AF37 !important; /* Metallic Gold for Titles */
    }
    p, div, label, span {
        color: #FAFAFA !important; /* Bright White for normal text */
    }
    
    /* Hide the Streamlit Red Balloon & Footer */
    footer {visibility: hidden;} 
    header {visibility: hidden;} 
    .stDeployButton {display:none;} 
    
    /* Make Input boxes readable (Dark Grey background, White text) */
    .stTextInput input {
        color: #ffffff !important;
        background-color: #262730 !important;
        border: 1px solid #D4AF37; /* Optional: Gold Border */
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION PRIVACY FIX (Stops "Thejas 5" from appearing) ---
# This ensures every new visitor starts as a "Guest"
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- 4. YOUR MAIN APP CONTENT ---
if st.session_state.user_name == "Guest":
    st.title("Welcome to Dubai Luxury Living")
    st.write("Experience the finest places to stay, shop, and dine.")
else:
    st.title(f"Welcome back, {st.session_state.user_name}")

# (Paste the rest of your logic/AI code here)
# IMPORTANT: Make sure you DELETED the old line that looked like:
# user = df.iloc[-1]['name']  <--- DELETE THIS LINE IF YOU SEE IT
