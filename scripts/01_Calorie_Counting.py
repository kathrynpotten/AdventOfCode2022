test_data = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

test_result = 24000
test_result2 = 45000


def most_calories(data):
    # split data into elves and convert into integers
    calories = data.strip().split('\n') 
    calories = [0 if cals == '' else int(cals) for cals in calories]
    #calculate total calories per elf and keep max
    max_calories = 0	
    for i in range(calories.count(0)):
        total_calories_carried = sum(calories[:calories.index(0)+1])
        calories = calories[calories.index(0)+1:]
        if total_calories_carried > max_calories:
            max_calories = total_calories_carried
    total_calories_carried = sum(calories)
    if total_calories_carried > max_calories:
            max_calories = total_calories_carried
    return max_calories

assert most_calories(test_data) == test_result

test_data_new = """
1000
2000
3000

10000"""

assert most_calories(test_data_new) == 10000

with open('./input_data/01_Calorie_Counting.txt', 'r', encoding="utf-8") as file:
    input = file.read()
    
print(most_calories(input))


def calories_per_elf(data):
    calories = data.strip().split('\n') 
    calories = [0 if cals == '' else int(cals) for cals in calories]
    #calculate total calories per elf
    calories_per_elf = []
    for i in range(calories.count(0)):
        total_calories_carried = sum(calories[:calories.index(0)+1])
        calories = calories[calories.index(0)+1:]
        calories_per_elf.append(total_calories_carried)
    total_calories_carried_final = sum(calories)
    calories_per_elf.append(total_calories_carried_final)
    return calories_per_elf

def calories_top_three(data):
    calories = calories_per_elf(data)
    calories.sort(reverse=True)
    return sum(calories[:3])


assert calories_top_three(test_data) == test_result2

print(calories_top_three(input))
    
    




    





