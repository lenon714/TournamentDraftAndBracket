from __init__ import *

st.set_page_config(
    layout="wide"
)

ss.teams = ss.sorted_teams
ss.team_score = ss.match_states[ss.current_match]

st.write("# This is the Bracket")

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
    match_dict = {}
    num_rounds = int(math.log2(num_teams))

    winners = []
    losers = []
    round_text = []

    # === Generate Winners Bracket ===
    w_match_id = 1
    for r in range(num_rounds):
        round_matches = []
        num_matches = num_teams // (2 ** (r + 1))
        for i in range(num_matches):
            label = f'W{w_match_id}'
            match_dict[label] = {'upper': None, 'lower': None}
            round_text.append(2 * (r - 1) - (r - 3) * (r < 3))
            round_matches.append(label)
            w_match_id += 1
        winners.append(round_matches)

    # === Generate Losers Bracket ===
    l_match_id = 1
    losers_per_round = [num_teams // 4]

    # Each subsequent losers round merges two previous matches
    for i in range(num_rounds + 1):
        if not i % 2:
            losers_per_round.append(losers_per_round[-1])
        else:
            if losers_per_round[-1] // 2 == 0:
                break
            losers_per_round.append(losers_per_round[-1] // 2)

    for r, count in enumerate(losers_per_round):
        round_matches = []
        for i in range(count):
            label = f'L{l_match_id}'
            match_dict[label] = {'upper': None, 'lower': None}
            round_text.append(str(r+1))
            round_matches.append(label)
            l_match_id += 1
        losers.append(round_matches)

    # === Wiring Winners to Winners and Losers ===
    for r, matches in enumerate(winners[:-1]):
        next_w = winners[r + 1]
        loser_r = losers[r]
        for i, match in enumerate(matches):
            match_dict[match]['upper'] = next_w[i // 2]
            if r % 2:
                match_dict[match]['lower'] = loser_r[i]
            else:
                match_dict[match]['lower'] = loser_r[i // 2]

    # Final Winners match goes to GF and to last losers round
    final_w = winners[-1][0]
    match_dict[final_w]['upper'] = 'GF'
    match_dict[final_w]['lower'] = losers[-1][0]

    # === Wiring Losers Bracket ===
    for r in range(len(losers) - 1):
        for i, match in enumerate(losers[r]):
            if not r % 2:
                match_dict[match]['upper'] = losers[r + 1][i]
            else:
                match_dict[match]['upper'] = losers[r + 1][i // 2]

    # Last losers match goes to GF
    match_dict[losers[-1][0]]['upper'] = 'GF'

    # === Grand Final and Reset ===
    match_dict['GF'] = {'upper': 'GFR', 'lower': None}
    match_dict['GFR'] = {'upper': None, 'lower': None}
    round_text.append('Grand Finals')
    round_text.append('Grand Finals Reset')

    return match_dict, round_text

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
    bracket_dict, round_text = generate_double_elim_bracket(next_power_of_two(len(ss.teams)-1))
    count = 0
    team_list = [team['header'] for team in ss.teams[1:]]
    participants = []
    matchups = []
    for i, team in enumerate(ss.teams[1::]):
        if count <= 1:
            if byes > 0:
                participants.append({"id": team['header'], "name": team['header'], "isWinner": True, "status": None, "resultText": "BYE"})
                count += 1
                byes -= 1
            else:
                participants.append({"id": team['header'], "name": team['header'], "isWinner": False, "status": None, "resultText": "0"})
            count += 1
        if count > 1:
            matchups.append(participants)
            count = 0
            participants = []

    for i, match in enumerate(bracket_dict.keys()):
        if i >= len(matchups):
            matchups.append([])
        side = 'upper' if 'W' in match else 'lower'
        try:
            state = 'SCORE_DONE' if (matchups[i][0]['isWinner'] or matchups[i][1]['isWinner']) else 'SCHEDULED'
        except:
            state = 'SCHEDULED'

        matches[side].append({
            "id": match,
            "name": match,
            "nextMatchId": bracket_dict[match]['upper'],
            "nextLoserMatchID": bracket_dict[match]['lower'],
            "tournamentRoundText": round_text[i],
            "state": state,
            "participants": matchups[i],
            "startTime": ""
            })
    return matches

def update_double_elim(matches):
    # Setups up next match in bracket
    for bracket in matches.keys():
        for match in matches[bracket]:
            if match['state'] == 'SCORE_DONE':
                # Grand Finals Edge Case
                if 'GF' in match['nextMatchId']:
                    match_idx = -2 if match['nextMatchId'] == 'GF' else -1
                    next_match_team = matches['lower'][match_idx]['participants']
                    for m in range(len(match['participants'])):
                        teams = [t['id'] for t in next_match_team]
                        if (match['participants'][m]['isWinner'] or match_idx == -1) and match['participants'][m]['id'] not in teams :
                            next_match_team.append(match['participants'][m].copy())
                            next_match_team[-1]['isWinner'] = False
                            next_match_team[-1]['status'] = None
                            next_match_team[-1]['resultText'] = ""
                            break

                # Move winners
                for i, next_match in enumerate(matches[bracket]):
                    if next_match['id'] == match['nextMatchId']:
                        for j in range(len(match['participants'])):
                            teams = [t['id'] for t in next_match['participants']]
                            if match['participants'][j]['isWinner'] and match['participants'][j]['id'] not in teams:
                                matches[bracket][i]['participants'].append(match['participants'][j].copy())
                                matches[bracket][i]['participants'][-1]['isWinner'] = False
                                matches[bracket][i]['participants'][-1]['status'] = None
                                matches[bracket][i]['participants'][-1]['resultText'] = ""
                                break
                        break

                # Move losers
                for k, next_match in enumerate(matches['lower']):
                    if next_match['id'] == match['nextLoserMatchID']:
                        for l in range(len(match['participants'])):
                            teams = [t['id'] for t in next_match['participants']]
                            if not match['participants'][l]['isWinner'] and match['participants'][l]['id'] not in teams:
                                matches['lower'][k]['participants'].append(match['participants'][l].copy())
                                matches['lower'][k]['participants'][-1]['status'] = None
                                matches['lower'][k]['participants'][-1]['resultText'] = "0"
                                break
                        break
    return matches

if ss.matches == {'upper': [], 'lower': []}:
    ss.matches = calculate_double_elimination()
    
ss.matches = update_double_elim(ss.matches)

# Render the bracket
if ss.matches != {'upper': [], 'lower': []}:
    bracket = tournament_bracket(matches=ss.matches)

st.write(ss.matches)