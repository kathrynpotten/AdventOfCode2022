import ast

test_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".strip()


def compare_list(left, right):
    correct_order = "no decision"
    if len(left) == 0 and len(right) > 0:
        correct_order = True
    for i in range(len(left)):
        try:
            if left[i] > right[i]:
                correct_order = False
                break
            elif left[i] < right[i]:
                correct_order = True
                break
        except IndexError:
            correct_order = False

    return correct_order


example_left = [1, 1, 3, 1, 1]
example_right = [1, 1, 5, 1, 1]
assert compare_list(example_left, example_right) == True


def compare_pairs(left, right):
    correct_order = "no decision"
    for i in range(len(left)):
        try:
            if type(left[i]) != type(right[i]):
                if type(left[i]) == int:
                    left_item = [left[i]]
                    right_item = right[i]
                elif type(right[i]) == int:
                    right_item = [right[i]]
                    left_item = left[i]
            else:
                left_item = left[i]
                right_item = right[i]

            if type(left_item) == list:
                if any(isinstance(element, list) for element in left_item):
                    list_order = compare_pairs(left_item, right_item)
                    if list_order != "no decision":
                        correct_order = list_order
                        break
                elif any(isinstance(element, list) for element in right_item):
                    list_order = compare_pairs(left_item, right_item)
                    if list_order != "no decision":
                        correct_order = list_order
                        break
                else:
                    list_order = compare_list(left_item, right_item)
                    if list_order != "no decision":
                        correct_order = list_order
                        break

            elif type(left_item) == int:
                if left_item > right_item:
                    correct_order = False
                    break
                elif left_item < right_item:
                    correct_order = True
                    break

        except IndexError:
            correct_order = False

    if correct_order == "no decision":
        correct_order = True

    return correct_order


assert compare_pairs(example_left, example_right) == True

example_left_2 = [[1], [2, 3, 4]]
example_right_2 = [[1], [4]]


assert compare_pairs(example_left_2, example_right_2) == True

example_left_3 = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
example_right_3 = [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]


assert compare_pairs(example_left_3, example_right_3) == False

example_left_4 = [9]
example_right_4 = [[8, 7, 6]]

assert compare_pairs(example_left_4, example_right_4) == False


def indices_sum_correct_order(pairs):
    indices_sum = 0
    indices_list = []
    for index, pair in enumerate(pairs):
        left, right = pair[0], pair[1]
        correct_order = compare_pairs(left, right)
        if correct_order:
            indices_list.append(index + 1)
            indices_sum += index + 1
    return indices_sum, indices_list


def input_to_pairs(input):
    pairs = []
    pairs_list = input.split("\n\n")
    pairs_strings = [pairs.split("\n") for pairs in pairs_list]
    for str_pair in pairs_strings:
        pair = [ast.literal_eval(str_list) for str_list in str_pair]
        pairs.append(pair)
    return pairs


assert input_to_pairs(test_data)[0] == [[1, 1, 3, 1, 1], [1, 1, 5, 1, 1]]


test_pairs = input_to_pairs(test_data)
assert indices_sum_correct_order(test_pairs)[1] == [1, 2, 4, 6]
assert indices_sum_correct_order(test_pairs)[0] == 13

with open("../input_data/13_Distress_Signal.txt", "r", encoding="utf-8") as file:
    input_pairs = input_to_pairs(file.read().strip())

example_pair = input_pairs[25]
ex_left, ex_right = example_pair[0], example_pair[1]


answer_1 = indices_sum_correct_order(input_pairs)
print(answer_1)
