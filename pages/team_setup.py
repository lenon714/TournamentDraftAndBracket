from __init__ import *

st.set_page_config(
    layout="wide"
)

ss.teams = ss.sorted_teams
ss.team_score = ss.match_states[ss.current_match]

def handle_add_and_rename(tc_keys):
    for i, player in enumerate(ss.setup_player_data.name):
        if player not in tc_keys and player is not None:
            add_player = True
            for key in tc_keys:
                if ss.player_config[key]['idx'] == i:
                    ss.sorted_teams[ss.player_config[key]['team']]['items'][ss.player_config[key]['pos']] = player
                    add_player = False
                    break
            if add_player:
                ss.sorted_teams[0]['items'].append(player)

def remove_players(removed_players):
    for player in removed_players:
        for i, team in enumerate(ss.sorted_teams):
            for j, item in enumerate(team['items']):
                if player == item:
                    ss.sorted_teams[i]['items'].remove(player)

def generate_player_config():
    for i, team in enumerate(ss.sorted_teams):
        for j, player in enumerate(team['items']):
            for k, item in enumerate(ss.setup_player_data['name']):
                if item == player:
                    ss.player_config[player] = {'team': i, 'pos': j, 'idx': k, 'cap': ss.setup_player_data['captain'][k]}

def update_captains():
    for i, player in enumerate(ss.setup_player_data.iloc[:, 0]):
        # Check if player is a captain
        if ss.setup_player_data['captain'][i]:
            # Find which teams have captains
            cap_dict = find_captains()
            for team in list(cap_dict.keys())[1::]:
                if cap_dict[team] < 1:
                    # Insert player at top of captainless team
                    ss.sorted_teams[team]['items'].insert(0, player)
                    # Remove them from original location
                    ss.sorted_teams[ss.player_config[player]['team']]['items'].remove(player)
                    ss.sorted_teams[team]['header'] = str('Team ' + player)
                    generate_player_config()
                    break
                elif team == ss.player_config[player]['team'] and cap_dict[team] == 1:
                    ss.sorted_teams[team]['header'] = str('Team ' + player)
                    generate_player_config()
                    break

def find_captains():
    cap_dict = {}
    for i in range(len(ss.sorted_teams)):
        cap_dict[i] = 0
    for player in ss.player_config.keys():
        team = ss.player_config[player]['team']
        if ss.player_config[player]['cap']:
            cap_dict[team] += 1
    return cap_dict

ss.teams = ss.sorted_teams

st.write("# This is the Setup")

num_teams = st.number_input("Number of Teams:")

update_team_button = st.button('Update Number of Teams')
if update_team_button:
    ss.num_teams = num_teams
    curr_num_teams = len(ss.teams)
    team_diff = int(num_teams) - curr_num_teams + 1
    if team_diff > 0:
        for i in range(team_diff):
            ss.teams.append({'header': 'Team ' + str(i + curr_num_teams), 'items': []})
    elif team_diff <= 0:
        for i in range(abs(team_diff)):
            ss.teams.pop()

ss.setup_player_data = st.data_editor(
    ss.player_data,
    key='player_data_editor',
    column_config={
        'name': st.column_config.Column(
            "List of Players",
            width="large",
            required=True,
            pinned=True,
        ),
        'captain': st.column_config.CheckboxColumn(
            "Captains",
            width="medium",
            default=False,
            pinned=True,
        )
    },
    width=641,
    hide_index=True,
    num_rows="dynamic",
)

tc_keys = list(ss.player_config.keys())
handle_add_and_rename(tc_keys)

removed_players = set(tc_keys) - set(ss.setup_player_data.name)
remove_players(removed_players)

ss.setup_player_data = ss.setup_player_data.reset_index(drop=True)

ss.player_config = {}
generate_player_config()

cap_dict = find_captains()
# update_captains()

st.write(cap_dict)
st.write(ss.player_data)
st.write(ss.player_config)
st.write(ss.sorted_teams)