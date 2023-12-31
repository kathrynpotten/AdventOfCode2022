import re
import numpy as np


test_data = """30373
25512
65332
33549
35390""".strip().split('\n')

test_result = 21
test_result_2 = 8


test_array = np.array([list(map(int, re.findall(r"[0-9]", line))) for line in test_data])




def visible_from_right(row):
    """ check row from RHS """
    visible = []
    for i in range(len(row)):
        if any(tree >= row[i] for tree in row[i+1:]):
            continue
        visible.append(i)
    return len(visible)    

assert visible_from_right([3,0,3,7,3]) == 2




def visible_from_left(row):
    """ check row from LHS """
    visible = []
    row.reverse()
    for i in range(len(row)):
        if any(tree >= row[i] for tree in row[i+1:]):
            continue
        visible.append(i)
    return len(visible)    

assert visible_from_left([3,0,3,7,3]) == 2




def is_visible(line):
    """ check if tree is visible """
    visible = []
    for i in range(len(line)):
        if any(tree >= line[i] for tree in line[i+1:]):
            continue
        visible.append(i)
    return visible   



def check_patch(array):
    """ takes a patch of trees and checks which trees are visible from the outside """
    visible = []

    #add any visible inner trees
    for index, row in enumerate(array):
        row_vis_rhs = is_visible(row)
        for tree in row_vis_rhs:
            visible.append((index,tree))
        
        row_vis_lhs = is_visible(row[::-1])
        row_vis_lhs = [len(row)-1-tree for tree in row_vis_lhs]
        for tree in row_vis_lhs:
            visible.append((index,tree))

    for index, column in enumerate(array.T):
        col_vis_top = is_visible(column[::-1])
        col_vis_top = [len(column)-1-tree for tree in col_vis_top]
        for tree in col_vis_top:
            visible.append((tree, index))

        col_vis_bottom = is_visible(column)
        for tree in col_vis_bottom:
            visible.append((tree,index))

    #remove duplicates and count
    return sorted(set(visible)), len(set(visible))



assert list(test_array.T[0]) == [3,2,6,3,3]

assert check_patch(test_array)[1] == test_result



with open('../input_data/08_Treetop_Tree_House.txt', 'r', encoding="utf-8") as file:
    input_file = file.read().strip().split('\n')


input_array = np.array([list(map(int, re.findall(r"[0-9]", line))) for line in input_file])


answer_1 = check_patch(input_array)[1]
print(answer_1)




""" Part 2 """

def scenic(line):
    """ check how many trees are visible from current posiiton """
    visible = []
    count = 0
    for i in range(1,len(line)):
        count +=1
        if line[i] < line[0]:
            visible.append(i)
        else:
            visible.append(i)
            break
    return len(visible)

def scenic_score(tree, array):
    """ calculate scenic score from tree of choice """
    i, j = tree
    score = 1
    score *= scenic(np.flip(array[i][:j+1]))
    score *= scenic(array[i][j:])
    score *= scenic(array.T[j][i:])
    score *= scenic(np.flip(array.T[j][:i+1]))
    return score

assert scenic_score((1,2), test_array) == 4
assert scenic_score((3,2), test_array) == 8


def max_scenic_score(array):
    """ calculate maximum scenic score in given tree patch """
    rows, columns = np.shape(array)
    scores = []
    for i in range(rows):
        for j in range(columns):
            score = scenic_score((i,j), array)
            scores.append(score)
    return max(scores)


assert max_scenic_score(test_array) == 8
    

answer_2 = max_scenic_score(input_array)
print(answer_2)
