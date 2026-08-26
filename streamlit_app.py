import requests
import streamlit as st
from datetime import datetime, timezone

st.title("🚀 Progress Bar Demo")

target_commits = st.number_input("Target commits per group", min_value=1, value=10)

if "groups" not in st.session_state:
    st.session_state.groups = [
        {"name": "Team Alpha", "owner": "octocat", "repo": "Hello-World"},
        {"name": "Team Beta", "owner": "octocat", "repo": "Spoon-Knife"},
    ]

with st.expander("Add a group"):
    new_name = st.text_input("Group name")
    new_owner = st.text_input("GitHub owner/org")
    new_repo = st.text_input("Repo name")
    if st.button("Add group"):
        if new_name and new_owner and new_repo:
            st.session_state.groups.append(
                {"name": new_name, "owner": new_owner, "repo": new_repo}
            )
            st.rerun()
        else:
            st.warning("Fill in all three fields first.")
 
if st.button("🔄 Refresh all"):
    st.rerun()

def get_commit_count(owner: str, repo: str) -> int:
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url, params={"per_page": 100})
    if response.status_code == 200:
        return len(response.json())
    return 0
 
 
# Loop over every group, call the API for each, draw a bar for each 
for group in st.session_state.groups:
    commit_count = get_commit_count(group["owner"], group["repo"])
    progress_value = min(commit_count / target_commits, 1.0)
 
    st.subheader(group["name"])
    st.progress(progress_value, text=f"{commit_count} / {target_commits} commits")
    st.caption(f"{group['owner']}/{group['repo']}")
    st.write("")
