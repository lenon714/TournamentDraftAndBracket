from pages import *

def update_server_state():
    with server_state_lock['matches']:  # Lock the "count" state for thread-safety
        server_state['matches'] = ss.matches.copy()
    
    teams_dict = {}
    for team in ss.teams:
        teams_dict[team['header']] = team

    with server_state_lock['teams']:
        server_state['teams'] = teams_dict.copy()

    match_wins = {}
    for match in list(ss.match_states.keys())[1:]:
        match_wins[match] = {}
        for i in range(2, 4):
            try:
                for j, player in enumerate(ss.match_states[match][list(ss.match_states[match].keys())[i]]):
                    match_wins[match][player] = ss.match_states[match]['team' + str(i-1) + '_win'][j]
            except:
                match_wins[match] = "TBD"
    
    with server_state_lock['match_wins']:
        server_state['match_wins'] = match_wins.copy()

def main():
    st.set_page_config(
    layout="wide"
    )
    
    ss.teams = ss.sorted_teams
    ss.player_data = ss.setup_player_data
    ss.team_score = ss.match_states[ss.current_match]

    st.title("Welcome to the Hidetone Tekken Tournament")
if __name__ == "__main__":
    main()