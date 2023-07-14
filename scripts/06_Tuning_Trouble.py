test_data_1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
test_data_2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
test_data_3 = "nppdvjthqldpwncqszvftbrmjlhg"
test_data_4 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
test_data_5 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"

test_result_1 = 7
test_result_2 = 5
test_result_3 = 6
test_result_4 = 10
test_result_5 = 11

test_result2_1 = 19
test_result2_2 = 23
test_result2_3 = 23
test_result2_4 = 29
test_result2_5 = 26



def check_duplicates(chars, number):
    """ for a set of characters of given length, check if any repeats found within"""
    if len(set(chars)) == number:
        return False
    else:
        return True
    
assert check_duplicates('mjqj',4) == True
assert check_duplicates('jpqm',4) == False
 
def split_signal(signal,number):
    """ split signal into sets of characters of given length """
    return [signal[i:i+number] for i in range(len(signal)-3)]

assert split_signal('mjqjpqmg',4) == ['mjqj','jqjp','qjpq','jpqm','pqmg']

def marker(signal,number):
    """ find and return end character of marker of given length """
    chars = split_signal(signal,number)
    for char_str,index in zip(chars,range(0,len(chars))):
        if check_duplicates(char_str,number) == False:
            return index+number
        else:
            continue
    return False

assert marker('mjqj',4) == False
assert marker('jpqm',4) == 4



assert marker(test_data_1,4) == test_result_1
assert marker(test_data_2,4) == test_result_2
assert marker(test_data_3,4) == test_result_3
assert marker(test_data_4,4) == test_result_4
assert marker(test_data_5,4) == test_result_5



assert marker(test_data_1,14) == test_result2_1
assert marker(test_data_2,14) == test_result2_2
assert marker(test_data_3,14) == test_result2_3
assert marker(test_data_4,14) == test_result2_4
assert marker(test_data_5,14) == test_result2_5

with open('../input_data/06_Tuning_Trouble.txt', 'r', encoding="utf-8") as file:
    input = file.read()

answer_1 = marker(input,4)
print(answer_1)    

answer_2 = marker(input,14)
print(answer_2)