from __init__ import *

st.set_page_config(
    layout="wide"
)

ss.teams = ss.sorted_teams
ss.team_score = ss.match_states[ss.current_match]

st.title("Welcome to the Hidetone Tekken Tournament")