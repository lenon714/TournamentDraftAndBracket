from __init__ import *

st.set_page_config(
    layout="wide"
)

ss.team_score = ss.match_states[ss.current_match]

ss.sorted_teams = sort_items(ss.teams, multi_containers=True, direction='vertical')

ss.player_data = ss.setup_player_data