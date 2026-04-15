# Forward Checking - Map Coloring (Gujarat)

# Colors
colors = ["Red", "Green", "Blue"]

# Graph (adjacency)
graph = {
    "Kutch": ["Banaskantha", "Jamnagar"],
    "Banaskantha": ["Kutch", "Patan", "Sabarkantha"],
    "Patan": ["Banaskantha", "Mehsana", "Surendranagar"],
    "Mehsana": ["Patan", "Gandhinagar", "Ahmedabad"],
    "Sabarkantha": ["Banaskantha", "Gandhinagar"],
    "Gandhinagar": ["Mehsana", "Sabarkantha", "Ahmedabad", "Kheda"],
    "Ahmedabad": ["Mehsana", "Gandhinagar", "Kheda", "Anand", "Surendranagar"],
    "Surendranagar": ["Patan", "Ahmedabad", "Rajkot"],
    "Rajkot": ["Surendranagar", "Jamnagar", "Junagadh"],
    "Jamnagar": ["Kutch", "Rajkot"],
    "Junagadh": ["Rajkot", "Amreli"],
    "Amreli": ["Junagadh", "Bhavnagar"],
    "Bhavnagar": ["Amreli", "Anand"],
    "Anand": ["Ahmedabad", "Kheda", "Bhavnagar", "Vadodara"],
    "Kheda": ["Gandhinagar", "Ahmedabad", "Anand", "Vadodara"],
    "Vadodara": ["Kheda", "Anand", "Bharuch", "Panchmahal"],
    "Bharuch": ["Vadodara", "Surat"],
    "Surat": ["Bharuch", "Navsari"],
    "Navsari": ["Surat", "Valsad","Dang"],
    "Valsad": ["Navsari"],
    "Dang": ["Navsari","Surat"],
    "Panchmahal": ["Vadodara", "Dahod"],
    "Dahod": ["Panchmahal"]
}

# Initial domains
domains = {v: list(colors) for v in graph}

# Check constraint
def is_safe(var, color, assignment):
    for neighbor in graph[var]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

# Forward Checking function
def forward_check(var, color, domains, assignment):
    new_domains = {v: list(domains[v]) for v in domains}

    for neighbor in graph[var]:
        if neighbor not in assignment:
            if color in new_domains[neighbor]:
                new_domains[neighbor].remove(color)
                if len(new_domains[neighbor]) == 0:
                    return None
    return new_domains

# Backtracking + Forward Checking
def solve(assignment, domains, depth=0):
    if len(assignment) == len(graph):
        return assignment

    # Select unassigned variable
    var = next(v for v in graph if v not in assignment)
    
    print(f"\n{'  ' * depth}Step {len(assignment) + 1}: Assigning color to {var}")
    print(f"{'  ' * depth}Available colors for {var}: {domains[var]}")

    for color in domains[var]:
        if is_safe(var, color, assignment):
            assignment[var] = color
            print(f"{'  ' * depth}>> Assigned {var} = {color}")
            print(f"{'  ' * depth}Current assignment: {assignment}")

            new_domains = forward_check(var, color, domains, assignment)
            if new_domains:
                print(f"{'  ' * depth}Domains after forward checking:")
                for v in graph:
                    if v not in assignment:
                        print(f"{'  ' * depth}  {v}: {new_domains[v]}")
                
                result = solve(assignment, new_domains, depth + 1)
                if result:
                    return result
            else:
                print(f"{'  ' * depth}X Forward checking failed - Domain became empty, backtracking...")

            del assignment[var]
            print(f"{'  ' * depth}X Backtracking from {var} = {color}")

    return None

# Run
solution = solve({}, domains)

# Output
print("Coloring Solution:")
for k, v in solution.items():
    print(k, "->", v)