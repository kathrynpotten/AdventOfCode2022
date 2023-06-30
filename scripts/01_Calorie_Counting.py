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

def calories_per_elf(elf):
    return sum(int(cals) for cals in elf.strip().split('\n'))

def most_calories(data):
    # calculate total calories per elf
    elves = data.strip().split('\n\n') 
    calories = [calories_per_elf(elf) for elf in elves]
    #keep max
    max_calories = 0	
    for i in range(len(calories)):
        total_calories_carried = calories[i]
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


def calories_top_three(data):
    elves = data.strip().split('\n\n')
    calories = [calories_per_elf(elf) for elf in elves]
    calories.sort(reverse=True)
    return sum(calories[:3])


assert calories_top_three(test_data) == test_result2

with open('./input_data/01_Calorie_Counting.txt', 'r', encoding="utf-8") as file:
    input = file.read()

answer_1 = most_calories(input)   
answer_2 = calories_top_three(input)

print(answer_1, answer_2)
    
    




    





