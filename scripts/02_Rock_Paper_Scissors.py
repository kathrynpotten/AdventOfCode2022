test_data = """
A Y
B X
C Z"""

test_result = 15
test_result2 = 12

"""
score_A = score_X = 1
score_B = score_Y = 2
score_C = score_Z = 3

loss = 0
draw = 3
win = 6         """

choice_scores = {'Rock':1,
          'Paper':2,
          'Scissors':3}
opponent_choice = {'A': 'Rock',
                   'B': 'Paper',
                   'C': 'Scissors'}
player_choice = {'X': 'Rock',
                 'Y': 'Paper',
                 'Z': 'Scissors'}
outcome_scores = {'win':6,'loss':0,'draw':3}

new_player_choice = {'X': 'loss',
                     'Y': 'draw',
                     'Z': 'win'}

wins = {('Rock','Paper'),
        ('Paper','Scissors'),
        ('Scissors','Rock')}
losses = {('Paper','Rock'),
          ('Scissors','Paper'),
          ('Rock','Scissors')}

def outcome(opponent,player):
    if (opponent, player) in wins:
        outcome = 'win'
    elif (opponent, player) in losses:
        outcome = 'loss'
    elif opponent == player:
        outcome = 'draw'
    return outcome

def score(opponent,player):
    outcome_score = outcome_scores[outcome(opponent,player)]
    player_score = choice_scores[player]
    return player_score + outcome_score


def choices(round):
    choice = round.split(' ')
    opponent, player = opponent_choice[choice[0]],player_choice[choice[1]]
    return opponent,player


def total_score(strategy_guide,parser):
    rounds = strategy_guide.strip().split('\n')
    scores = [score(*parser(round)) for round in rounds]
    return sum(scores)

assert total_score(test_data,choices) == test_result

with open('../input_data/02_Rock_Paper_Scissors.txt', 'r', encoding="utf-8") as file:
    input = file.read()

answer_1 = total_score(input,choices)
print(answer_1)


""" Part 2 """

""" if X, we lose - score of 0, and choose from losses set
if Y, we draw - score of 3, take same as opponent
if Z, we win - score of 6, and choose from wins set"""

win_dict = dict(wins)
loss_dict = dict(losses)

def new_choices(round):
    choice = round.split(' ')
    opponent, player_aim = opponent_choice[choice[0]],new_player_choice[choice[1]]
    if player_aim == 'draw':
        player = opponent
    elif player_aim == 'loss':
        player = loss_dict[opponent]
    elif player_aim == 'win':
        player = win_dict[opponent]    
    return player,player_aim


def new_score(player,player_aim):
    outcome_score = outcome_scores[player_aim]
    player_score = choice_scores[player]
    return player_score + outcome_score

def new_total_score(strategy_guide,parser):
    rounds = strategy_guide.strip().split('\n')
    scores = [new_score(*parser(round)) for round in rounds]
    return sum(scores)

assert new_total_score(test_data,new_choices) == test_result2

answer_2 = new_total_score(input,new_choices)
print(answer_2)
