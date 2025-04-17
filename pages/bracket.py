from __init__ import *
initialize_ss()

ss.teams = ss.sorted_teams

st.set_page_config(
    page_title="Bracket",
    page_icon="👋",
)

st.write("# This is the Bracket")

# Sample match data
matches = [
    {
        "id": 1,
        "name": "Match 1",
        "nextMatchId": 3,
        "tournamentRoundText": "Round 1",
        "startTime": "2021-05-30",
        "state": "SCHEDULED",
        "participants": [
            {"id": "a", "name": "Player 1", "isWinner": False, "status": None, "resultText": ""},
            {"id": "b", "name": "Player 2", "isWinner": False, "status": None, "resultText": ""},
        ],
    },
    {
        "id": 2,
        "name": "Match 2",
        "nextMatchId": 3,
        "tournamentRoundText": "Round 1",
        "startTime": "2021-05-30",
        "state": "SCHEDULED",
        "participants": [
            {"id": "c", "name": "Player 3", "isWinner": False, "status": None, "resultText": ""},
            {"id": "d", "name": "Player 4", "isWinner": False, "status": None, "resultText": ""},
        ],
    },
    {
        "id": 3,
        "name": "Final",
        "nextMatchId": None,
        "tournamentRoundText": "Final",
        "startTime": "2021-06-01",
        "state": "SCHEDULED",
        "participants": [],
    },
]
# Render the bracket
bracket = tournament_bracket(matches=matches)