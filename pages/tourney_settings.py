from pages import *

def main():
    ss.teams = ss.sorted_teams
    ss.player_data = ss.setup_player_data
    ss.team_score = ss.match_states[ss.current_match]

    st.set_page_config(
        layout="wide"
    )

    tourney_format = st.selectbox('Format: ', options=['WASEDA', 'Pokemon'])
if __name__ == "__main__":
    main()