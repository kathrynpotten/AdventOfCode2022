test_data = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

test_data_to_list = test_data.strip().split('\n')

rucksack1 = 'vJrwpWtwJgWrhcsFMMfFFhFp'

test_result = 157

def compartements(rucksack):
    first_compartement = rucksack[:int(len(rucksack)/2)]
    second_compartement = rucksack[int(len(rucksack)/2):]
    return first_compartement, second_compartement

assert compartements(rucksack1) == ('vJrwpWtwJgWr','hcsFMMfFFhFp')

def shared_item(rucksack):
    first_compartement, second_compartement = compartements(rucksack)
    item =  set(first_compartement).intersection(second_compartement)
    return item.pop()

assert shared_item(rucksack1) == 'p'

def assign_priority(item):
    priorities_lower = {chr(i+96): i for i in range(1,27)}
    priorities_upper = {chr(i+64): i+26 for i in range(1,27)}
    priorities = dict(priorities_lower,**priorities_upper)
    return priorities[item]

assert assign_priority('p') == 16

def priority_total(list):
    items = [shared_item(rucksack) for rucksack in list]
    priorities = [assign_priority(item) for item in items]
    return sum(priorities)

assert priority_total(test_data_to_list) == 157




def group_item(list):
    first_bag, second_bag, third_bag = list[0],list[1],list[2]
    items_1 =  set(first_bag).intersection(second_bag)
    group_item = items_1.intersection(third_bag)
    return group_item.pop()

def group_priorities(list):
    total_priority = 0
    for i in range(int(len(list)/3)):
        group_no = (i+1)*3
        group_list = list[group_no-3:group_no]
        item = group_item(group_list)
        total_priority += assign_priority(item)
    return total_priority

assert group_priorities(test_data_to_list) == 70


with open('../input_data/03_Rucksack_Reorganisation.txt', 'r', encoding="utf-8") as file:
    input = file.read().strip().split('\n')


answer_1 = priority_total(input)
print(answer_1)

answer_2 = group_priorities(input)
print(answer_2)
    
