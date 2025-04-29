from pages import *

st.set_page_config(
    layout="wide"
)

def main():
    ss.team_score = ss.match_states[ss.current_match]

    ss.sorted_teams = sort_items(ss.teams, multi_containers=True, direction='vertical')

    ss.player_data = ss.setup_player_data
if __name__ == "__main__":
    main()