import streamlit as st
from openai import OpenAI
from pinecone import Pinecone
import re # Tool to find phone numbers

# 1. Config
st.set_page_config(page_title="Aeolianlux Luxury Living", page_icon="✨")
st.title("Dubai Luxury Living")
st.caption("Stay • Shop • Food")

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
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": "Hello! I can help you find Exotic Luxury places to stay, excellent restaurants, and where to buy Luxury special gifts. What are you looking for?"
    }]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 4. Input & Lead Capture Logic
if prompt := st.chat_input("Ask me about Dubai Luxury life..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # --- LEAD CAPTURE (New Feature) ---
    # This checks if the user typed something that looks like a phone number (digits > 7)
    if any(char.isdigit() for char in prompt):
        phone_pattern = re.search(r'\+?\d[\d -]{7,}\d', prompt)
        if phone_pattern:
            captured_number = phone_pattern.group()
            print(f"💰 LEAD CAPTURED: {captured_number} - Query: {prompt}") 
            # This 'print' saves it to your Streamlit App Logs (Manage App -> Logs)

    try:
        # A. Embed
        response = client.embeddings.create(input=prompt, model="text-embedding-3-small")
        query_vector = response.data[0].embedding

        # B. Search
        search_response = index.query(vector=query_vector, top_k=5, include_metadata=True)

        # C. Context
        context_text = ""
        for match in search_response['matches']:
            if 'text' in match['metadata']:
                context_text += match['metadata']['text'] + "\n---\n"

        # D. Answer
        my_email = "john.thejas@gmail.com"
        my_phone = "+918722232727"

        system_prompt = f"""You are a Luxury Concierge for Dubai.
        Context: {context_text}
        Official Contact: {my_email}, {my_phone}
        
        Instructions:
        1. Answer based on context.
        2. IF USER PROVIDES PHONE/EMAIL:
           - Acknowledge it warmly.
           - Provide YOUR Official Contact details immediately.
           - Say: "I have noted your interest. For immediate bespoke assistance, please reach out to our team at {my_phone}."
        """

        openai_response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        
        bot_reply = openai_response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

    except Exception as e:
        st.error(f"Error: {e}")
