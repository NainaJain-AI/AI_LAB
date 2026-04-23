def pl_fc_entails(KB, facts, query):
    # count[c] = number of symbols in premise of clause c
    count = {}

    # inferred[s] = False initially
    inferred = {}

    # initialize inferred for all symbols
    for premises, conclusion in KB:
        for p in premises:
            inferred[p] = False
        inferred[conclusion] = False

    # queue = list of known facts
    queue = list(facts)

    # initialize count table
    for i in range(len(KB)):
        premises, conclusion = KB[i]
        count[i] = len(premises)

    # loop
    while len(queue) != 0:
        p = queue.pop(0)   # normal queue (FIFO)

        if p == query:
            return True

        if inferred[p] == False:
            inferred[p] = True

            # check all clauses
            for i in range(len(KB)):
                premises, conclusion = KB[i]

                if p in premises:
                    count[i] -= 1

                    if count[i] == 0:
                        queue.append(conclusion)

    return False
KB_a = [
    (["P"], "Q"),
    (["L", "M"], "P"),
    (["A", "B"], "L")
]

facts_a = ["A", "B", "M"]
query_a = "Q"

print(pl_fc_entails(KB_a, facts_a, query_a))  # True
KB_b = [
    (["A"], "B"),
    (["B"], "C"),
    (["C"], "D"),
    (["D", "E"], "F")
]

facts_b = ["A", "E"]
query_b = "F"

print(pl_fc_entails(KB_b, facts_b, query_b))  # True