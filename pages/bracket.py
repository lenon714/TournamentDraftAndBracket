from __init__ import *
initialize_ss()

ss.teams = ss.sorted_teams

st.set_page_config(
    page_title="Bracket",
    page_icon="👋",
    layout="wide"
)

st.write("# This is the Bracket")

# Sample match data
matches = [
    {
        "id": 1,
        "name": "Match 1",
        "nextMatchId": 3,
        "tournamentRoundText": "Round 1",
        "state": "SCHEDULED",
        "participants": [
            {"id": "a", "name": "Player 1", "isWinner": False, "status": None, "resultText": ""},
            {"id": "b", "name": "Player 2", "isWinner": False, "status": None, "resultText": ""},
        ],
        "startTime": ""
    },
    {
        "id": 2,
        "name": "Match 2",
        "nextMatchId": 3,
        "tournamentRoundText": "Round 1",
        "state": "SCHEDULED",
        "participants": [
            {"id": "c", "name": "Player 3", "isWinner": False, "status": None, "resultText": ""},
            {"id": "d", "name": "Player 4", "isWinner": False, "status": None, "resultText": ""},
        ],
        "startTime": ""
    },
    {
        "id": 3,
        "name": "Final",
        "nextMatchId": None,
        "tournamentRoundText": "Final",
        "state": "SCHEDULED",
        "participants": [],
        "startTime": ""
    }
]

def next_power_of_two(n):
    return 1 if n <= 1 else 2**math.ceil(math.log2(n))

def generate_bracket_ids(num_teams):
    if num_teams < 2:
        raise ValueError("Number of teams must be at least 2")
    
    rounded_teams = next_power_of_two(num_teams)
    total_matches = rounded_teams - 1
    bracket = []
    current_id = 1
    matches_in_round = rounded_teams // 2

    while matches_in_round > 0:
        round_matches = list(range(current_id, current_id + matches_in_round))
        bracket.append(round_matches)
        current_id += matches_in_round
        matches_in_round //= 2

    return bracket

matches = []
participants = []
matchups = []
count = 0

byes = next_power_of_two(len(ss.teams)-1) - len(ss.teams) + 1
bracketID = generate_bracket_ids(len(ss.teams)-1)

for i, team in enumerate(ss.teams[1::]):
    if count <= 1:
        if byes > 0:
            participants.append({"id": "", "name": team['header'], "isWinner": True, "status": None, "resultsText": ""})
            count += 1
            byes -= 1
        else:
            participants.append({"id": "", "name": team['header'], "isWinner": False, "status": None, "resultsText": ""})
        count += 1
    if count > 1:
        matchups.append(participants)
        count = 0
        participants = []

for i, ID in enumerate(bracketID[0]):
    nextID = bracketID[1][i//2]
    if matchups[i][0]['isWinner']:
        state = "WALK_OVER"
    else:
        state = "SCHEDULED"
    matches.append({
        "id": ID,
        "name": "",
        "nextMatchId": nextID,
        "tournamentRoundText": "1",
        "state": state,
        "participants": matchups[i],
        "startTime": ""
        })

for i, t_round in enumerate(bracketID[1::]):
    for ID in t_round: 
        try:
            nextID = bracketID[i+2][i//2]
        except:
            nextID = None
        matches.append({
        "id": ID,
        "name": "",
        "nextMatchId": nextID,
        "tournamentRoundText": str(i+2),
        "state": "SCHEDULED",
        "participants": [],
        "startTime": ""
        })

# Render the bracket
bracket = tournament_bracket(matches=matches)

st.write(bracketID)
st.write(matchups)