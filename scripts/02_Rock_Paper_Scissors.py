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

scores = {'A':1,'B':2,'C':3,
          'X':1,'Y':2,'Z':3}
outcomes = {'win':6,'loss':0,'draw':3}


def convert_to_score(round):
    return [scores.get(val) for val in round]

def outcome(round_val):
    opponent, player = round_val[0], round_val[1]
    if player > opponent:
        outcome = 'win'
    elif player < opponent:
        outcome = 'loss'
    elif player == opponent:
        outcome = 'draw'
    return outcome

def score(round_val):
    opponent, player = round_val[0], round_val[1]
    return player + outcomes.get(outcome(round_val))


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
    converted = [convert_to_score(round) for round in rounds]
    # calculate score per round
    scores = [score(round) for round in converted]
    return sum(scores)


assert total_score(test_data) == test_result

with open('C:/Users/Kathryn/OneDrive/dev/AdventOfCode2022/input_data/02_Rock_Paper_Scissors.txt', 'r', encoding="utf-8") as file:
    input = file.read()

answer_1 = total_score(input)
print(answer_1)




