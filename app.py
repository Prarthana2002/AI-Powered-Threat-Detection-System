import streamlit as st
import google.generativeai as genai
import numpy as np
import random
import requests


# Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "Your-TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "Your- TELEGRAM_CHAT_ID"

# Function to analyze input and detect anomalies
def detect_anomaly(user_input):
    prompt = f"""
    You are an AI trained to detect anomalies in network logs and error messages.
    Analyze the following input and classify it as:
    - "Anomaly" (if it indicates an attack, security threat, or network issue)
    - "Normal" (if there is no unusual activity).

    Input:
    {user_input}

    Output: (Only respond with "Anomaly" or "Normal")
    """

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    return response.text.strip()

# Function to send Telegram alert
def send_telegram_alert(anomaly_details):
    message = f"\U0001F6A8 *Cybersecurity Alert!* \U0001F6A8\n\n\U0001F50D *Anomaly Detected:*\n{anomaly_details}\n\n⚠️ Immediate action required!"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# RL Decision Making Class
class CyberSecurityEnv:
    def __init__(self):
        self.states = ["Low-Risk", "Medium-Risk", "High-Risk"]
        self.actions = ["Mitigation", "Alert"]
        self.state = random.choice(self.states)

    def reset(self):
        self.state = random.choice(self.states)
        return self.state

    def step(self, action):
        reward = 10 if (self.state == "Low-Risk" and action == "Mitigation") else 15 if (self.state == "High-Risk" and action == "Alert") else -5
        self.state = random.choice(self.states)
        return self.state, reward

env = CyberSecurityEnv()

def rl_decision(state):
    state_idx = env.states.index(state)
    return env.actions[state_idx % 2]

# Streamlit UI
st.set_page_config(page_title="🔍 Anomaly Detector", layout="centered")

# Sidebar with title and logo
st.sidebar.markdown("<h1 style='color: navy;'>Threat Detection using Reinforcement Learning</h1>", unsafe_allow_html=True)

# Upload and display logo
logo_path = "Logo.png"
try:
    st.sidebar.image(logo_path, use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("⚠️ Logo image not found. Please upload 'logo.jpg'.")

# Main page content
st.title("🚀 AI-Powered Data Threat Detector")
st.markdown("### 🛡️ Detect security threats and take action in real-time!")

user_input = st.text_area("📝 Enter Network Log / Error Message:", "")
if st.button("🔍 Predict"):
    if user_input.strip():
        result = detect_anomaly(user_input)
        st.write(f"### 🔎 Detection Result: `{result}`")

        if result == "Anomaly":
            risk_level = random.choice(env.states)
            decision = rl_decision(risk_level)
            st.write(f"### 🤖 RL Decision: `{decision}`")

            if decision == "Mitigation":
                st.success("✅ Suggested Mitigation Actions: Consult security team.")
            elif decision == "Alert":
                send_telegram_alert(user_input)
                st.error("🚨 Alert Sent to Security Team!")
        else:
            st.success("✅ No security threat detected.")
    else:
        st.warning("⚠️ Please enter a network log or error message.")
