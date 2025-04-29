from pages import *

def init_teams():
    for bracket in ss.matches.keys():
        for match in ss.matches[bracket]:
            ss.prev_match = ""
            ss.current_match = match['id']
            ss.match_states[ss.current_match] = find_teams()

def find_teams():
    team_score = {'team1_win': [], 'team2_win': []}
    if ss.current_match not in ss.match_states.keys():
        for bracket in ss.matches.keys():
            for match in ss.matches[bracket]:
                if match['id'] == ss.current_match:
                    for i, team in enumerate(match['participants']):
                        team_list = [t['header'] for t in ss.sorted_teams] 
                        players = ss.sorted_teams[team_list.index(team['id'])]['items'].copy()
                        for j in range(len(players)):
                            team_score['team' + str(i+1) + '_win'].append(False)
                        team_score[team['id']] = players
        ss.match_states[ss.current_match] = team_score.copy()
        ss.prev_match = ss.current_match
    elif ss.current_match != ss.prev_match and ss.current_match is not None:
        team_score = ss.match_states[ss.current_match]
        if team_score['team1_win'] == [] and len(list(team_score.keys())) >= 3:
            team_score['team1_win'] = [False]*len(team_score[list(team_score.keys())[2]])
        if team_score['team2_win'] == [] and len(list(team_score.keys())) == 4:
            team_score['team2_win'] = [False]*len(team_score[list(team_score.keys())[3]])
        ss.prev_match = ss.current_match
    else:
        # Set team score to DNC or Do not change
        team_score = {}
    return team_score

def find_matches():
    match_list = []
    for bracket in ss.matches:
        for match in ss.matches[bracket]:
            team_count = 0
            dd_option = str(match['id']) + ": "
            for participant in match['participants']:
                dd_option = dd_option + str(participant['id']) + " vs "
                team_count += 1
            if team_count:
                dd_option = dd_option[:-3]
            match_list.append(dd_option)
    return match_list

def compare_dicts_of_lists(dict1, dict2):
    """
    Compares two dictionaries with lists of equal length as values.
    Returns a dictionary mapping keys to indices where values differ.
    """
    differences = {}

    for key in dict1:
        if key in dict2:
            diffs = [i for i, (a, b) in enumerate(zip(dict1[key], dict2[key])) if a != b]
            if diffs:
                differences[key] = diffs
        else:
            differences[key] = 'Missing in dict2'

    return differences

def update_score(team1, team2):
    for bracket in ss.matches.keys():
        for i, match in enumerate(ss.matches[bracket]):
            if match['id'] == ss.current_match:
                for j, team in enumerate(match['participants']):
                    if team['id'] == team1:
                        ss.matches[bracket][i]['participants'][j]['resultText'] = str(sum(ss.edited_team_score['team1_win']))
                    elif team['id'] == team2:
                        ss.matches[bracket][i]['participants'][j]['resultText'] = str(sum(ss.edited_team_score['team2_win']))
                    if int(ss.matches[bracket][i]['participants'][j]['resultText']) >= 2:
                        ss.matches[bracket][i]['participants'][j]['isWinner'] = True
                    else:
                        ss.matches[bracket][i]['participants'][j]['isWinner'] = False
    ss.match_states[ss.current_match] = ss.edited_team_score 

def main():
    st.set_page_config(
    layout="wide"
    )
    
    ss.teams = ss.sorted_teams

    ss.rerun = False

    regenerate_bracket_button = st.button("Regenerate Bracket")

    if ss.matches == {'upper': [], 'lower': []} or regenerate_bracket_button:
        ss.match_states = {None: {}}    
        ss.prev_match = ""
        ss.current_match = None
        ss.matches = calculate_double_elimination()
        ss.matches = update_bracket(ss.matches)
        ss.team_score = find_teams()
        ss.edited_team_score = ss.match_states[ss.current_match]
        init_teams()

    if ss.current_match == None:
        ss.current_match = 'W1'
    if 'match_index' not in ss:
        ss.match_index = 0
    if 'selected_match' not in ss:
        ss.selected_match = None

    match_select = st.container()

    ss.match_select_options = find_matches()

    if 'team_score' not in ss:
        ss.team_score = find_teams()
    if 'edited_team_score' not in ss:
        ss.edited_team_score = ss.match_states[ss.current_match]

    team_score_temp = find_teams()
    if team_score_temp != {}:
        ss.team_score = team_score_temp

    bye = (False, 0)
    try:
        for match in ss.matches['upper']:
            if match['id'] == ss.current_match and match['participants'][0]['resultText'] == 'BYE':
                bye = (True, match['participants'][0]['id'])
    except:
        pass 

    if bye[0]:
        st.write('# {bye[1]} was given a bye')
    elif len(list(ss.team_score.keys())) < 4:
        st.write("# The participants for this match have not been decided yet")
    else:
        team1 = list(ss.match_states[ss.current_match].keys())[2]
        team2 = list(ss.match_states[ss.current_match].keys())[3]
        
        score_box = st.container()
        
        ss.edited_team_score = st.data_editor(
            ss.team_score,
            key='score_board',
            column_config={
                'team1_win': st.column_config.CheckboxColumn(
                    '',
                    width="small",
                    default=False,
                    pinned=True,
                    disabled=False,
                ),
                team1: st.column_config.Column(
                    team1,
                    width="medium",
                    required=False,
                    pinned=True,
                    disabled=True,
                ),
                team2: st.column_config.Column(
                    team2,
                    width="medium",
                    required=False,
                    pinned=True,
                    disabled=True,
                ),
                'team2_win': st.column_config.CheckboxColumn(
                    '',
                    width="small",
                    default=False,
                    pinned=True,
                    disabled=False,
                ),
            },
            width=552,
            hide_index=True,
            num_rows="fixed",
            column_order=('team1_win', team1, team2, 'team2_win'),
        )

        score = str(sum(ss.edited_team_score['team1_win'])) + ' - ' + str(sum(ss.edited_team_score['team2_win']))
        score_box.write('Score: ' + score)
        update_score(team1, team2)
        ss.match_index = ss.match_select_options.index(ss.selected_match)

    # st.write(ss.team_score)
    # st.write(ss.edited_team_score)
    # st.write(ss.prev_match)
    st.write(ss.match_states)

    ss.matches = update_bracket(ss.matches)
    ss.match_select_options = find_matches()

    ss.selected_match = match_select.selectbox("Select a Match:", ss.match_select_options, key='match_select', index=ss.match_index)
    ss.current_match = ss.selected_match.split(":")[0]

    st.rerun()

    update_server_state()

if __name__ == "__main__":
    main()