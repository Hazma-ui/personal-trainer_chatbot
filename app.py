import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
COHERE_API_KEY = "7VnnFqfEDDwXWz2TBrop83ver1yJPrDu7bngPm4F"


# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Initialize Streamlit Session State
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI setup
st.title("Personal Trainer Chatbot")

# Collect User Information
if st.session_state.user_data is None:
    with st.form("user_info_form"):
        st.header("Tell me about yourself:")
        name = st.text_input("What is your name?")
        age = st.number_input("What is your age?", min_value=10, max_value=100, value=25)
        gender = st.selectbox("What is your gender?", options=["Male", "Female", "Other"])
        weight = st.number_input("What is your weight (kg)?", min_value=30, max_value=300, value=70)
        height = st.number_input("What is your height (cm)?", min_value=100, max_value=250, value=170)
        activity_level = st.selectbox("What is your activity level?", 
                                      options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        goal = st.selectbox("What is your fitness goal?", 
                             options=["Lose Weight", "Gain Muscle", "Improve Endurance", "Stay Healthy"])
        submit = st.form_submit_button("Generate Plan")

    if submit:
        # Save user data into session state
        st.session_state.user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "activity_level": activity_level,
            "goal": goal,
        }

        # Generate fitness plan
        prompt = f"""
        You are a professional fitness trainer. Based on the user's information provided below, 
        create a unique weekly fitness plan. Make it realistic and achievable for their goal. 
        Use the details provided:

        User Information:
        Name: {name}
        Age: {age}
        Gender: {gender}
        Weight: {weight} kg
        Height: {height} cm
        Activity Level: {activity_level}
        Goal: {goal}

        Fitness Plan:
        """

        with st.spinner("Generating your fitness plan..."):
            response = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=1200,
                temperature=0.7
            )
            fitness_plan = response.generations[0].text.strip()

        st.session_state.user_data["fitness_plan"] = fitness_plan  # Save plan in session state
        st.success("Here is your tailored fitness plan!")

# Fitness Plan Section
if st.session_state.user_data and "fitness_plan" in st.session_state.user_data:
    st.write("### Your Weekly Fitness Plan:")
    st.text(st.session_state.user_data["fitness_plan"])  # Always show the fitness plan

# Chatbot Interface
if st.session_state.user_data:
    st.write("### Ask me anything about fitness!")

    # Chat history display
    chat_container = st.container()  # Use a container to append chat messages
    with chat_container:
        for msg in st.session_state.chat_history:
            # Safely access 'message' for user and 'response' for bot
            user_msg = msg.get("message", "")  # Default to empty string if 'message' key is not found
            bot_msg = msg.get("response", "")  # Default to empty string if 'response' key is not found
            
            if user_msg:
                st.write(f"**You:** {user_msg}")
            if bot_msg:
                st.write(f"**Bot:** {bot_msg}")

    # Chat input bar
    with st.container():
        user_message = st.text_input("Your message:", key="user_input", placeholder="Ask something...")
        if st.button("Send"):
            if user_message:
                # Add user message to chat history
                st.session_state.chat_history.append({"sender": "user", "message": user_message})

                # Create chatbot prompt with user data and chat history
                chat_history_text = ""
                for msg in st.session_state.chat_history:
                    user_msg = msg.get("message", "")
                    bot_msg = msg.get("response", "")
                    chat_history_text += f"User: {user_msg}\nBot: {bot_msg}\n"

                # Prepare the final prompt string without causing escape sequence issues
                chat_prompt = f"""
                You are a professional fitness trainer chatbot. The user has shared their profile with you:
                Name: {st.session_state.user_data['name']}
                Age: {st.session_state.user_data['age']}
                Gender: {st.session_state.user_data['gender']}
                Weight: {st.session_state.user_data['weight']} kg
                Height: {st.session_state.user_data['height']} cm
                Activity Level: {st.session_state.user_data['activity_level']}
                Goal: {st.session_state.user_data['goal']}

                Fitness Plan:
                {st.session_state.user_data['fitness_plan']}  # No backslashes or escape sequences

                Chat History:
                {chat_history_text}  # Safe chat history handling

                User Message: {user_message}

                Respond as a fitness trainer with expert advice:
                """

                # Generate response
                with st.spinner("Thinking..."):
                    response = co.generate(
                        model="command-r-plus",
                        prompt=chat_prompt,
                        max_tokens=200,
                        temperature=0.7
                    )
                    bot_message = response.generations[0].text.strip()

                # Add bot response to chat history
                st.session_state.chat_history.append({"sender": "bot", "response": bot_message})
