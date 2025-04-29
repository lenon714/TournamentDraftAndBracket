from pages import *

_component_func = components.declare_component(
    "bracket",
    path=("/mount/src/tournamentdraftandbracket/bracket_app/streamlit_bracket/frontend/build")
    # url='http://localhost:3001'
)

def tournament_bracket(matches, teams, scores):
    return _component_func(matches=matches, teams=teams, scores=scores)