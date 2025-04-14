from __init__ import *
initialize_ss()

st.set_page_config(
    page_title="Team Draft",
    page_icon="👋",
)

st.write("# Welcome to the Hidetone Tekken Tournament")

ss.sorted_teams = sort_items(ss.teams, multi_containers=True, direction='vertical')

ss.player_data = ss.setup_player_data.copy()