import random
from collections import deque


class VacuumProblem:
    def __init__(self, initial):
        # state: (loc, A_state, B_state) where loc in {'A','B'} and states in {'Clean','Dirty'}
        self.initial = initial

    def actions(self, state):
        loc, a, b = state
        acts = []
        acts.append('Suck')
        if loc == 'A':
            acts.append('Right')
        else:
            acts.append('Left')
        acts.append('NoOp')
        return acts

    def is_goal(self, state):
        _, a, b = state
        return a == 'Clean' and b == 'Clean'

    def results(self, state, action):
        loc, a, b = state
        outcomes = []
        if action == 'NoOp':
            outcomes.append(state)
            return outcomes

        if action == 'Right':
            outcomes.append(('B', a, b))
            return outcomes

        if action == 'Left':
            outcomes.append(('A', a, b))
            return outcomes

        # action == 'Suck'
        if loc == 'A':
            # when applied to A
            if a == 'Dirty':
                # Possible nondet outcomes:
                # 1) Clean A only
                outcomes.append(('A', 'Clean', b))
                # 2) Clean A and also clean B
                outcomes.append(('A', 'Clean', 'Clean'))
                # 3) Clean A but accidentally dirty B
                outcomes.append(('A', 'Clean', 'Dirty'))
            else:  # a == 'Clean'
                # 1) no change
                outcomes.append(('A', 'Clean', b))
                # 2) Suck may deposit dirt on A
                outcomes.append(('A', 'Dirty', b))
                # 3) or may dirty B
                outcomes.append(('A', 'Clean', 'Dirty'))
        else:
            # loc == 'B'
            if b == 'Dirty':
                outcomes.append(('B', a, 'Clean'))
                outcomes.append(('B', 'Clean', 'Clean'))
                outcomes.append(('B', 'Dirty', 'Clean'))
                # Note: second and third above represent different side-effects
            else:
                outcomes.append(('B', a, 'Clean'))
                outcomes.append(('B', a, 'Dirty'))
                outcomes.append(('B', a, 'Clean'))

        # normalize outcomes to proper tuples (loc, A, B)
        normalized = []
        for o in outcomes:
            if len(o) == 3:
                normalized.append(o)
            else:
                # safety fallback
                normalized.append(state)
        # remove duplicates while keeping order
        seen = set()
        uniq = []
        for s in normalized:
            if s not in seen:
                seen.add(s)
                uniq.append(s)
        return uniq


def stringify(state):
    return f"loc={state[0]} A={state[1]} B={state[2]}"


def OR_SEARCH(problem, state, path, max_depth=12, print_tree=False, depth=0):
    indent = "  " * depth
    if print_tree:
        print(f"{indent}OR({stringify(state)})")
    
    if problem.is_goal(state):
        if print_tree:
            print(f"{indent}  -> GOAL")
        return {'action': 'NoOp'}
    if state in path:
        if print_tree:
            print(f"{indent}  -> CYCLE DETECTED")
        return 'failure'
    if len(path) > max_depth:
        if print_tree:
            print(f"{indent}  -> MAX DEPTH EXCEEDED")
        return 'failure'

    for action in problem.actions(state):
        if print_tree:
            print(f"{indent}  Try action: {action}")
        plan = AND_SEARCH(problem, problem.results(state, action), path + [state], max_depth, print_tree, depth + 1)
        if plan != 'failure':
            if print_tree:
                print(f"{indent}  -> SUCCESS with {action}")
            return {'action': action, 'branches': plan}
    
    if print_tree:
        print(f"{indent}  -> FAILURE")
    return 'failure'


def AND_SEARCH(problem, states, path, max_depth=12, print_tree=False, depth=0):
    indent = "  " * depth
    if print_tree:
        print(f"{indent}AND({[stringify(s) for s in states]})")
    
    plan = {}
    for s in states:
        subplan = OR_SEARCH(problem, s, path, max_depth, print_tree, depth + 1)
        if subplan == 'failure':
            if print_tree:
                print(f"{indent}  -> FAILURE (subgoal {stringify(s)} failed)")
            return 'failure'
        plan[s] = subplan
    
    if print_tree:
        print(f"{indent}  -> AND SUCCESS")
    return plan


def pretty_print_plan(plan, indent=0):
    sp = '  ' * indent
    if plan == 'failure' or plan is None:
        print(sp + 'FAILURE')
        return
    if plan.get('action') == 'NoOp':
        print(sp + 'NoOp')
        return
    action = plan['action']
    print(sp + f'Action: {action}')
    branches = plan.get('branches', {})
    for state, sub in branches.items():
        print(sp + f'  If outcome -> {stringify(state)}:')
        pretty_print_plan(sub, indent + 2)


def simulate(plan, problem, actual_state, trials=5, seed=1):
    random.seed(seed)
    for t in range(trials):
        s = actual_state
        steps = 0
        trace = [s]
        while not problem.is_goal(s) and steps < 100:
            # find action for current state in plan
            if plan == 'failure' or plan is None:
                break
            node = plan_for_state(plan, s)
            if node is None or node == 'failure':
                break
            action = node.get('action')
            outcomes = problem.results(s, action)
            # choose random outcome
            s = random.choice(outcomes)
            trace.append(s)
            steps += 1
        print(f'Run {t+1}: steps={steps}, goal={problem.is_goal(s)}, trace:')
        for st in trace:
            print('   ', stringify(st))


def reactive_policy_run(problem, actual_state, trials=100, max_steps=50, seed=0):
    # Simple reactive policy: if current tile dirty -> Suck, else move to other tile.
    random.seed(seed)
    success = 0
    for t in range(trials):
        s = actual_state
        steps = 0
        while not problem.is_goal(s) and steps < max_steps:
            loc, a, b = s
            if loc == 'A':
                cur = a
            else:
                cur = b
            if cur == 'Dirty':
                action = 'Suck'
            else:
                action = 'Right' if loc == 'A' else 'Left'
            outcomes = problem.results(s, action)
            s = random.choice(outcomes)
            steps += 1
        if problem.is_goal(s):
            success += 1
    print(f'Reactive policy success: {success}/{trials} runs ({success/trials:.2%})')


def plan_for_state(plan, state):
    # plan is rooted at initial state; since our plan branches are keyed by concrete states,
    # we need to traverse: start at root plan and follow actual states to find appropriate subplan.
    node = plan
    # If root is NoOp
    if node.get('action') == 'NoOp':
        return node
    while True:
        action = node.get('action')
        branches = node.get('branches', {})
        # find branch for this state
        if state in branches:
            node = branches[state]
            if node.get('action') is None:
                return None
            if node.get('action') == 'NoOp':
                return node
            # continue loop
            continue
        # No matching branch found: cannot follow plan deterministically
        return {'action': action, 'branches': branches}


def main():
    # Example initial states
    init = ('A', 'Dirty', 'Dirty')
    problem = VacuumProblem(init)

    print('=== SEARCH TREE ===')
    plan = OR_SEARCH(problem, problem.initial, [], print_tree=True)
    print('\n=== FINAL CONDITIONAL PLAN (AND-OR) ===')
    pretty_print_plan(plan)
    print('\n=== SIMULATIONS (random nondet outcomes) ===')
    simulate(plan, problem, init, trials=5, seed=42)
    print('\n=== REACTIVE POLICY TRIALS ===')
    reactive_policy_run(problem, init, trials=200, max_steps=50, seed=123)


if __name__ == '__main__':
    main()
