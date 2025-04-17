import math

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
    grand_final = f'M{match_id}'
    match_dict[grand_final] = {'upper': None, 'lower': None}
    match_dict[final_w]['upper'] = grand_final
    match_dict[final_l]['upper'] = grand_final

    return match_dict

print(generate_double_elim_bracket(64))