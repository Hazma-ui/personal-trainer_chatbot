Personal Trainer Chatbot

Overview

The Personal Trainer Chatbot is a Streamlit-based web application that provides users with personalized fitness plans and expert advice. By leveraging Cohere's natural language processing capabilities, the app interacts with users to gather their fitness data, generate tailored workout plans, and respond to fitness-related queries in a conversational manner.

Features

User Profile Creation:

Collects user details such as name, age, gender, weight, height, activity level, and fitness goals.

Custom Fitness Plan Generator:

Generates a weekly fitness plan based on user input using Cohere's AI language model.

Chatbot for Fitness Advice:

Enables users to ask questions about fitness, workouts, and health.

Remembers chat history for seamless conversations.

Interactive UI:

Uses Streamlit for an easy-to-use and visually appealing interface.

Requirements

Python Libraries

Streamlit: For building the interactive web app.

Cohere: To utilize the AI language model.

dotenv: For securely managing API keys and environment variables.

os: To handle environment variables.

API Key

To run this application, you will need a Cohere API key. Add it to a .env file in the following format:

COHERE_API_KEY=your_cohere_api_key_here

Installation

Clone the repository.

Install the required Python packages:

pip install streamlit cohere python-dotenv

Create a .env file and add your Cohere API key as mentioned above.

Run the Streamlit application:

streamlit run app.py

Open the app in your browser using the URL provided by Streamlit (e.g., http://localhost:8501).

Usage

Step 1: Enter User Information

On the first screen, fill out the form with your personal details such as age, weight, height, activity level, and fitness goal. Submit the form to generate a tailored fitness plan.

Step 2: View Fitness Plan

Once the plan is generated, it will be displayed on the screen. You can always refer back to it while interacting with the chatbot.

Step 3: Chat with the Bot

Use the chat interface to ask questions about fitness and health. The chatbot will provide expert advice based on the user profile and the fitness plan.

Code Structure

Environment Setup:

.env file for storing the Cohere API key.

Streamlit Session State:

Saves user profile, fitness plan, and chat history across interactions.

Prompt Engineering:

Generates dynamic prompts for Cohere based on user input and chat context.

Fitness Plan Generation:

Uses Cohere's generate API to create a realistic weekly fitness plan.

Chat Interface:

Maintains a conversation history to deliver context-aware responses.
