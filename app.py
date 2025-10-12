import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz, process

# Load CSV data
data = pd.read_csv("srit_faq.csv")  # Make sure this file is in the same folder

# Function to get answer
def get_answer(user_input):
    user_input = user_input.lower()  # convert input to lowercase
    questions = [q.lower() for q in data['Question'].tolist()]  # lowercase all questions
    best_match = process.extractOne(user_input, questions, scorer=fuzz.token_set_ratio)
    
    if best_match[1] > 75:  # stricter similarity threshold
        # find the exact answer from original data
        original_question = data['Question'].iloc[questions.index(best_match[0])]
        return data.loc[data['Question'] == original_question, 'Answer'].values[0]
    else:
        return "Sorry, I don't know the answer. You can contact SRIT at www.srit.ac."

# Streamlit UI
st.set_page_config(page_title="SRIT Help Assist Chatbot", page_icon=":robot_face:")

# Optional logo
st.image("assets/srit_logo.png", width=200)

st.title("🤖 SRIT Help Assist Chatbot")
st.subheader("Ask me anything about SRIT")

user_input = st.text_input("Your Question:")
if st.button("Send"):
    answer = get_answer(user_input)
    st.text_area("Answer:", value=answer, height=150)
