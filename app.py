import streamlit as st
import pandas as pd
from openai import OpenAI
from pinecone import Pinecone
import time

# 1. Config
st.set_page_config(page_title="Aeolianlux Brain Builder", page_icon="🧠")
st.title("🧠 Upload Data to Aeolianlux Memory")

# 2. Setup Connections
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
    index = pc.Index("aeolianlux-index")
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# 3. File Uploader
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    st.info("File received. Processing...")
    
    # Read the file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write(f"Preview of data ({len(df)} rows found):")
        st.dataframe(df.head())
        
        if st.button("Start Uploading to Brain"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Loop through data
            vectors_to_upload = []
            
            for i, row in df.iterrows():
                # Convert row to a single string of text
                # We combine all columns so the AI knows everything in the row
                text_chunk = f"Info: {row.to_string(index=False)}"
                
                # Create Embedding
                try:
                    response = client.embeddings.create(
                        input=text_chunk,
                        model="text-embedding-3-small"
                    )
                    embedding = response.data[0].embedding
                    
                    # Prepare for Pinecone (ID, Vector, Metadata)
                    # We store the text in metadata so the AI can read it later
                    vectors_to_upload.append({
                        "id": f"row_{i}",
                        "values": embedding,
                        "metadata": {"text": text_chunk}
                    })
                    
                except Exception as e:
                    st.error(f"Error on row {i}: {e}")
                
                # Update Progress
                status_text.text(f"Processed row {i+1}/{len(df)}")
                progress_bar.progress((i + 1) / len(df))
                
                # Upload in batches of 50 to be safe
                if len(vectors_to_upload) >= 50:
                    index.upsert(vectors=vectors_to_upload)
                    vectors_to_upload = [] # Reset batch
                    time.sleep(0.5) # Be gentle on the connection

            # Upload remaining rows
            if vectors_to_upload:
                index.upsert(vectors=vectors_to_upload)
            
            st.success("✅ Success! Your data is now inside the Pinecone Brain.")
            st.balloons()
            
    except Exception as e:
        st.error(f"Error reading file: {e}")
