import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Mind Jungle 🌿")
st.write("Welcome to your personal journal summarizer! This tool helps you reflect on your thoughts and feelings by summarizing the word jungles you create in your journal entries. Say whatever you want, I'll keep your secrets safe 😉")

entry = st.text_area("***What's on your mind?***", height=300, placeholder="Type something, anything...")

if st.button("Analyze my thoughts"):
    if entry.strip() == "":
        st.warning("You didn't write anything!")
    else:
        with st.spinner("Untangling your jungle..."):
            message = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": f"Here is my journal entry: {entry}"}
                ]
            )
            st.write(message.choices[0].message.content)