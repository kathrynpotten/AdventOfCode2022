import math
import re

test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()


class Monkey:
    def __init__(self, name, items, operation, test, true_throw, false_throw):
        self.name = name
        self.items = items
        self.operation = operation
        self.test = test
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspected = 0

    def __repr__(self):
        return f"Monkey {self.name} has items {', '.join(str(item) for item in self.items)}"

    def take_turn(self, test_condition=100, manage_worry=True):
        # inspect
        old = self.items[0]
        self.items.remove(old)
        self.inspected += 1
        item = eval(self.operation)
        if manage_worry:
            item = math.floor(item / 3)
        else:
            item = item % test_condition
        # test worry
        if item % self.test == 0:
            recipient = self.true_throw
        else:
            recipient = self.false_throw
        # throw item
        return recipient, item

    def inspect(self, manage_worry=True):
        old = self.items[0]
        self.items.remove(old)
        self.inspected += 1
        item = eval(self.operation)
        if manage_worry:
            item = math.floor(item / 3)
        self.items.append(item)
        return item

    def test_worry(self, item):
        if item % self.test == 0:
            recipient = self.true_throw
        else:
            recipient = self.false_throw
        return recipient

    def throw_item(self, item):
        self.items.remove(item)

    def catch_item(self, item):
        self.items.append(item)


monkey_zero = Monkey(0, [79, 98], "old * 19", 23, 2, 3)
item = monkey_zero.inspect()
recipient = monkey_zero.test_worry(item)
monkey_zero.throw_item(item)

monkey_three = Monkey(3, [74], "old + 3", 17, 0, 1)
monkey_three.catch_item(item)

assert monkey_zero.items == [98]
assert monkey_three.items == [74, 500]


def parse_input(text):
    monkeys_input = text.split("Monkey ")[1:]
    monkeys = []
    for monkey in monkeys_input:
        name = monkey[0]
        instructions = monkey.split("\n")
        items = re.findall("\d+", instructions[1])
        items = [int(item) for item in items]
        operation = instructions[2].split("new = ")[-1]
        test = int(re.findall("\d+", instructions[3])[0])
        true_throw = int(instructions[4].split("monkey ")[-1])
        false_throw = int(instructions[5].split("monkey ")[-1])
        monkeys.append(Monkey(name, items, operation, test, true_throw, false_throw))
    return monkeys


monkeys = parse_input(test_data)
assert str(monkeys[0]) == "Monkey 0 has items 79, 98"
assert str(monkeys[1]) == "Monkey 1 has items 54, 65, 75, 74"
assert str(monkeys[2]) == "Monkey 2 has items 79, 60, 97"
assert str(monkeys[3]) == "Monkey 3 has items 74"


def round(monkeys, test_condition=100, manage_worry=True):
    for monkey in monkeys:
        for _ in range(len(monkey.items)):
            recipient, item = monkey.take_turn(test_condition, manage_worry)
            monkeys[recipient].catch_item(item)
    return monkeys


monkeys = round(monkeys)
assert str(monkeys[0]) == "Monkey 0 has items 20, 23, 27, 26"
assert str(monkeys[1]) == "Monkey 1 has items 2080, 25, 167, 207, 401, 1046"
assert str(monkeys[2]) == "Monkey 2 has items "
assert str(monkeys[3]) == "Monkey 3 has items "


def play_monkey_in_the_middle(rounds, input_data, manage_worry=True):
    monkeys = parse_input(input_data)
    test_condition = math.lcm(*(monkey.test for monkey in monkeys))

    for i in range(rounds):
        if i % 100 == 0 and i > 0:
            print(f"Running round {i}")
        monkeys = round(monkeys, test_condition, manage_worry)

    inspections = [monkey.inspected for monkey in monkeys]
    inspections.sort(reverse=True)
    monkey_business = inspections[0] * inspections[1]

    return monkey_business


assert play_monkey_in_the_middle(20, test_data) == 10605

assert play_monkey_in_the_middle(1, test_data, False) == 24
assert play_monkey_in_the_middle(20, test_data, False) == 103 * 99
assert play_monkey_in_the_middle(1000, test_data, False) == 5204 * 5192
assert play_monkey_in_the_middle(10000, test_data, False) == 2713310158


with open("../input_data/11_Monkey_In_The_Middle.txt", "r", encoding="utf-8") as file:
    input = file.read().strip()


answer_1 = play_monkey_in_the_middle(20, input)
print(answer_1)

answer_2 = play_monkey_in_the_middle(10000, input, False)
print(answer_2)
