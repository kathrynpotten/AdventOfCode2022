test_data = """
A Y
B X
C Z"""

test_result = 15

"""
score_A = score_X = 1
score_B = score_Y = 2
score_C = score_Z = 3

loss = 0
draw = 3
win = 6         """

scores = {'A':1,'B':2,'C':3, 'X':1,'Y':2,'Z':3}

def convert_to_score(input):
    return [scores.get(val) for val in input]

def select_round(rounds):
    # split into separate rounds
    rounds_list = rounds.strip().split('\n')
    rounds = []
    for i in range(len(rounds_list)):
        round = rounds_list[i].split(' ')
        rounds.append(round)
    return rounds

def total_score(strategy_guide):
    # split into separate rounds
    rounds = select_round(strategy_guide)
    # convert letters into scores
    scores_list = [convert_to_score(round) for round in rounds]
    # calculate total score
    total_score = 0
    for round in scores_list:
        if round[1] > round[0]:
            total_score += 6 + round[1]
        elif round[1] == round[0]:
            total_score += 3 + round[1]
        elif round[1] < round[0]:
            total_score += 0 + round[1]
    return total_score

assert total_score(test_data) == test_result


