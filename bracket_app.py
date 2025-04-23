from __init__ import *

_component_func = components.declare_component(
    'bracket',
    path='streamlit_bracket_app/streamlit_bracket/frontend'
    # url='http://localhost:3001'
)

def tournament_bracket(matches):
    return _component_func(matches=matches)