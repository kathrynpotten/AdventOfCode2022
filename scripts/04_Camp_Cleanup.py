test_data = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

test_result = 2

test_data_to_list = test_data.strip().split('\n')

test_pair = """2-4,6-8"""




def convert_to_tuples(pair):
    return tuple(pair.split(','))

assert convert_to_tuples(test_pair) == ('2-4','6-8')
 


def task_compare_inclusive(pair):
    elf1,elf2 = pair
    elf1_tasks = [int(task) for task in elf1.split('-')]
    elf2_tasks = [int(task) for task in elf2.split('-')]
    elf1_range = list(range(elf1_tasks[0],elf1_tasks[1]+1))
    elf2_range = list(range(elf2_tasks[0],elf2_tasks[1]+1))
    if all(tasks in elf2_range for tasks in elf1_range):
        return True
    elif all(tasks in elf1_range for tasks in elf2_range):
        return True
    else:
        return False

assert task_compare_inclusive(('2-4','6-8')) == False

def pairs_included(list):
    pairs = [tuple(pair.split(',')) for pair in list]
    included = [task_compare_inclusive(pair) for pair in pairs]
    return sum(included)

assert pairs_included(test_data_to_list) == test_result



with open('../input_data/04_Camp_Cleanup.txt', 'r', encoding="utf-8") as file:
    input = file.read().strip().split('\n')

answer_1 = pairs_included(input)
print(answer_1)
