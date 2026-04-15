from collections import deque

# Variables
variables = ['P1','P2','P3','P4','P5','P6']

# Domains
domains = {v: ['R1','R2','R3'] for v in variables}

# Neighbors (constraint graph)
neighbors = {
    'P1': ['P2','P3','P6'],
    'P2': ['P1','P3','P4'],
    'P3': ['P1','P2','P5'],
    'P4': ['P2','P6'],
    'P5': ['P3','P6'],
    'P6': ['P1','P4','P5']
}

# Constraint: different rooms
def constraint(x, y):
    return x != y


# -- Create explicit constraint (arc) list
constraints = []
for Xi in neighbors:
    for Xj in neighbors[Xi]:
        constraints.append((Xi, Xj))

print("=== INITIAL CONSTRAINT ARCS ===")
for arc in constraints:
    print(arc)


# -- Revise function
def revise(domains, Xi, Xj):
    revised = False

    print(f"\nARC ({Xi}, {Xj})")

    for x in domains[Xi][:]:
        print(f" Check {x} in {Xi}:")

        valid = False
        for y in domains[Xj]:
            print(f"   Compare {x} != {y}", end=" ")
            if constraint(x, y):
                print("OK")
                valid = True
                break
            else:
                print("FAIL")

        if not valid:
            print(f"   >> Remove {x} from {Xi}")
            domains[Xi].remove(x)
            revised = True

    return revised


# -- AC-3 Algorithm
def ac3(domains):
    queue = deque(constraints)

    print("\n=== START AC-3 ===")

    while queue:
        Xi, Xj = queue.popleft()
        print(f"\nProcessing arc: ({Xi}, {Xj})")

        if revise(domains, Xi, Xj):

            if len(domains[Xi]) == 0:
                print("\n[FAIL] Domain empty >> FAILURE")
                return False
    added = []   # to track newly added arcs

    for Xk in neighbors[Xi]:
        if Xk != Xj:
            arc = (Xk, Xi)
            print(f"   >> Add arc {arc} to queue")
            queue.append(arc)
            added.append(arc)

    # -- Print queue AFTER adding arcs
    print("\nQueue after adding new arcs:")
    print(list(queue))

    return True


# -- -------- RUN --------

print("\nAssign P1 = R1\n")
domains['P1'] = ['R1']

result = ac3(domains)

# -- Final Output
print("\n=== FINAL DOMAINS ===")
for k, v in domains.items():
    print(k, ":", v)

print("\nArc Consistent:", result)

# -- P1 = R1 CONSTRAINT ANALYSIS - WITH INTERMEDIATE QUEUE STATES
print("\n" + "="*60)
print("DETAILED ANALYSIS: P1 ASSIGNED TO R1")
print("="*60)

print(f"\n[INITIAL] P1 = R1")
print(f"  P1 Domain: {domains['P1']}")

# Recreate AC3 with P1=R1 to show queue evolution
print("\n[AC3 QUEUE EVOLUTION WITH P1=R1]\n")

test_domains = {v: list(domains[v]) for v in domains}
queue = deque()

# Add all arcs involving P1's neighbors
for Xi in neighbors:
    for Xj in neighbors[Xi]:
        queue.append((Xi, Xj))

arc_number = 0
print("Initial queue size:", len(list(queue)))

while queue and arc_number < 15:  # Show first 15 arcs
    arc_number += 1
    Xi, Xj = queue.popleft()
    
    print(f"\n[Arc {arc_number}] Processing ({Xi}, {Xj})")
    
    revised = False
    for x in test_domains[Xi][:]:
        if not any(test_domains[Xj] for y in test_domains[Xj] if x != y):
            test_domains[Xi].remove(x)
            revised = True
            print(f"   >> Removed {x} from {Xi}")
    
    if revised:
        print(f"   Domain {Xi} updated: {test_domains[Xi]}")
        # Add related arcs
        added = []
        for Xk in neighbors[Xi]:
            if Xk != Xj:
                queue.append((Xk, Xi))
                added.append((Xk, Xi))
        if added:
            print(f"   Added {len(added)} new arcs to queue")
    else:
        print(f"   No changes needed for {Xi}")
    
    print(f"   Queue now has {len(list(queue))} arcs")

print("\n[TEAMS AFFECTED BY P1=R1 CONSTRAINT]")
print("Teams conflicting with P1:", neighbors['P1'])
print("\nDomain reductions:")
for team in ['P2', 'P3', 'P6']:
    print(f"  {team}: {test_domains[team]}")
for team in ['P4', 'P5']:
    print(f"  {team}: {test_domains[team]} (no direct conflict with P1)")

print("\n[FINAL RESULT]")
if result:
    if all(len(domains[team]) > 0 for team in ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']):
        print("  SUCCESS: Arc consistent - valid solution exists!")
        print("  The constraint graph remains satisfiable.")
    else:
        print("  FAILURE: Empty domain detected!")
else:
    print("  FAILURE: AC3 could not find arc consistency")