import streamlit as st
import pandas as pd
from openai import OpenAI
from pinecone import Pinecone
import time

# 1. Config
st.set_page_config(page_title="Aeolianlux Brain Builder", page_icon="🧠")
st.title("🧠 Add NEW Knowledge to Brain")

# 2. Setup Connections
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
    index = pc.Index("aeolianlux-index")
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# 3. File Uploader
uploaded_file = st.file_uploader("Upload your 'Luxury Services' Excel file", type=['xlsx', 'csv'])

if uploaded_file is not None:
    st.info("File received. Processing...")
    
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write(f"Preview ({len(df)} rows):")
        st.dataframe(df.head())
        
        if st.button("Upload to Brain"):
            progress_bar = st.progress(0)
            
            vectors_to_upload = []
            
            for i, row in df.iterrows():
                # Combine columns into text
                # We assume columns are 'Topic' and 'Details'
                text_chunk = f"Topic: {row.iloc[0]} - Details: {row.iloc[1]}"
                
                try:
                    response = client.embeddings.create(
                        input=text_chunk,
                        model="text-embedding-3-small"
                    )
                    embedding = response.data[0].embedding
                    
                    # UNIQUE ID (Using timestamp to ensure we don't overwrite)
                    vectors_to_upload.append({
                        "id": f"update_{int(time.time())}_{i}", 
                        "values": embedding,
                        "metadata": {"text": text_chunk}
                    })
                    
                except Exception as e:
                    st.error(f"Error on row {i}: {e}")
                
                # Batch upload every 50 rows to keep it stable
                if len(vectors_to_upload) >= 50:
                    index.upsert(vectors=vectors_to_upload)
                    vectors_to_upload = [] # Reset list
                    
                progress_bar.progress((i + 1) / len(df))

            # Upload any remaining
            if vectors_to_upload:
                index.upsert(vectors=vectors_to_upload)
            
            st.success("✅ Success! New knowledge added.")
            st.balloons()
            
    except Exception as e:
        st.error(f"Error reading file: {e}")
