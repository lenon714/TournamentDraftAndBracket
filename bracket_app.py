from __init__ import *

_component_func = components.declare_component(
    "bracket",
    path=os.path.join(os.path.dirname(__file__), "streamlit_bracket_app", "streamlit_bracket", "frontend", "build")
    # url='http://localhost:3001'
)

def tournament_bracket(matches):
    return _component_func(matches=matches)