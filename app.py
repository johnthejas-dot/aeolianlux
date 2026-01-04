import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Aeolianlux | Dubai Luxury",
    page_icon="⚜️",
    layout="wide"
)

# --- 2. CUSTOM CSS (STYLING) ---
st.markdown("""
    <style>
    /* MAIN BACKGROUND - Deep Luxury Black */
    .stApp {
        background-color: #0E1117;
    }

    /* TEXT COLORS */
    h1, h2, h3 {
        color: #D4AF37 !important; /* Gold Titles */
    }
    p, div, span, label {
        color: #FAFAFA !important; /* White Text */
    }

    /* HIDE FOOTER & STREAMLIT BRANDING */
    footer {display: none !important;}
    header {visibility: hidden;}
    div[data-testid="stDecoration"] {display:none;}

    /* INPUT BOX STYLING (Make them visible!) */
    .stTextInput input, .stChatInput textarea {
        color: #000000 !important; /* Black Text when typing */
        background-color: #FFFFFF !important; /* White Background */
        border: 2px solid #D4AF37 !important; /* Gold Border */
        border-radius: 10px;
    }
    
    /* FIX FOR CHAT MESSAGES */
    div[data-testid="stChatMessage"] {
        background-color: #1E1E1E; /* Dark Grey Message Bubble */
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE (Memory) ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SIDEBAR (Lead Capture) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5968/5968260.png", width=50) # Placeholder Logo
    st.header("Concierge Service")
    st.write("Need personalized assistance?")
    contact_email = st.text_input("Your Email (for updates)")
    if st.button("Subscribe"):
        st.success("Thank you! We will be in touch.")

# --- 5. MAIN APP INTERFACE ---
if st.session_state.user_name == "Guest":
    st.title("Welcome to Dubai Luxury Living")
    st.write("Experience the finest places to stay, shop, and dine.")
else:
    st.title(f"Welcome back, {st.session_state.user_name}")

# --- 6. CHAT INTERFACE (The Missing Part!) ---
# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# The Input Box (This is what was missing)
if prompt := st.chat_input("Ask me about Dubai Luxury life..."):
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Show AI Response (Placeholder logic)
    # *Note: Paste your original AI response logic here later*
    response = f"You asked about: {prompt}. (AI is processing...)"
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
