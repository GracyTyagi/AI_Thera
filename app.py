import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
from database import create_usertable, create_moodtable, add_userdata, login_user, add_mooddata, get_user_moods
from engine import get_sentiment, get_recommendations

# Page Configuration
st.set_page_config(
    page_title="AI Thera - Mental Wellness Platform",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS for a Minimalist, Open Layout
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    /* Header & Typography */
    .wellness-header {
        color: #2e7d32;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        margin-bottom: 30px;
    }
    .section-title {
        color: #388e3c;
        font-weight: 600;
        font-size: 1.5rem;
        margin-bottom: 10px;
        border-bottom: 2px solid #e8f5e9;
        padding-bottom: 5px;
    }
    
    /* Breathing Bubble Animation (Refined) */
    @keyframes breathe {
        0% { transform: scale(1); background-color: #c8e6c9; }
        50% { transform: scale(1.3); background-color: #a5d6a7; }
        100% { transform: scale(1); background-color: #c8e6c9; }
    }
    .breathing-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        margin-top: 20px;
    }
    .bubble {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        animation: breathe 8s infinite ease-in-out;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #2e7d32;
        font-weight: 600;
        text-align: center;
        border: 2px solid #81c784;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #f1f8e9;
        color: #2e7d32;
        border: 1px solid #c8e6c9;
        height: 3em;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #2e7d32;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Initialize Database
    create_usertable()
    create_moodtable()

    st.markdown("<h1 class='wellness-header'>🌿 AI Thera</h1>", unsafe_allow_html=True)
    
    # Initialize Session State
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ""
    if 'page' not in st.session_state:
        st.session_state['page'] = "Home"

    # --- PERSISTENT HEADER NAVIGATION ---
    cols = st.columns([1, 1, 1, 1, 1, 1])
    nav_items = ["Home", "Login", "Register", "Mood Tracker", "Dashboard", "Wellness Hub"]
    icons = ["🏠", "🔑", "📝", "📊", "📈", "💡"]
    
    for i, item in enumerate(nav_items):
        with cols[i]:
            if st.button(f"{icons[i]} {item}"):
                st.session_state['page'] = item
                st.rerun()
    
    st.divider()

    # Sidebar - Logout only
    if st.session_state['logged_in']:
        st.sidebar.success(f"User: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.session_state['page'] = "Home"
            st.rerun()

    # Page Routing
    if st.session_state['page'] == "Home":
        # Hero Section
        st.markdown("<h2 style='text-align: center; color: #555;'>How can we help you today?</h2>", unsafe_allow_html=True)
        
        # Open Grid Layout (No Cards)
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("<p class='section-title'>🧘‍♂️ Breathe</p>", unsafe_allow_html=True)
            st.write("Take a moment for yourself. Inhale deeply.")
            st.markdown("""
                <div class='breathing-container'>
                    <div class='bubble'>Relax</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<p class='section-title'>🎭 Mood Log</p>", unsafe_allow_html=True)
            st.write("One-tap mood log:")
            if st.session_state['logged_in']:
                m_cols = st.columns(3)
                moods = [("😊", "Happy", 0.9), ("😐", "Neutral", 0.0), ("😔", "Sad", -0.7), ("😡", "Angry", -0.9), ("😴", "Tired", -0.2)]
                for i, (emoji, name, score) in enumerate(moods):
                    if st.button(f"{emoji} {name}", key=f"mood_{i}"):
                        add_mooddata(st.session_state['username'], f"Quick Log: {name}", name, score)
                        st.session_state['msg'] = f"Logged: {name} {emoji}"
                        if score > 0: st.balloons()
                if 'msg' in st.session_state:
                    st.success(st.session_state['msg'])
            else:
                st.info("Log in to track mood.")

        with col3:
            st.markdown("<p class='section-title'>🎯 Checklist</p>", unsafe_allow_html=True)
            w1 = st.checkbox("Hydration 💧")
            w2 = st.checkbox("Exercise 🏃")
            w3 = st.checkbox("Kindness 😊")
            w4 = st.checkbox("Deep Breath 🌬️")
            if w1 and w2 and w3 and w4:
                st.success("Great job! ⭐")
                st.balloons()
        
        st.divider()
        
        # Daily Quote Section at the bottom
        quotes = [
            "Your mental health is a priority.",
            "Self-care is how you take your power back.",
            "Every day is a fresh start.",
            "One small positive thought can change your whole day."
        ]
        st.markdown(f"<p style='text-align: center; font-style: italic; color: #888;'>\"{random.choice(quotes)}\"</p>", unsafe_allow_html=True)

    elif st.session_state['page'] == "Login":
        st.subheader("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Sign In"):
            result = login_user(username, password)
            if result:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['page'] = "Home"
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    elif st.session_state['page'] == "Register":
        st.subheader("📝 Register")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Sign Up"):
            if add_userdata(new_user, new_password):
                st.success("Account created!")
            else:
                st.error("User exists.")

    elif st.session_state['page'] == "Mood Tracker":
        if st.session_state['logged_in']:
            st.subheader(f"📊 Mood Tracker - {st.session_state['username']}")
            mood_text = st.text_area("What's on your mind?", height=150)
            if st.button("Analyze & Save"):
                if mood_text:
                    sentiment, score = get_sentiment(mood_text)
                    add_mooddata(st.session_state['username'], mood_text, sentiment, score)
                    st.write(f"### Mood: {sentiment}")
                    if sentiment == "Positive": st.balloons()
                else: st.error("Please write something.")
        else: st.warning("Login first.")

    elif st.session_state['page'] == "Dashboard":
        if st.session_state['logged_in']:
            st.subheader("📈 Dashboard")
            data = get_user_moods(st.session_state['username'])
            if data:
                df = pd.DataFrame(data, columns=['Mood Entry', 'Sentiment', 'Score', 'Timestamp'])
                st.dataframe(df)
                fig = px.line(df, x='Timestamp', y='Score', markers=True)
                st.plotly_chart(fig, use_container_width=True)
            else: st.info("No data.")
        else: st.warning("Login first.")

    elif st.session_state['page'] == "Wellness Hub":
        if st.session_state['logged_in']:
            st.subheader("💡 Wellness Hub")
            data = get_user_moods(st.session_state['username'])
            if data:
                latest = data[0][1]
                st.write(f"Recommended for **{latest}** mood:")
                for r in get_recommendations(latest):
                    st.info(f"💡 {r}")
            else: st.info("No logs.")
        else: st.warning("Login first.")

if __name__ == '__main__':
    main()
