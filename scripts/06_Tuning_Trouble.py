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



def check_duplicates(chars):
    """ for a set of 4 characters, check if any repeats found within"""
    if len(set(chars)) == 4:
        return False
    else:
        return True
    
assert check_duplicates('mjqj') == True
assert check_duplicates('jpqm') == False
 
def split_signal(signal):
    """ split signal into sets of 4 characters """
    return [signal[i:i+4] for i in range(len(signal)-3)]

assert split_signal('mjqjpqmg') == ['mjqj','jqjp','qjpq','jpqm','pqmg']

def start_of_packet_marker(signal):
    """ find and return start-of-packet marker """
    chars = split_signal(signal)
    for char_str,index in zip(chars,range(0,len(chars))):
        if check_duplicates(char_str) == False:
            return index+4
        else:
            continue
    return False

assert start_of_packet_marker('mjqj') == False
assert start_of_packet_marker('jpqm') == 4



assert start_of_packet_marker(test_data_1) == test_result_1
assert start_of_packet_marker(test_data_2) == test_result_2
assert start_of_packet_marker(test_data_3) == test_result_3
assert start_of_packet_marker(test_data_4) == test_result_4
assert start_of_packet_marker(test_data_5) == test_result_5


with open('../input_data/06_Tuning_Trouble.txt', 'r', encoding="utf-8") as file:
    input = file.read()

answer_1 = start_of_packet_marker(input)
print(answer_1)    