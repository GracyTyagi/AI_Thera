# 🌿 AI Thera: Mental Wellness Platform

AI Thera is a professional, AI-powered mental wellness platform built with Python and Streamlit. It allows users to track their daily moods, analyze sentiments using NLP, and receive personalized wellness recommendations based on their emotional state.

## 🚀 Features
- **User Authentication:** Secure registration and login system with password hashing.
- **Mood Tracker:** Input your daily thoughts and get real-time AI sentiment analysis (Positive, Neutral, Negative).
- **Personalized Recommendations:** Dynamic wellness tips tailored to your current mood.
- **Analytics Dashboard:**
    - Sentiment trend line charts (using Plotly).
    - Mood distribution pie charts.
    - Historical logs of all mood entries.
- **SQLite Integration:** All data is stored locally in a `wellness.db` database.

## 📁 Project Structure
```text
ai_thera/
├── app.py              # Main UI and Routing (Streamlit)
├── database.py         # SQLite Schema and User/Mood management
├── engine.py           # NLP Sentiment Analysis and Recommendation logic
├── requirements.txt    # List of dependencies
└── README.md           # Project Documentation
```

## 🛠️ Installation Guide

1. **Clone or Navigate to the project folder:**
   ```bash
   cd ai_thera
   ```

2. **Install Dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## 🧠 How it Works
- **Sentiment Analysis:** The platform uses the NLTK VADER (Valence Aware Dictionary and sEntiment Reasoner) model to analyze the emotional tone of your text input.
- **Recommendations:** Based on the sentiment score, the system provides curated advice, ranging from mindfulness exercises for neutral moods to encouragement for positive ones and support tips for negative ones.

## 📝 Technologies Used
- **Frontend:** Streamlit
- **Data Handling:** Pandas
- **Visualization:** Plotly
- **NLP Engine:** NLTK
- **Database:** SQLite3

---
*Built with ❤️ to support mental health awareness.*
