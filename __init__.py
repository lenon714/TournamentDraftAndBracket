import streamlit as st
from streamlit_sortables import sort_items
from streamlit import session_state as ss
import pandas as pd
import streamlit.components.v1 as components
import os
from bracket_app import tournament_bracket
import math

def initialize_ss():
    if 'player_data' not in ss:
        ss['player_data'] = pd.DataFrame({'name':['P1', 'P2'], 'captain':[True, False]})
    if 'setup_player_data' not in ss:
        ss['setup_player_data'] = ss.player_data
    if 'player_config' not in ss:
        # team: Current team player is placed in
        # pos: Current position on the team
        # idx: Current index on player list
        # cap: If they are a captain
        ss['player_config'] = {'P1':{'team': 0, 'pos': 0, 'idx': 0, 'cap': True},
                            'P2':{'team': 0, 'pos': 1, 'idx': 1, 'cap': False}}
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
        ss['sorted_teams'] = ss.teams
    if 'num_teams' not in ss:
        ss['num_teams'] = 0