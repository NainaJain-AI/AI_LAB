# -----------------------------
# Symbol Class
# -----------------------------
class Symbol:
    def __init__(self, name):
        if name.startswith('~'):
            self.name = name[1:]
            self.negated = True
        else:
            self.name = name
            self.negated = False

    def evaluate(self, values):
        val = values[self.name]
        return not val if self.negated else val

    def __repr__(self):
        return ('~' if self.negated else '') + self.name


# -----------------------------
# Operator Function
# -----------------------------
def apply_operator(op, a, b):
    if op == '∧':
        return a and b
    elif op == '∨':
        return a or b
    elif op == '→':
        return (not a) or b
    elif op == '↔':
        return a == b


# -----------------------------
# Precedence
# -----------------------------
precedence = {
    '∧': 2,
    '∨': 1,
    '→': 0,
    '↔': 0
}


# -----------------------------
# Infix → Postfix
# -----------------------------
def infix_to_postfix(tokens):
    output = []
    stack = []

    print("\nTRACE (Infix → Postfix):")

    for token in tokens:
        if isinstance(token, Symbol):
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

        else:
            while (stack and stack[-1] != '(' and
                   precedence.get(token, 0) <= precedence.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)

        print(f"{token} | Stack: {stack} | Output: {output}")

    while stack:
        output.append(stack.pop())
        print(f"POP | Stack: {stack} | Output: {output}")

    print("Postfix:", output)
    return output


# -----------------------------
# Evaluate Postfix (normal)
# -----------------------------
def evaluate_postfix(postfix, values):
    stack = []

    for token in postfix:
        if isinstance(token, Symbol):
            stack.append(token.evaluate(values))
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_operator(token, a, b))

    return stack[0]


# -----------------------------
# Generate Values
# -----------------------------
def generate_values(symbols):
    names = sorted(list(set([s.name for s in symbols])))
    n = len(names)

    total = 2 ** n
    combinations = []

    for i in range(total):
        values = {}
        for j in range(n):
            bit = (i >> j) & 1
            values[names[j]] = bool(bit)
        combinations.append(values)

    return combinations, names


# -----------------------------
# Truth Table
# -----------------------------
def truth_table(expr_tokens, symbols):
    postfix = infix_to_postfix(expr_tokens)
    combinations, names = generate_values(symbols)

    infix_str = " ".join(str(t) for t in expr_tokens)
    postfix_str = " ".join(str(t) for t in postfix)

    print("\nEXPRESSION:", infix_str)
    print("POSTFIX:", postfix_str)

    print("\nTRACE (Postfix Evaluation for ALL rows)\n")

    for val_dict in combinations:
        print(val_dict)
        stack = []

        for token in postfix:
            if isinstance(token, Symbol):
                stack.append(token.evaluate(val_dict))
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(apply_operator(token, a, b))

            print(f"{token} | Stack: {stack}")
        print()

    print("TRUTH TABLE\n")

    print(" | ".join(names) + " | " + infix_str)
    print("-" * (len(names) * 4 + len(infix_str)))

    for val_dict in combinations:
        result = evaluate_postfix(postfix, val_dict)

        row = ["T" if val_dict[n] else "F" for n in names]
        print(" | ".join(row) + " | " + ("T" if result else "F"))

    print("\n=============================\n")


# -----------------------------
# Symbols
# -----------------------------
P = Symbol('P')
Q = Symbol('Q')
R = Symbol('R')


# -----------------------------
# ALL EXPRESSIONS
# -----------------------------

expr1 = [Symbol('~P'), '→', Q]

expr2 = [Symbol('~P'), '∧', Symbol('~Q')]

expr3 = [Symbol('~P'), '∨', Symbol('~Q')]

expr4 = [Symbol('~P'), '→', Symbol('~Q')]

expr5 = [Symbol('~P'), '↔', Symbol('~Q')]

expr6 = ['(', P, '∨', Q, ')', '∧', '(', Symbol('~P'), '→', Q, ')']

expr7 = ['(', P, '∨', Q, ')', '→', Symbol('~R')]

expr8 = [
    '(', '(', P, '∨', Q, ')', '→', Symbol('~R'), ')',
    '↔',
    '(', '(', Symbol('~P'), '∧', Symbol('~Q'), ')', '→', Symbol('~R'), ')'
]

expr9 = [
    '(', '(', P, '→', Q, ')', '∧', '(', Q, '→', R, ')', ')',
    '→',
    '(', Q, '→', R, ')'
]

# FIXED Q10 (important grouping)
expr10 = [
    '(', P, '→', '(', Q, '∨', R, ')', ')',
    '→',
    '(',
        '(', Symbol('~P'), '∧', Symbol('~Q'), ')',
        '∧',
        Symbol('~R'),
    ')'
]


# -----------------------------
# RUN ALL
# -----------------------------
truth_table(expr1, [P, Q])
truth_table(expr2, [P, Q])
truth_table(expr3, [P, Q])
truth_table(expr4, [P, Q])
truth_table(expr5, [P, Q])
truth_table(expr6, [P, Q])
truth_table(expr7, [P, Q, R])
truth_table(expr8, [P, Q, R])
truth_table(expr9, [P, Q, R])
truth_table(expr10, [P, Q, R])