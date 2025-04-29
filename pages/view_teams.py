from pages import *

def main():
    st.set_page_config(
        layout="wide"
    )

    ss.teams = ss.sorted_teams
    ss.player_data = ss.setup_player_data
    ss.team_score = ss.match_states[ss.current_match]
if __name__ == "__main__":
    main()