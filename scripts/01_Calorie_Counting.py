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
	# split data into elves
	calories = data.split('\n') 
	if calories.index('') == 0:
		calories = calories[1:]
	calories = [0 if cals == '' else int(cals) for cals in calories]
	max_calories = 0	
	for i in range(calories.count(0)):
		total_calories_carried = sum(calories[:calories.index(0)+1])
		calories = calories[calories.index(0)+1:]
		if total_calories_carried > max_calories:
			max_calories = total_calories_carried
	return max_calories

assert most_calories(test_data) == test_result


with open('./input_data/01_Calorie_Counting.txt', 'r', encoding="utf-8") as file:
	input = file.read()
	
print(most_calories(input))




	





