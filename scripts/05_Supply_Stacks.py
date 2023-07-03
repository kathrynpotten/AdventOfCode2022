test_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

test_result = 'CMZ'


#test_data_to_list = test_data.split('\n')
#test_moves = [item for item in test_data_to_list if item[:4] == 'move']

test_instruction = "move 1 from 2 to 1"

# decode instructions
def decode_move(move):
    return tuple([int(s) for s in move.split() if s.isdigit()])    

assert decode_move(test_instruction) == (1,2,1)

#decode start position
def start_position(input):
    crates = input.split('\n')
    indices = [int(x) for x in crates.pop().split()]
    stacks = [[] for i in indices]
    crates.reverse()
    for line in crates:
            crates = line[1::4]
            for crate, index in zip(crates,indices):
                 if crate != ' ':
                      stacks[index-1] += crate

    return stacks



def parse_input(data):
    input,instructions = data.split('\n\n')
    start = start_position(input)
    moves = [decode_move(move) for move in instructions.strip().split('\n')]
    return start, moves

#print(start_position(test_data.split('\n\n')[0]))

def make_move(position,move):
    quantity,origin,end = move
    new_position = position
    for _ in range(quantity):
          new_position[end-1].append(new_position[origin-1][-1])
          new_position[origin-1].pop()
    return new_position

def rearrange_outcome(data):
    start, moves = parse_input(data)
    next = start
    for move in moves:
        end = make_move(next,move)
        next = end
    top_of_pile = ''
    for stack in next:
         top_of_pile += stack[-1]
    return top_of_pile


assert rearrange_outcome(test_data) == test_result


with open('../input_data/05_Supply_Stacks.txt', 'r', encoding="utf-8") as file:
    input = file.read()

answer_1 = rearrange_outcome(input)
print(answer_1)     

    
    
    
    

