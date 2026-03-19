import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import re

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
                    {
                        "role": "system",
                        "content": """You are a compassionate journal analyzer. When given a journal entry, respond ONLY in this exact format with no extra text:

SCORE: [a single number from 1 to 10 representing emotional heaviness of the entry, where 1 is very light and positive, 10 is very heavy and distressed]

**THEMES 🤔**
[2-4 key themes, comma separated]

**EMOTIONAL TONE 😁 😢**
[2-3 sentences describing the emotional tone, nuanced and specific]

**SUMMARY 🎯**
[2-3 sentences capturing the heart of the entry. Address the user directly]

**GENTLE REFRAME 🫶**
[One grounding, compassionate observation. Not toxic positivity, just honest and kind. Don't sound like a robot]"""
                    },
                    {
                        "role": "user",
                        "content": f"Here is my journal entry: {entry}"
                    }
                ]
            )
            response = message.choices[0].message.content

            # parse score from the first line
            score_match = re.search(r"SCORE:\s*(\d+)", response)
            score = int(score_match.group(1))
            # limit between 1 and 10
            score = max(1, min(10, score))
            # convert score to percentage (1=0%, 10=100%)
            position = (1 - (score - 1) / 9) * 100

            st.markdown(
                f"""
                <style>
                .meter-container {{
                    position: relative;
                    margin: 20px 0;
                }}
                .meter-bar {{
                    height: 16px;
                    border-radius: 8px;
                    background: linear-gradient(to right, #F44336, #FF9800, #FFEB3B, #4CAF50);
                    position: relative;
                }}
                .meter-indicator {{
                    width: 24px;
                    height: 24px;
                    background: white;
                    border: 3px solid #333;
                    border-radius: 50%;
                    position: absolute;
                    top: -4px;
                    animation: slideIn 1s ease-out forwards;
                    left: 0%;
                }}
                @keyframes slideIn {{
                    from {{ left: 50%; }}
                    to {{ left: calc({position}% - 12px); }}
                }}
                .meter-labels {{
                    display: flex;
                    justify-content: space-between;
                    font-size: 12px;
                    color: #888;
                    margin-top: 6px;
                }}
                </style>
                <div class="meter-container">
                    <p style="margin-bottom: 8px;"><strong>Emotional Heaviness</strong></p>
                    <div class="meter-bar">
                        <div class="meter-indicator"></div>
                    </div>
                    <div class="meter-labels">
                        <span>😔 Heavy</span>
                        <span>😊 Light</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("---")

            # strip score line and show analysis
            analysis = re.sub(r"SCORE:\s*\d+\n?", "", response).strip()
            st.markdown(analysis)