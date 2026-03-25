import streamlit as st
from groq import Groq
from supabase import create_client
from dotenv import load_dotenv
import os
import re

load_dotenv()

def apply_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

        /* ── Base ── */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #F5F0E8;
            color: #2C1810;
            font-family: 'DM Sans', sans-serif;
        }

        [data-testid="stAppViewContainer"] > .main {
            background-color: #F5F0E8;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: #EDE5D8;
            border-right: 1px solid #D4C4A8;
        }

        [data-testid="stSidebar"] * {
            color: #2C1810 !important;
        }

        /* ── Title & Headers ── */
        h1 {
            font-family: 'Lora', serif !important;
            color: #2C1810 !important;
            font-weight: 600 !important;
        }

        h2, h3 {
            font-family: 'Lora', serif !important;
            color: #3D2314 !important;
        }

        /* ── Text area ── */
        [data-testid="stTextArea"] textarea {
            background-color: #FDF8F2 !important;
            border: 1px solid #D4C4A8 !important;
            border-radius: 8px !important;
            color: #2C1810 !important;
            font-family: 'DM Sans', sans-serif !important;
        }

        [data-testid="stTextArea"] textarea:focus {
            border-color: #C4784A !important;
            box-shadow: 0 0 0 2px #C4784A22 !important;
        }

        /* ── Buttons ── */
        [data-testid="stButton"] button {
            background-color: #C4784A !important;
            color: #FDF8F2 !important;
            border: none !important;
            border-radius: 8px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 500 !important;
            padding: 0.5rem 1.5rem !important;
            transition: background-color 0.2s ease !important;
        }

        [data-testid="stButton"] button:hover {
            background-color: #A85E35 !important;
        }

        /* ── Metrics ── */
        [data-testid="stMetric"] {
            background-color: #EDE5D8 !important;
            border-radius: 10px !important;
            padding: 16px !important;
            border: 1px solid #D4C4A8 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #7A5C4A !important;
        }

        [data-testid="stMetricValue"] {
            color: #2C1810 !important;
        }

        /* ── Tabs ── */
        [data-testid="stTabs"] [data-baseweb="tab"] {
            font-family: 'DM Sans', sans-serif !important;
            color: #7A5C4A !important;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            color: #C4784A !important;
            border-bottom-color: #C4784A !important;
        }

        /* ── Radio ── */
        [data-testid="stRadio"] label {
            color: #2C1810 !important;
        }

        /* ── Spinner ── */
        [data-testid="stSpinner"] {
            color: #C4784A !important;
        }

        /* ── Input fields ── */
        [data-testid="stTextInput"] input {
            background-color: #FDF8F2 !important;
            border: 1px solid #D4C4A8 !important;
            border-radius: 8px !important;
            color: #2C1810 !important;
        }

        /* ── Divider ── */
        hr {
            border-color: #D4C4A8 !important;
        }

        /* ── Warning/Success/Info ── */
        [data-testid="stAlert"] {
            border-radius: 8px !important;
        }

        /* ── Dataframe ── */
        [data-testid="stDataFrame"] {
            border-radius: 8px !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #EDE5D8;
        }
        ::-webkit-scrollbar-thumb {
            background: #C4784A;
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

apply_theme()

# loading screen
def show_splash():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');
        
        .splash-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
            font-family: 'Lora', serif;
        }
        
        @keyframes jump {
            from { transform: translateY(0px); }
            to { transform: translateY(-30px); }
        }
        
        @keyframes walk {
            from { margin-left: -300px; opacity: 0; }
            to { margin-left: 300px; opacity: 1; }
        }

        .splash-title {
            font-size: 48px;
            color: #2C1810;
            margin-top: 24px;
            animation: fadeIn 1s ease-in 0.5s forwards;
            opacity: 0;
        }

        .splash-subtitle {
            font-size: 18px;
            color: #7A5C4A;
            margin-top: 8px;
            animation: fadeIn 1s ease-in 1s forwards;
            opacity: 0;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0px); }
        }
        </style>

        <div class="splash-container">
            <div class="splash-title">Mind Jungle 🌿</div>
            <div class="splash-subtitle">loading your space to think...</div>
        </div>
    """, unsafe_allow_html=True)
    
    import time
    time.sleep(3)
    st.session_state.splash_done = True
    st.rerun()

# ─────────────────────────────────────────
# AUTH FUNCTIONS
# ─────────────────────────────────────────

def sign_up(email, password, username):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            supabase.table("profiles").insert({
                "id": res.user.id,
                "username": username
            }).execute()
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        # set session so the RLS works
        supabase.auth.set_session(res.session.access_token, res.session.refresh_token)
        username = get_username(res.user.id)
        return res.user, res.session, username, None
    except Exception as e:
        return None, None, None, str(e)

def sign_out():
    supabase.auth.sign_out()
    st.session_state.clear()

def get_username(user_id):
    try:
        res = supabase.table("profiles").select("username").eq("id", user_id).execute()
        if res.data:
            return res.data[0]["username"]
    except:
        pass
    return "friend"

# ─────────────────────────────────────────
# DATABASE FUNCTIONS
# ─────────────────────────────────────────

def save_mood(user_id, score, themes):
    supabase.table("mood_entries").insert({
        "user_id": user_id,
        "score": score,
        "themes": themes
    }).execute()

def get_mood_history(user_id):
    res = supabase.table("mood_entries").select("*").eq("user_id", user_id).order("created_at").execute()
    return res.data

# ─────────────────────────────────────────
# LOGIN / SIGNUP PAGE
# ─────────────────────────────────────────

def show_auth_page():
    st.title("Mind Jungle 🌿")
    st.write("Hello there! Please log in or sign up to continue.")

    tab1, tab2 = st.tabs(["Log In", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In"):
            user, session, username, error = sign_in(email, password)
            if error:
                st.error(f"Login failed: {error}")
            else:
                st.session_state.user = user
                st.session_state.session = session
                st.session_state.username = username
                st.rerun()

    with tab2:
        username = st.text_input("What should I call you?", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if username.strip() == "":
            st.warning("Please enter a name!")
        else:
            user, error = sign_up(email, password, username)
            if error:
                st.error(f"Sign up failed: {error}")
            else:
                st.success("Account created! Please log in.")

# ─────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────

def show_main_app():
    user = st.session_state.user

    # Sidebar
    with st.sidebar:
        username = st.session_state.get("username", "friend")
        st.markdown(f"<h3 style='color: #2C1810;'>What's up, <strong>{username}</strong> 👋</h3>", unsafe_allow_html=True)
        if st.button("Log Out"):
            sign_out()
            st.rerun()
        st.markdown("---")
        page = st.radio("Navigate", ["📝 Journal", "📊 My Mood History"])

    if page == "📝 Journal":
        show_journal_page(user)
    else:
        show_dashboard_page(user)

# ─────────────────────────────────────────
# JOURNAL PAGE
# ─────────────────────────────────────────

def show_journal_page(user):
    st.title("Mind Jungle 🌿")
    st.write("Welcome to your personal journal summarizer! This tool helps you reflect on your thoughts and feelings by summarizing the word jungles you create in your journal entries. Say whatever you want, I'll keep your secrets safe 😉")

    # Journal prompt generator
    if "journal_prompt" not in st.session_state:
        st.session_state.journal_prompt = None

    if st.button("✨ Give me a prompt"):
        with st.spinner("Finding a prompt for you..."):
            prompt_message = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=100,
                messages=[
                    {
                        "role": "system",
                        "content": "You generate single, thoughtful journaling prompts. Return ONLY the prompt itself — no intro, no quotes, no extra text. Make it specific, introspective, and warm. Vary the topics: relationships, memories, emotions, dreams, gratitude, fears, growth, daily life."
                    },
                    {
                        "role": "user",
                        "content": "Give me a journaling prompt."
                    }
                ]
            )
            st.session_state.journal_prompt = prompt_message.choices[0].message.content.strip()

    if st.session_state.journal_prompt:
        st.markdown(
            f"""
            <div style="background-color: #FDF3E7; border-left: 4px solid #C4784A; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px; color: #333;">
                💭 <em>{st.session_state.journal_prompt}</em>
            </div>
            """,
            unsafe_allow_html=True
        )

    entry = st.text_area("***What's on your mind?***", height=300, placeholder="Type something, anything...")

    if st.button("Analyze my thoughts"):
        if entry.strip() == "":
            st.warning("You didn't write anything!")
        else:
            with st.spinner("Untangling your jungle..."):
                message = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a compassionate journal analyzer. When given a journal entry, respond ONLY in this exact format with no extra text:

SCORE: [a single number from 1 to 10 representing emotional heaviness, where 1 is very light and positive, 10 is very heavy and distressed]

**THEMES 🤔**
[2-4 key themes, comma separated]

**EMOTIONAL TONE 😁 😢**
[1-2 sentences describing the emotional tone, nuanced and specific]

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

                # parse score
                score_match = re.search(r"SCORE:\s*(\d+)", response)
                score = int(score_match.group(1)) if score_match else 5
                score = max(1, min(10, score))
                position = (1 - (score - 1) / 9) * 100

                # save to database
                themes_match = re.search(r"THEMES.*?\n(.+)", response)
                themes = themes_match.group(1).strip() if themes_match else ""
                save_mood(user.id, score, themes)

                # mood meter
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

                analysis = re.sub(r"SCORE:\s*\d+\n?", "", response).strip()
                
            st.markdown(analysis)

# ─────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────

def show_dashboard_page(user):
    st.title("📊 My Mood History")
    
    entries = get_mood_history(user.id)
    
    if not entries:
        st.info("No entries yet! Go write something in your journal :)")
        return

    import pandas as pd
    import altair as alt

    df = pd.DataFrame(entries)
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")
    df = df.groupby("created_at").agg({"score": "mean", "themes": "first"}).reset_index()

    # -- Fun stats --
    total = len(df)
    avg_score = df["score"].mean()
    best_day = df.loc[df["score"].idxmin(), "created_at"]
    hardest_day = df.loc[df["score"].idxmax(), "created_at"]

    # most recurring theme
    all_themes = ", ".join(df["themes"].dropna().tolist()).lower()
    theme_words = [t.strip() for t in all_themes.split(",") if t.strip()]
    from collections import Counter
    theme_counts = Counter(theme_words)
    top_theme = theme_counts.most_common(1)[0][0].title() if theme_counts else "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("📝 Total Entries", total)
    col2.metric("🤩 Best Day", str(best_day))
    col3.metric("😞 Worst Day", str(hardest_day))

    st.markdown("---")

    # -- LLAMA Narrative --
    st.subheader("A little insight for you...")
    if st.button("Tell me what's going on"):
        with st.spinner("Reflecting on your journey..."):
            history_summary = "\n".join([
                f"{row['created_at']} - Score: {row['score']}/10, Themes: {row['themes']}"
                for _, row in df.iterrows()
            ])
            narrative = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=300,
                messages=[
                    {
                        "role": "system",
                        "content": "You're a compassionate mood analyst. Given a person's journal mood history (dates, heaviness, and themes), write an objective, personal 3-4 sentence narrative that reflects on their emotional journey. Notice patterns, highlight progress, acknowledge hard days. Speak directly to the user, don't be generic or robotic."
                    },
                    {
                        "role": "user",
                        "content": f"Here's what's been going on:\n{history_summary}"
                    }
                ]
            )
            st.markdown(
                f"""
                <div style="background-color: #FDF3E7; border-left: 4px solid #C4784A; padding: 16px; border-radius: 6px; color: #333;">
                    💭{narrative.choices[0].message.content.strip()}
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown("---")

    # -- Mood Chart --
    st.subheader("Mood Over Time")
    chart = alt.Chart(df).mark_line(
        color="#C4784A",
        point=alt.OverlayMarkDef(color="#C4784A", filled=True, size=80)
    ).encode(
        x=alt.X("created_at:T", title="Date", axis=alt.Axis(format="%b %d", labelAngle=-45)),
        y=alt.Y("score:Q", scale=alt.Scale(domain=[1,10]), axis=alt.Axis(tickMinStep=1), title="Heaviness Score"),
        tooltip=["created_at:T", "score:Q", "themes:N"]
    ).properties(
        height=500,
        background="#F5F0E8"
    ).configure_axis(
        gridColor="#D4C4A8",
        labelColor="#7A5C4A",
        titleColor="#7A5C4A"
    ).configure_view(
        stroke="#D4C4A8"
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")

    # -- Raw Data --
    with st.expander("📘 See all entries"):
        st.dataframe(
            df[["created_at", "score", "themes"]].sort_values("created_at", ascending=False),
            use_container_width=True
        )

# ─────────────────────────────────────────
# APP ENTRY POINT
# ─────────────────────────────────────────

if "splash_done" not in st.session_state:
    show_splash()
elif "user" not in st.session_state:
    show_auth_page()
else: 
    session = st.session_state.session
    supabase.auth.set_session(session.access_token, session.refresh_token)
    show_main_app()