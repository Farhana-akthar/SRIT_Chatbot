import streamlit as st
import pandas as pd
from fuzzywuzzy import process, fuzz

# -------------------------------
# Load FAQ data
# -------------------------------
faq_df = pd.read_csv("srit_faq.csv")

# -------------------------------
# Function to get answer
# -------------------------------
def get_answer(user_input):
    user_input = user_input.lower()
    questions = [q.lower() for q in faq_df['Question'].tolist()]
    best_match = process.extractOne(user_input, questions, scorer=fuzz.token_set_ratio)
    
    if best_match and best_match[1] > 70:
        # return the exact answer
        original_question = faq_df['Question'].iloc[questions.index(best_match[0])]
        return faq_df.loc[faq_df['Question'] == original_question, 'Answer'].values[0]
    else:
        return "Sorry, I don't know the answer. You can contact SRIT at www.srit.ac."

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="SRIT Help Chatbot", page_icon="🤖", layout="centered")

# Display logo
st.image("assets/logo.png", width=200)

st.title("🤖 SRIT Help Chatbot")
st.subheader("Welcome to Srinivasa Ramanujan Institute of Technology (SRIT) Help Assistant! 💬")
st.write("Ask me anything about SRIT — like faculty, courses, location, or facilities.")

# User input
user_input = st.text_input("Your Question:")

# Button to get answer
if st.button("Send"):
    if user_input.strip() != "":
        answer = get_answer(user_input)
        st.text_area("Answer:", value=answer, height=150)
    else:
        st.warning("Please type a question to get an answer.")



