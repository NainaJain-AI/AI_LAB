def backward_chaining(KB, facts, query):

    queue = [query]     # queue ← [q]
    inferred = set()    # inferred ← ∅

    while len(queue) != 0:
        p = queue.pop()   # p ← pop(queue)

        # if p is fact → continue
        if p in facts:
            continue

        # if already inferred → continue
        if p in inferred:
            continue

        inferred.add(p)   # inferred[p] = true

        # find rule whose conclusion is p
        found = False
        for premises, conclusion in KB:
            if conclusion == p:
                found = True

                # push all premises into queue
                for prem in premises:
                    queue.append(prem)

                break

        # if no rule found → return false
        if not found:
            return False

    return True
KB_a = [
    (["P"], "Q"),
    (["R"], "Q"),
    (["A"], "P"),
    (["B"], "R")
]

facts_a = ["A", "B"]
query_a = "Q"

print(backward_chaining(KB_a, facts_a, query_a))  # True
KB_b = [
    (["A"], "B"),
    (["B", "C"], "D"),
    (["E"], "C")
]

facts_b = ["A", "E"]
query_b = "D"

print(backward_chaining(KB_b, facts_b, query_b))  # True