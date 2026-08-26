import streamlit as st

def commit_progress_score(commit_count: int, target_commits: int = 20) -> float:
    if target_commits <= 0:
        return 0.0
    return min(commit_count / target_commits, 1.0)
