from __init__ import *
from pages.bracket import update_double_elim, calculate_double_elimination

st.set_page_config(
    layout="wide"
)

ss.teams = ss.sorted_teams

def find_teams():
    team_score = {}
    if ss.current_match not in ss.match_states.keys() or len(list(ss.match_states[ss.current_match].keys())) < 4:
        for bracket in ss.matches.keys():
            for match in ss.matches[bracket]:
                if match['id'] == ss.current_match:
                    for team in match['participants']:
                        player_list = [t['header'] for t in ss.sorted_teams] 
                        curr_team = ss.sorted_teams[player_list.index(team['id'])]['items'].copy()
                        team_score[team['id'] + '_win'] = []
                        for i in range(len(curr_team)):
                            team_score[team['id'] + '_win'].append(False)
                        team_score[team['id']] = curr_team
        ss.match_states[ss.current_match] = team_score.copy()
        ss.prev_match = ss.current_match
    elif ss.current_match != ss.prev_match:
        team_score = ss.match_states[ss.current_match]
        ss.prev_match = ss.current_match
    else:
        # Set team score to DNC or Do not change
        team_score = 'DNC'
    return team_score

def find_matches():
    match_list = []
    for match in ss.matches['upper']:
        dd_option = str(match['id']) + ": "
        for participant in match['participants']:
            dd_option = dd_option + str(match['participants'][0]['id']) + " "
        match_list.append(dd_option)
    for match in ss.matches['lower']:
        dd_option = str(match['id']) + ": "
        for participant in match['participants']:
            dd_option = dd_option + str(match['participants'][0]['id']) + " "
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

def update_score(edited_team_score):
    for bracket in ss.matches.keys():
        for i, match in enumerate(ss.matches[bracket]):
            if match['id'] == ss.current_match:
                for j, team in enumerate(match['participants']):
                    if team['id'] == team1:
                        ss.matches[bracket][i]['participants'][j]['resultText'] = str(sum(edited_team_score[team1_win]))
                    elif team['id'] == team2:
                        ss.matches[bracket][i]['participants'][j]['resultText'] = str(sum(edited_team_score[team2_win]))
                    if int(ss.matches[bracket][i]['participants'][j]['resultText']) >= 2:
                        ss.matches[bracket][i]['participants'][j]['isWinner'] = True
                        ss.matches[bracket][i]['state'] = 'SCORE_DONE'
                    else:
                        ss.matches[bracket][i]['participants'][j]['isWinner'] = False

regenerate_bracket_button = st.button("Regenerate Bracket")

if ss.matches == {'upper': [], 'lower': []} or regenerate_bracket_button:
    ss.match_states = {None: {}}
    ss.team_score = {}
    ss.edited_team_score = {}
    ss.prev_match = ""
    ss.current_match = None
    ss.matches = calculate_double_elimination()
    ss.matches = update_double_elim(ss.matches)

try:
    ss.current_match = st.selectbox("Select a Match:", find_matches()).split(":")[0]
except:
    ss.current_match = "W1"

if 'team_score' not in ss:
    ss['team_score'] = find_teams()

team_score_temp = find_teams()
if team_score_temp != 'DNC':
    ss.team_score = team_score_temp

bye = (False, 0)
try:
    for match in ss.matches['upper']:
        if match['id'] == ss.current_match and match['participants'][0]['resultText'] == 'BYE':
            bye = (True, match['participants'][0]['id'])
except:
    pass

if bye[0]:
    st.write(f'# {bye[1]} was given a bye')
elif len(list(ss.team_score.keys())) < 4:
    st.write("# The participants for this match have not been decided yet")
else:
    team1 = list(ss.team_score.keys())[1]
    team2 = list(ss.team_score.keys())[3]

    team1_win = team1 + '_win'
    team2_win = team2 + '_win'

    # st.title(team1 + ' vs ' + team2)

    score_box = st.container()
    
    edited_team_score = st.data_editor(
        ss.team_score,
        key='score_board',
        column_config={
            team1_win: st.column_config.CheckboxColumn(
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
            team2_win: st.column_config.CheckboxColumn(
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
        column_order=(team1_win, team1, team2, team2_win),
    )

    score = str(sum(edited_team_score[team1_win])) + ' - ' + str(sum(edited_team_score[team2_win]))
    score_box.write('Score: ' + score)
    update_score(edited_team_score)

    ss.match_states[ss.current_match] = edited_team_score

# st.write(ss.team_score)
# st.write(edited_team_score)
# st.write(ss.prev_match)
st.write(ss.match_states)

ss.matches = update_double_elim(ss.matches)