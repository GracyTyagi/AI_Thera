import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download necessary NLTK data (run once)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def get_sentiment(text):
    """
    Analyzes the sentiment of the given text using NLTK VADER.
    Returns: (Sentiment Category, Polarity Score)
    """
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)['compound']
    
    if score >= 0.05:
        return "Positive", score
    elif score <= -0.05:
        return "Negative", score
    else:
        return "Neutral", score

def get_recommendations(sentiment):
    """
    Provides personalized wellness recommendations based on detected sentiment.
    """
    recommendations = {
        "Positive": [
            "Keep up the great energy! Consider journaling what made you feel this way.",
            "Share your positivity with someone else today.",
            "Try a creative activity like painting or writing to channel this mood.",
            "Take a moment to practice gratitude for the good things in your life."
        ],
        "Neutral": [
            "A balanced day is a good day. Try a 5-minute mindfulness meditation.",
            "Take a short walk outside to refresh your mind.",
            "Listen to your favorite music or a calming podcast.",
            "Ensure you're staying hydrated and taking regular breaks."
        ],
        "Negative": [
            "It's okay to feel down. Try deep breathing exercises for 2 minutes.",
            "Reach out to a trusted friend or family member to talk.",
            "Engage in light physical exercise, like yoga or stretching.",
            "Prioritize rest today; your mental health comes first.",
            "Note: If you feel overwhelmed, consider speaking with a professional."
        ]
    }
    
    return recommendations.get(sentiment, ["Take care of yourself today."])
