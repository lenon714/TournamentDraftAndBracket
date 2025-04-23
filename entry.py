from __init__ import *
initialize_ss()

home = st.Page('pages/home.py', title='Home')
bracket = st.Page('pages/bracket.py', title='Bracket')
view_matches = st.Page('pages/view_matches.py', title='View Match')
view_teams = st.Page('pages/view_teams.py', title='View Teams')
edit_matches = st.Page('pages/edit_matches.py', title='Score Matches')
team_draft = st.Page('pages/team_draft.py', title='Team Draft')
team_setup = st.Page('pages/team_setup.py', title='Team Setup')
tourney_settings = st.Page('pages/tourney_settings.py', title='Tournament Settings')

pg = st.navigation({
    '': [home],
    'Tournament': [bracket, view_matches, view_teams],
    'Setup': [edit_matches, team_draft, team_setup, tourney_settings],
    })
pg.run()