import streamlit as st
from streamlit_sortables import sort_items
from streamlit import session_state as ss
import pandas as pd
import streamlit.components.v1 as components
import os
from bracket_app import tournament_bracket
import math
import json
# from sample_match_data import sample_match

def initialize_ss():
    if 'player_data' not in ss:
        # ss['player_data'] = pd.DataFrame({'name':['P1', 'P2'], 'captain':[True, False]})
        # Sample Data
        ss['player_data'] = pd.DataFrame({'name':['Knee', 'Mulgold', 'LowHigh', 
                                                  'Arslan Ash', 'ATIF', 'William', 
                                                  'Tetsu', 'Dombilimaymun', 'Strog', 
                                                  'Raef', 'JJ', 'Renzoken'], 
                                          'captain':[True, False, False,
                                                     True, False, False,
                                                     True, False, False,
                                                     True, False, False,]})
    if 'setup_player_data' not in ss:
        ss['setup_player_data'] = ss.player_data
    if 'player_config' not in ss:
        # team: Current team player is placed in
        # pos: Current position on the team
        # idx: Current index on player list
        # cap: If they are a captain
        # ss['player_config'] = {'P1':{'team': 0, 'pos': 0, 'idx': 0, 'cap': True},
        #                     'P2':{'team': 0, 'pos': 1, 'idx': 1, 'cap': False}}
        # Sample Config
        ss['player_config'] = {'Knee': {'team': 1, 'pos': 0, 'idx': 0, 'cap': True},
                             'Mulgold': {'team': 1, 'pos': 1, 'idx': 1, 'cap': False},
                             'LowHigh': {'team': 1, 'pos': 2, 'idx': 2, 'cap': False},
                             'Arslan Ash': {'team': 2, 'pos': 0, 'idx': 3, 'cap': True},
                             'ATIF': {'team': 2, 'pos': 1, 'idx': 4, 'cap': False},
                             'William': {'team': 2, 'pos': 2, 'idx': 5, 'cap': False},
                             'Tetsu': {'team': 3, 'pos': 0, 'idx': 6, 'cap': True},
                             'Dombilimaymun': {'team': 3, 'pos': 1, 'idx': 7, 'cap': False},
                             'Strog': {'team': 3, 'pos': 2, 'idx': 8, 'cap': False},
                             'Raef': {'team': 4, 'pos': 0, 'idx': 9, 'cap': True},
                             'JJ': {'team': 4, 'pos': 1, 'idx': 10, 'cap': False},
                             'Renzoken': {'team': 4, 'pos': 2, 'idx': 11, 'cap': False},
                             }
    if 'teams' not in ss:
        # ss['teams'] = [
        #     {'header': 'Player List', 'items': ['P1', 'P2']},
        #     {'header': 'Team 1',  'items': []},
        #     {'header': 'Team 2',  'items': []},
        #     {'header': 'Team 3',  'items': []},
        #     {'header': 'Team 4',  'items': []},
        #     {'header': 'Team 5',  'items': []},
        #     {'header': 'Team 6',  'items': []},
        # ]
        # Sample Team
        ss['teams']= [
            {'header': 'Player List', 'items': []},
            {'header': 'Team South Korea',  'items': ['Knee', 'Mulgold', 'LowHigh']},
            {'header': 'Team Pakistan',  'items': ['Arslan Ash', 'ATIF',  'William']},
            {'header': 'Team Europe',  'items': ['Tetsu', 'Dombilimaymun', 'Strog']},
            {'header': 'Team Middle East',  'items': ['Raef', 'JJ', 'Renzoken']},
        ]
    if 'sorted_teams' not in ss:
        ss['sorted_teams'] = ss.teams
    if 'num_teams' not in ss:
        ss['num_teams'] = 0
    if 'matches' not in ss:
        ss['matches'] = {'upper': [], 'lower': []}
    if 'match_states' not in ss:
        ss['match_states'] = {None: {}}
    if 'prev_match' not in ss:
        ss['prev_match'] = ""
    if 'current_match' not in ss:
        ss['current_match'] = None