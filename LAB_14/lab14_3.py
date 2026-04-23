def pl_resolve(Ci, Cj):
    resolvents = []

    for li in Ci:
        for lj in Cj:

            # check complementary literals
            if li == negate(lj) or negate(li) == lj:

                # (Ci − {li}) ∪ (Cj − {lj})
                new_clause = []

                for x in Ci:
                    if x != li:
                        new_clause.append(x)

                for x in Cj:
                    if x != lj and x not in new_clause:
                        new_clause.append(x)

                # remove duplicates already handled above
                resolvents.append(new_clause)

    return resolvents


def negate(literal):
    if literal.startswith("¬"):
        return literal[1:]
    else:
        return "¬" + literal


def pl_resolution(KB, query):

    # negate query and add to clauses
    clauses = KB.copy()
    clauses.append([negate(query)])

    new = []

    while True:
        n = len(clauses)

        for i in range(n):
            for j in range(i + 1, n):

                resolvents = pl_resolve(clauses[i], clauses[j])

                for r in resolvents:
                    # if empty clause → success
                    if len(r) == 0:
                        return True

                    if r not in new:
                        new.append(r)

        # if no new clauses
        all_included = True
        for clause in new:
            if clause not in clauses:
                all_included = False

        if all_included:
            return False

        # clauses ← clauses ∪ new
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)
KB_a = [
    ["P", "Q"],
    ["¬P", "R"],
    ["¬Q", "S"],
    ["¬R", "S"]
]

query_a = "S"

print(pl_resolution(KB_a, query_a))  # True            
KB_b = [
    ["¬P", "Q"],
    ["¬Q", "R"],
    ["¬S", "¬R"],
    ["P"]
]

query_b = "S"

print(pl_resolution(KB_b, query_b))  # False