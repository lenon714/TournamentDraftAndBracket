from __init__ import *
initialize_ss()

st.set_page_config(
    page_title="Setup",
    page_icon="👋",
)

ss.teams = ss.sorted_teams

st.write("# This is the Setup")

num_teams = st.number_input("Number of Teams:")

update_team_button = st.button('Update Number of Teams')
if update_team_button:
    ss.num_teams = num_teams
    curr_num_teams = len(ss.teams)
    team_diff = int(num_teams) - curr_num_teams + 1
    print(num_teams, curr_num_teams, team_diff)
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
        "name": st.column_config.Column(
            "List of Players",
            width="medium",
            required=True,
        ),
    },
    hide_index=True,
    num_rows="dynamic",
)

tc_keys = list(ss.team_config.keys())
for i, player in enumerate(ss.setup_player_data.name):
    if player not in tc_keys and player is not None:
        add_player = True
        for key in tc_keys:
            if ss.team_config[key]['idx'] == i:
                ss.sorted_teams[ss.team_config[key]['team']]['items'][ss.team_config[key]['pos']] = player
                add_player = False
                break
        if add_player:
            ss.sorted_teams[0]['items'].append(player)

removed_players = set(tc_keys) - set(ss.setup_player_data.name)
for player in removed_players:
    for i, team in enumerate(ss.sorted_teams):
        for j, item in enumerate(team['items']):
            if player == item:
                ss.sorted_teams[i]['items'].remove(player)

ss.team_config = {}
for i, team in enumerate(ss.sorted_teams):
    for j, player in enumerate(team['items']):
        for k, item in enumerate(ss.setup_player_data.name):
            if item == player:
                ss.team_config[player] = {'team': i, 'pos': j, 'idx': k}

st.write(removed_players)
st.write(ss.setup_player_data)
st.write(ss.player_data)
st.write(ss.team_config)
st.write(ss.sorted_teams)