""" Timing code """

import timeit
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

    def take_turn(self, manage_worry=True):
        # inspect
        old = self.items[0]
        self.items.remove(old)
        self.inspected += 1
        item = eval(self.operation)
        if manage_worry:
            item = math.floor(item / 3)
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

setup = """
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

    def take_turn(self, manage_worry=True):
        # inspect
        old = self.items[0]
        self.items.remove(old)
        self.inspected += 1
        item = eval(self.operation)
        if manage_worry:
            item = math.floor(item / 3)
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

monkeys = [Monkey(0, [79, 98], "old * 19", 23, 2, 3), Monkey(1, [54, 65, 75, 74], "old + 6", 19, 2, 0), Monkey(2, [79, 60, 97], "old * old", 13, 1, 3), Monkey(3, [74], "old + 3", 17, 0, 1)]

def round_v1(monkeys, manage_worry=True):
    for monkey in monkeys:
        for _ in range(len(monkey.items)):
            recipient, item = monkey.take_turn(manage_worry)
            monkeys[recipient].catch_item(item)
    return monkeys


def round_v2(monkeys, manage_worry=True):
    for monkey in monkeys:
        for _ in range(len(monkey.items)):
            item = monkey.inspect(manage_worry)
            recipient = monkey.test_worry(item)
            monkey.throw_item(item)
            monkeys[recipient].catch_item(item)
    return monkeys

def play_monkey_in_the_middle_v1(rounds, monkeys, manage_worry=True):


    for _ in range(rounds):
        monkeys = round_v1(monkeys, manage_worry)

    inspections = [monkey.inspected for monkey in monkeys]
    inspections.sort(reverse=True)
    monkey_business = inspections[0] * inspections[1]

    return monkey_business


def play_monkey_in_the_middle_v2(rounds, monkeys, manage_worry=True):


    for _ in range(rounds):
        monkeys = round_v2(monkeys, manage_worry)

    inspections = [monkey.inspected for monkey in monkeys]
    inspections.sort(reverse=True)
    monkey_business = inspections[0] * inspections[1]

    return monkey_business

"""

stmt = "play_monkey_in_the_middle_v1(100, monkeys, False)"

print(timeit.timeit(stmt, setup, number=10))

stmt2 = "play_monkey_in_the_middle_v2(100, monkeys, False)"

print(timeit.timeit(stmt2, setup, number=10))


setup = """
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

    def take_turn(self, manage_worry=True):
        # inspect
        old = self.items[0]
        self.items.remove(old)
        self.inspected += 1
        item = eval(self.operation)
        if manage_worry:
            item = math.floor(item / 3)
            worry = item % self.test
        else:
            worry = item % self.test
        # test worry
        if worry == 0:
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

monkeys = [Monkey(0, [79, 98], "old * 19", 23, 2, 3), Monkey(1, [54, 65, 75, 74], "old + 6", 19, 2, 0), Monkey(2, [79, 60, 97], "old * old", 13, 1, 3), Monkey(3, [74], "old + 3", 17, 0, 1)]

def round(monkeys, manage_worry=True):
    for monkey in monkeys:
        for _ in range(len(monkey.items)):
            recipient, item = monkey.take_turn(manage_worry)
            monkeys[recipient].catch_item(item)
    return monkeys


def play_monkey_in_the_middle(rounds,monkeys, manage_worry=True):

    for _ in range(rounds):
        monkeys = round(monkeys, manage_worry)

    inspections = [monkey.inspected for monkey in monkeys]
    inspections.sort(reverse=True)
    monkey_business = inspections[0] * inspections[1]

    return monkey_business


"""

stmt = "play_monkey_in_the_middle(100, monkeys, False)"

print(timeit.timeit(stmt, setup, number=10))
