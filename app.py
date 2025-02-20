import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
client = openai.Client(api_key=OPENAI_API_KEY)


def detect_intent(user_input):
    """ Determine if the input is a medical term, a greeting, or random text. """

    prompt = f"""
    Classify the user input: '{user_input}' into one of these categories:
    1. Medical Term - If it's a valid medical term like 'Hypertension' or 'MRI'.
    2. Thank You - If the user is expressing gratitude (e.g., 'Thanks', 'Thank you').
    3. Greeting - If it's a greeting like 'Hello', 'Hi', 'Hey'.
    4. Random - If it’s completely unrelated (e.g., 'Pizza', 'Car').

    Respond with ONLY the category name: 'Medical Term', 'Thank You', 'Greeting', or 'Random'.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    category = response.choices[0].message.content.strip()
    return category


def explain_medical_term(term):
    """ Fetches a simple explanation for a medical term. """

    prompt = f"""
    Explain the medical term '{term}' in a way that a 14-year-old can easily understand.
    Keep it simple and avoid difficult medical words.
    Focus on what it means, why it happens, and how it affects a person.
    Use relatable examples if possible. Make sure the explanation is clear and reassuring.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a friendly medical assistant who explains medical terms simply and calmly."},
            {"role": "user", "content": prompt}
        ]
    )

    explanation = response.choices[0].message.content
    return explanation


# ------------------------ Streamlit UI ------------------------

st.title("🩺 Medical Terminology Explainer")
st.write("Enter a medical term, and I'll explain it in simple words. 😊")

# User input field
user_input = st.text_input("Enter a medical term or message:")

if user_input:
    category = detect_intent(user_input)

    if category == "Medical Term":
        explanation = explain_medical_term(user_input)
        st.success(f"**🤖 AI says:** {explanation}")
    elif category == "Thank You":
        st.info("You're welcome! 😊 I'm happy to help!")
    elif category == "Greeting":
        st.info("Hello! 👋 How can I assist you today?")
    else:
        st.warning("Hmm, that doesn't seem like a medical term. Try asking about a health-related topic! 😊")
