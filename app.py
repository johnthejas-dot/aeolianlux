import streamlit as st
import datetime
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Aeolianlux | Dubai Luxury",
    page_icon="⚜️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRA-LUXURY VISUAL STYLE (CSS) ---
st.markdown("""
<style>
    /* 1. Main Background - Deep Dark Navy/Black */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* 2. HIDE STREAMLIT BRANDING (Footer & Menu) */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stDecoration"] {display:none !important;}
    [data-testid="stStatusWidget"] {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* 3. INPUT FIELDS (Visible Text) */
    .stTextInput input {
        color: #000000 !important; 
        background-color: #FFFFFF !important; 
        border: 1px solid #D4AF37 !important; 
        border-radius: 5px;
    }
    .stTextInput label {
        color: #D4AF37 !important; 
    }
    
    /* 4. THE BUTTON FIX (BULLETPROOF) */
    [data-testid="stFormSubmitButton"] > button {
        background-color: #D4AF37 !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFormSubmitButton"] > button p {
        color: #000000 !important; 
        font-weight: 900 !important;
        font-size: 18px !important;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #FFFFFF !important;
        border: 1px solid #D4AF37 !important;
    }
    [data-testid="stFormSubmitButton"] > button:hover p {
        color: #D4AF37 !important;
    }

    /* --- 5. CHAT MESSAGE FIX (READABILITY) --- */
    
    /* User Message Bubble (Dark Grey) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1E1E1E !important;
        border: 1px solid #333 !important;
    }
    
    /* AI Message Bubble (Dark Navy + Gold Border) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #161920 !important;
        border: 1px solid #D4AF37 !important;
    }
    
    /* *** CRITICAL FIX: FORCE TEXT TO BE WHITE *** */
    /* This targets the paragraphs (p) inside the chat bubbles */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] div {
        color: #E0E0E0 !important; /* Bright Grey/White */
        line-height: 1.6 !important;
    }
    
    /* Chat Input Box */
    .stChatInput textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. INITIALIZE CONNECTIONS ---
try:
    from openai import OpenAI
    from pinecone import Pinecone
    
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        client = None
        
    if "PINECONE_API_KEY" in st.secrets:
        pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
        index = pc.Index("aeolianlux-index")
    else:
        index = None
except Exception as e:
    client = None
    index = None

# --- 4. SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# --- 5. LEAD CAPTURE FORM ---
if st.session_state.user_info is None:
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>⚜️ Aeolianlux</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #BBBBBB;'>The Definition of Dubai Luxury.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("May we request the pleasure of your introduction to serve you better as you navigate the absolute pinnacle of Dubai luxury?")
    
    with st.form("lead_capture_form"):
        name = st.text_input("Full Name")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            country_code = st.text_input("Code", value="+971")
        with col2:
            mobile_number = st.text_input("Mobile Number")
            
        submitted = st.form_submit_button("ENTER CONCIERGE")
        
        if submitted and name and mobile_number:
            full_phone = f"{country_code} {mobile_number}"
            # You can uncomment this next line to debug in logs
            # print(f"NEW LEAD: {name} - {full_phone}")
            st.session_state.user_info = {"name": name, "phone": full_phone}
            st.rerun()
            
    st.stop()

# --- 6. MAIN CHAT INTERFACE ---
st.markdown(f"<h3 style='color: #D4AF37;'>⚜️ Welcome, {st.session_state.user_info['name']}</h3>", unsafe_allow_html=True)

for message in st.session_state.chat_history:
    role = message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])

user_input = st.chat_input("I am at your service. What do you wish to discover about Dubai Luxury Living?")

if user_input:
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # 2. Retrieve Knowledge
    knowledge = ""
    if client and index:
        try:
            xq = client.embeddings.create(input=user_input, model="text-embedding-3-small").data[0].embedding
            res = index.query(vector=xq, top_k=3, include_metadata=True)
            knowledge = "\n".join([match['metadata']['text'] for match in res['matches']])
        except Exception:
            knowledge = "Database not connected."

    # 3. Generate AI Response
    system_prompt = f"""
    You are Aeolianlux, Dubai's most elite digital concierge.
    User Name: {st.session_state.user_info['name']}
    Context from database: {knowledge}
    Tone Guidelines: Elegant, sophisticated, and warm.
    """

    if client:
        with st.chat_message("assistant"):
            response_stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )
            response_text = st.write_stream(response_stream)
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
    else:
        # Fallback response if no API key is present
        response_text = "The AI concierge is currently offline. Please check your API keys."
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
