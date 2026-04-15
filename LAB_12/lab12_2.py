from collections import deque

# ---------------- INPUT ----------------
grid = [
[0,0,0,0,0,6,0,0,0],
[0,5,9,0,0,0,0,0,8],
[2,0,0,0,0,8,0,0,0],
[0,4,5,0,0,0,0,0,0],
[0,0,3,0,0,0,0,0,0],
[0,0,6,0,0,3,0,5,0],
[0,0,0,0,0,7,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,5,0,0,0,2]
]

cells = [(r, c) for r in range(9) for c in range(9)]

# ---------------- INITIAL DOMAINS ----------------
def init_domains():
    domains = {}
    for r, c in cells:
        if grid[r][c] == 0:
            domains[(r,c)] = list(range(1,10))
        else:
            domains[(r,c)] = [grid[r][c]]
    return domains

# ---------------- NEIGHBORS ----------------
def get_neighbors(r, c):
    neighbors = set()

    for i in range(9):
        if i != c:
            neighbors.add((r, i))
        if i != r:
            neighbors.add((i, c))

    br, bc = (r//3)*3, (c//3)*3
    for i in range(br, br+3):
        for j in range(bc, bc+3):
            if (i,j) != (r,c):
                neighbors.add((i,j))

    return neighbors

neighbors = {cell: get_neighbors(*cell) for cell in cells}

# ---------------- BUILD ARCS ----------------
def build_arcs():
    arcs = deque()
    for Xi in cells:
        for Xj in neighbors[Xi]:
            arcs.append((Xi, Xj))
    return arcs

# ---------------- CONSTRAINT ----------------
def constraint(x, y):
    return x != y

# ---------------- REVISE ----------------
def revise(domains, Xi, Xj):
    revised = False
    removed_vals = []

    for x in domains[Xi][:]:
        if not any(constraint(x, y) for y in domains[Xj]):
            domains[Xi].remove(x)
            removed_vals.append(x)
            revised = True

    if revised:
        print(f"Revise {Xi} wrt {Xj} >> removed {removed_vals}")

    return revised, len(removed_vals)

# ---------------- AC-3 ----------------
def ac3(domains, show_steps=True):
    queue = build_arcs()
    removed_count = 0
    steps = 0

    while queue:
        Xi, Xj = queue.popleft()
        steps += 1

        revised, removed = revise(domains, Xi, Xj)

        if revised:
            removed_count += removed

            if len(domains[Xi]) == 0:
                print(f"\n[FAIL] Domain wiped out at {Xi}")
                return False, removed_count

            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    print(f"\nTotal arc checks: {steps}")
    return True, removed_count

# ---------------- BACKTRACKING ----------------
def is_valid(domains, var, value):
    for n in neighbors[var]:
        if len(domains[n]) == 1 and domains[n][0] == value:
            return False
    return True

def select_unassigned(domains):
    unassigned = [v for v in cells if len(domains[v]) > 1]
    return min(unassigned, key=lambda v: len(domains[v])) if unassigned else None

def backtrack(domains):
    var = select_unassigned(domains)

    if var is None:
        return domains

    for value in domains[var]:
        if is_valid(domains, var, value):
            new_domains = {cell: list(domains[cell]) for cell in cells}
            new_domains[var] = [value]

            result, _ = ac3(new_domains, show_steps=False)

            if result:
                solution = backtrack(new_domains)
                if solution:
                    return solution

    return None

# ---------------- PRINT FUNCTIONS ----------------
def print_domain_grid(domains):
    for r in range(9):
        print(" ".join(str(len(domains[(r,c)])) for c in range(9)))

def print_solution(domains):
    for r in range(9):
        print(" ".join(str(domains[(r,c)][0]) for c in range(9)))

# ================= RUN =================

print("========== AC-3 PROCESS ==========")
domains_ac3 = init_domains()
result, removed = ac3(domains_ac3)

print("\n========== AC-3 RESULT ==========")
print("Values removed:", removed)

print("\nDomain Size Grid:")
print_domain_grid(domains_ac3)

all_one = all(len(domains_ac3[cell]) == 1 for cell in cells)
any_zero = any(len(domains_ac3[cell]) == 0 for cell in cells)

print("\nArc Consistent:", result)
print("Any domain empty:", any_zero)
print("Fully solved by AC-3:", all_one)

print("\n========== AC-3 + BACKTRACKING ==========")
domains_bt = init_domains()
ac3(domains_bt, show_steps=False)

solution = backtrack(domains_bt)

if solution:
    print("\n[SUCCESS] Final Solved Sudoku:")
    print_solution(solution)
else:
    print("\n[FAILED] No solution found")

# ---------------- FINAL COMPARISON ----------------
print("\n========== COMPARISON ==========")
print("AC-3 Only >> Partial Reduction")
print("AC-3 + Backtracking >> Complete Solution")