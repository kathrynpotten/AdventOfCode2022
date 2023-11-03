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
    for i in range(len(left)):
        if left[i] > right[i]:
            # print("Error! Inputs in wrong order")
            correct_order = False
            break
        elif left[i] < right[i]:
            correct_order = True
            break

    return correct_order


example_left = [1, 1, 3, 1, 1]
example_right = [1, 1, 5, 1, 1]
assert compare_list(example_left, example_right) == True


def compare_pairs(left, right):
    correct_order = "no decision"
    for i in range(len(left)):
        print(left[i], right[i])
        try:
            if type(left[i]) != type(right[i]):
                left_item = [left[i]]
                right_item = [right[i]]
                list_order = compare_list(left_item, right_item)
                if list_order != "no decision":
                    correct_order = list_order
                    break
            elif type(left[i]) == list:
                list_order = compare_list(left[i], right[i])
                if list_order != "no decision":
                    correct_order = list_order
                    break
            elif type(left[i]) == int:
                if left[i] > right[i]:
                    # print("Error! Inputs in wrong order")
                    correct_order = False
                    break
                elif left[i] < right[i]:
                    correct_order = True
                    break
        except IndexError:
            correct_order = False

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
    for index, pair in enumerate(pairs):
        left, right = pair[0], pair[1]
        correct_order = compare_pairs(left, right)
        if correct_order:
            indices_sum += index
    return indices_sum


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
# assert indices_sum_correct_order(test_pairs) == 13
