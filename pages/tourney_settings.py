from __init__ import *

ss.teams = ss.sorted_teams
ss.team_score = ss.match_states[ss.current_match]

st.set_page_config(
    layout="wide"
)

tourney_format = st.selectbox('Format: ', options=['WASEDA', 'Pokemon'])