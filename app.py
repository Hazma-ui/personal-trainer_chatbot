import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    st.error("Cohere API key not found. Set COHERE_API_KEY in your .env file.")
    st.stop()

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Initialize Session State
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# UI Title
st.title("Personal Trainer Chatbot")

# ================= USER FORM =================
if st.session_state.user_data is None:
    with st.form("user_info_form"):
        st.header("Tell me about yourself:")
        name = st.text_input("What is your name?")
        age = st.number_input("What is your age?", 10, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", 30, 300, 70)
        height = st.number_input("Height (cm)", 100, 250, 170)
        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
        )
        goal = st.selectbox(
            "Goal",
            ["Lose Weight", "Gain Muscle", "Improve Endurance", "Stay Healthy"]
        )

        submit = st.form_submit_button("Generate Plan")

    if submit:
        st.session_state.user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "activity_level": activity_level,
            "goal": goal,
        }

        prompt = f"""
You are a professional fitness trainer.

Create a realistic weekly fitness plan based on:

Name: {name}
Age: {age}
Gender: {gender}
Weight: {weight} kg
Height: {height} cm
Activity Level: {activity_level}
Goal: {goal}
"""

        with st.spinner("Generating plan..."):
            response = co.chat(
                model="command-r-plus",
                message=prompt
            )
            fitness_plan = response.text.strip()

        st.session_state.user_data["fitness_plan"] = fitness_plan
        st.success("Plan generated!")

# ================= PLAN DISPLAY =================
if st.session_state.user_data and "fitness_plan" in st.session_state.user_data:
    st.subheader("Your Weekly Fitness Plan")
    st.write(st.session_state.user_data["fitness_plan"])

# ================= CHATBOT =================
if st.session_state.user_data:
    st.subheader("Ask me anything about fitness")

    # Show chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.write(f"**You:** {msg['content']}")
        else:
            st.write(f"**Bot:** {msg['content']}")

    user_input = st.text_input("Your message")

    if st.button("Send") and user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Build context
        history_text = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in st.session_state.chat_history
        ])

        chat_prompt = f"""
You are a professional fitness trainer.

User profile:
Name: {st.session_state.user_data['name']}
Age: {st.session_state.user_data['age']}
Gender: {st.session_state.user_data['gender']}
Weight: {st.session_state.user_data['weight']} kg
Height: {st.session_state.user_data['height']} cm
Activity Level: {st.session_state.user_data['activity_level']}
Goal: {st.session_state.user_data['goal']}

Fitness Plan:
{st.session_state.user_data['fitness_plan']}

Conversation:
{history_text}

Respond helpfully and professionally.
"""

        with st.spinner("Thinking..."):
            response = co.chat(
                model="command-r-plus",
                message=chat_prompt
            )
            bot_reply = response.text.strip()

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        st.rerun()
