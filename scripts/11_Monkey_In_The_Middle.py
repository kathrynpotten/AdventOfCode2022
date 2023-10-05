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
        return f"{self.name} has items {','.join(item for item in self.items)}"

    def inspect(self):
        item = self.items[0]
        self.items.remove(item)
        self.inspected += 1
        operation, value = self.operation
        if operation == "multiply":
            item *= value
        elif operation == "add":
            item += value
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


monkey_zero = Monkey(0, [79, 98], ("multiply", 19), 23, 2, 3)
item = monkey_zero.inspect()
recipient = monkey_zero.test_worry(item)
monkey_zero.throw_item(item)

monkey_three = Monkey(3, [74], ("add", 3), 17, 0, 1)
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
        operation = instructions[2].split("new = ")[-1]

    return monkeys
