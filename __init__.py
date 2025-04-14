import streamlit as st
from streamlit_sortables import sort_items
from streamlit import session_state as ss
import pandas as pd

def initialize_ss():
    if 'player_data' not in ss:
        ss['player_data'] = pd.DataFrame({'name':['P1', 'P2']})
    if 'setup_player_list' not in ss:
        ss['setup_player_list'] = ss.player_data.copy()
    if 'team_config' not in ss:
        ss['team_config'] = {'P1':{'team': 0, 'pos': 0, 'idx': 0},
                            'P2':{'team': 0, 'pos': 1, 'idx': 1}}
    if 'teams' not in ss:
        ss['teams'] = [
            {'header': 'Player List', 'items': ['P1', 'P2']},
            {'header': 'Team 1',  'items': []},
            {'header': 'Team 2',  'items': []},
            {'header': 'Team 3',  'items': []},
            {'header': 'Team 4',  'items': []},
            {'header': 'Team 5',  'items': []},
            {'header': 'Team 6',  'items': []},
        ]
    if 'sorted_teams' not in ss:
        ss['sorted_teams'] = ss.teams.copy()
    if 'num_teams' not in ss:
        ss['num_teams'] = 0