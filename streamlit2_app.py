import requests
import streamlit as st

st.title("🚀 HackPulse Live Leaderboard")

# 1. Target URL (Use localhost if running on the same laptop, or your ngrok URL)
BACKEND_URL = "http://localhost:3000/api/leaderboard"

target_score = st.number_input("Target Score", min_value=10, value=100)

# 2. Fetch data from your Express server
try:
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        teams_data = response.json()  # Array: [{"teamId":"team-404","gitCommits":1,"score":40}, ...]
    else:
        teams_data = []
        st.error(f"Backend API error: {response.status_code}")
except Exception as e:
    teams_data = []
    st.error(f"Cannot connect to Express server at {BACKEND_URL}. Is node server.js running?")

# 3. Render Leaderboard and Progress Bars
st.subheader("🏆 Team Rankings & Progress")

if teams_data:
    for rank, team in enumerate(teams_data, start=1):
        team_id = team.get("teamId", "Unknown")
        score = team.get("score", 0)
        commits = team.get("gitCommits", 0)
        lines = team.get("cappedLines", 0)
        
        # Calculate progress ratio based on Target Score
        progress_value = min(score / target_score, 1.0)
        
        # Display team status
        st.write(f"**#{rank} | {team_id}** — {score} pts ({commits} commits, {lines} capped line pts)")
        st.progress(progress_value, text=f"Progress: {score}/{target_score} pts")
        st.divider()
else:
    st.info("No team data available yet. Waiting for GitHub webhooks...")

# 4. Manual Refresh Button
if st.button("🔄 Refresh Leaderboard"):
    st.rerun()
