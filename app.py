import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# 1. Config
st.set_page_config(page_title="Aeolianlux AI", page_icon="🤖")
st.title("Aeolianlux Intelligence (Debug Mode)")

# 2. Connect
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
    index = pc.Index("aeolianlux-index") 
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# 3. Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Ask me a question, and I will show you what I find in the database."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 4. Input
if prompt := st.chat_input("Ask about a specific client or job..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # A. Embed
        response = client.embeddings.create(
            input=prompt,
            model="text-embedding-3-small"
        )
        query_vector = response.data[0].embedding

        # B. Search
        search_response = index.query(
            vector=query_vector,
            top_k=5, 
            include_metadata=True
        )

        # --- DEBUG SECTION START ---
        # This creates a clickable box to see the raw data
        with st.expander("🕵️ Debug: View Raw Database Matches"):
            st.write(search_response)
        # --- DEBUG SECTION END ---

        # C. Context
        context_text = ""
        for match in search_response['matches']:
            if 'text' in match['metadata']:
                context_text += match['metadata']['text'] + "\n---\n"

        # D. Answer
        system_prompt = f"""You are a helpful assistant. 
        Here is the data found in the database:
        {context_text}
        
        Question: {prompt}
        
        If the data above contains the answer, answer politely.
        If the data is empty or irrelevant, tell the user exactly what you found (or didn't find).
        """

        openai_response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        bot_reply = openai_response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

    except Exception as e:
        st.error(f"Error: {e}")
