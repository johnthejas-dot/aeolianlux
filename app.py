import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# 1. Page Configuration
st.set_page_config(page_title="Aeolianlux AI", page_icon="🤖")
st.title("Aeolianlux Intelligence")
st.caption("Ask me about UAE Jobs, International Clients, or Consulting.")

# 2. Connect to the "Fuel" (API Keys)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
    index = pc.Index("aeolianlux-index") 
except Exception as e:
    st.error(f"Connection Error: {e}. Did you set up the secrets?")
    st.stop()

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I am ready to help. Ask me anything about our database."}]

# 4. Display Chat History
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 5. Handle User Input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # --- THE BRAIN LOGIC ---
    try:
        # A. Convert user question to numbers
        response = client.embeddings.create(
            input=prompt,
            model="text-embedding-3-small"
        )
        query_vector = response.data[0].embedding

        # B. Search Pinecone for similar info
        search_response = index.query(
            vector=query_vector,
            top_k=5, # Get top 5 best matches
            include_metadata=True
        )

        # C. Construct the Context
        context_text = ""
        for match in search_response['matches']:
            if 'text' in match['metadata']:
                context_text += match['metadata']['text'] + "\n---\n"

        # D. Send to OpenAI
        system_prompt = f"""You are a helpful assistant for Aeolianlux. 
        Answer based ONLY on the following Context. 
        If the answer is not in the context, say "I don't have that information in my records, but I can connect you to the owner."
        
        Context:
        {context_text}
        """

        openai_response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        bot_reply = openai_response.choices[0].message.content
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

    except Exception as e:
        st.error(f"An error occurred: {e}")
