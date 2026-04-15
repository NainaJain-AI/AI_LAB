# ── Variables and domains ─────────────────────────────────────────────────────
VARIABLES = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y', 'c1', 'c2', 'c3', 'c4']

INITIAL_DOMAINS = {
    'S': set(range(1, 10)),   # S != 0
    'E': set(range(0, 10)),
    'N': set(range(0, 10)),
    'D': set(range(0, 10)),
    'M': {1},                 #  FIXED: M must be 1
    'O': set(range(0, 10)),
    'R': set(range(0, 10)),
    'Y': set(range(0, 10)),
    'c1': {0, 1},
    'c2': {0, 1},
    'c3': {0, 1},
    'c4': {1},                #  Since c4 = M = 1
}


# ── Constraint Check ──────────────────────────────────────────────────────────

def check_constraint(assignment):
    a = assignment

    # Partial checking
    if not all(v in a for v in VARIABLES):

        if all(v in a for v in ['D', 'E', 'Y', 'c1']):
            if a['D'] + a['E'] != a['Y'] + 10 * a['c1']:
                return False

        if all(v in a for v in ['N', 'R', 'c1', 'E', 'c2']):
            if a['N'] + a['R'] + a['c1'] != a['E'] + 10 * a['c2']:
                return False

        if all(v in a for v in ['E', 'O', 'c2', 'N', 'c3']):
            if a['E'] + a['O'] + a['c2'] != a['N'] + 10 * a['c3']:
                return False

        if all(v in a for v in ['S', 'M', 'c3', 'O', 'c4']):
            if a['S'] + a['M'] + a['c3'] != a['O'] + 10 * a['c4']:
                return False

        if all(v in a for v in ['c4', 'M']):
            if a['c4'] != a['M']:
                return False

        return None

    # Full check
    return (
        a['D'] + a['E'] == a['Y'] + 10 * a['c1'] and
        a['N'] + a['R'] + a['c1'] == a['E'] + 10 * a['c2'] and
        a['E'] + a['O'] + a['c2'] == a['N'] + 10 * a['c3'] and
        a['S'] + a['M'] + a['c3'] == a['O'] + 10 * a['c4'] and
        a['c4'] == a['M']
    )


# ── All Different ─────────────────────────────────────────────────────────────

def all_different(assignment):
    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    vals = [assignment[v] for v in letters if v in assignment]
    return len(vals) == len(set(vals))


# ── Forward Checking ──────────────────────────────────────────────────────────

def forward_check(var, value, domains, assignment):
    new_domains = {v: set(d) for v, d in domains.items()}

    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']

    if var in letters:
        for other in letters:
            if other != var and other not in assignment:
                new_domains[other].discard(value)
                if not new_domains[other]:
                    return None

    return new_domains


# ── Backtracking ─────────────────────────────────────────────────────

call_count = 0

def backtrack(assignment, domains, solutions=None):
    global call_count
    call_count += 1

    if solutions is None:
        solutions = []

    # Goal
    if len(assignment) == len(VARIABLES):
        if check_constraint(assignment):
            solutions.append(dict(assignment))
        return solutions

    #Simple order 
    var = next(v for v in VARIABLES if v not in assignment)

    for value in sorted(domains[var]):
        assignment[var] = value

        if not all_different(assignment):
            del assignment[var]
            continue

        if check_constraint(assignment) is False:
            del assignment[var]
            continue

        new_domains = forward_check(var, value, domains, assignment)
        if new_domains is None:
            del assignment[var]
            continue

        backtrack(assignment, new_domains, solutions)
        del assignment[var]

    return solutions


# ── Print Solution ────────────────────────────────────────────────────────────

def print_solution(sol):
    S,E,N,D = sol['S'],sol['E'],sol['N'],sol['D']
    M,O,R,Y = sol['M'],sol['O'],sol['R'],sol['Y']

    SEND  = 1000*S + 100*E + 10*N + D
    MORE  = 1000*M + 100*O + 10*R + E
    MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

    print("\nSolution:")
    print(sol)
    print(f"\n {SEND}")
    print(f"+{MORE}")
    print("------")
    print(f"{MONEY}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Solving SEND + MORE = MONEY (Forward Checking Only)\n")

    domains = {v: set(d) for v, d in INITIAL_DOMAINS.items()}
    call_count = 0

    solutions = backtrack({}, domains)

    print(f"\nCalls: {call_count}")
    print(f"Solutions found: {len(solutions)}")

    for sol in solutions:
        print_solution(sol)