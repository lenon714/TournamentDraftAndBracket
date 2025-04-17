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

def generate_double_elim_bracket(num_teams):
    assert (num_teams & (num_teams - 1)) == 0, "Teams must be power of 2"
    num_rounds = int(math.log2(num_teams))
    
    match_dict = {}
    match_id = 1

    winners_matches = []
    losers_matches = []

    # Generate Winners Bracket
    for r in range(num_rounds):
        round_matches = []
        for _ in range(num_teams // (2 ** (r + 1))):
            m = f'U{match_id}'
            match_dict[m] = {'upper': None, 'lower': None}
            round_matches.append(m)
            match_id += 1
        winners_matches.append(round_matches)

    # Generate Losers Bracket (2*num_rounds - 1 rounds)
    total_losers_rounds = 2 * num_rounds - 1
    for r in range(total_losers_rounds):
        round_matches = []
        num_matches = num_teams // (2 ** ((r // 2) + 1)) if r < total_losers_rounds - 1 else 1
        for _ in range(num_matches):
            m = f'L{match_id}'
            match_dict[m] = {'upper': None, 'lower': None}
            round_matches.append(m)
            match_id += 1
        losers_matches.append(round_matches)

    # Wire Winners Bracket
    for r, round_matches in enumerate(winners_matches[:-1]):
        next_round = winners_matches[r + 1]
        for i, m in enumerate(round_matches):
            next_m = next_round[i // 2]
            match_dict[m]['upper'] = next_m
            # Also send loser to appropriate first loser round
            loser_r = 2 * r
            loser_m = losers_matches[loser_r][i]
            match_dict[m]['lower'] = loser_m

    # Wire Losers Bracket
    for r, round_matches in enumerate(losers_matches[:-1]):
        next_round = losers_matches[r + 1]
        for i, m in enumerate(round_matches):
            next_m = next_round[i // 2]
            match_dict[m]['upper'] = next_m

    # Wire Winners Final to Grand Final
    final_w = winners_matches[-1][0]
    final_l = losers_matches[-1][0]
    grand_final = f'U{match_id}'
    match_dict[grand_final] = {'upper': 'reset', 'lower': 'reset'}
    match_dict[grand_final] = {'upper': None, 'lower': None}
    match_dict[final_w]['upper'] = grand_final
    match_dict[final_l]['upper'] = grand_final
    
    return match_dict

def calculate_single_elimination():
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
        for j, ID in enumerate(t_round): 
            print("i " + str(i))
            print("j " + str(j//2))
            try:
                nextID = bracketID[i+2][j//2]
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
    return matches

def calculate_double_elimination():
    matches = {
        'upper': [],
        'lower': []
            }
    byes = next_power_of_two(len(ss.teams)-1) - len(ss.teams) + 1
    bracket_dict = generate_double_elim_bracket(next_power_of_two(len(ss.teams)-1))
    count = 0
    participants = []
    
    for match in bracket_dict.keys():
        side = 'upper' if 'U' in match else 'lower'
        matches[side].append({
            "id": match,
            "name": "",
            "nextMatchId": bracket_dict[match]['upper'],
            "nextLooserMatchID": bracket_dict[match]['lower'],
            "tournamentRoundText": "",
            "state": "SCHEDULED",
            "participants": [{"id": "", "name": "Bob", "isWinner": True, "status": None, "resultsText": ""},
                             {"id": "", "name": "Joe", "isWinner": False, "status": None, "resultsText": ""}],
            "startTime": ""
            })
    return matches

matches = calculate_double_elimination()
st.write(matches)
# Render the bracket
bracket = tournament_bracket(matches=matches)