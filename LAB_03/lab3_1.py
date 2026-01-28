class Environment:
    def __init__(self, rooms):
        self.rooms = rooms

    def all_clean(self):
        return all(state == 'Clean' for state in self.rooms.values())


class VacuumAgent:
    def __init__(self):
        self.location = 'A'

        self.rules = {
            ('A', 'Dirty'): 'SUCK',
            ('B', 'Dirty'): 'SUCK',
            ('C', 'Dirty'): 'SUCK',
            ('A', 'Clean'): 'RIGHT',
            ('B', 'Clean'): 'RIGHT',
            ('C', 'Clean'): 'LEFT'
        }

    def perceive(self, env):
        return (self.location, env.rooms[self.location])

    def act(self, percept):
        return self.rules[percept]

    def move(self, action):
        if action == 'RIGHT':
            if self.location == 'A':
                self.location = 'B'
            elif self.location == 'B':
                self.location = 'C'
        elif action == 'LEFT':
            if self.location == 'C':
                self.location = 'B'


def run_vacuum(room_dict):
    env = Environment(room_dict)
    agent = VacuumAgent()

    step = 1

    while True:
        percept = agent.perceive(env)

        if env.all_clean():
            print(f"Step {step}: NO_OP")
            break

        action = agent.act(percept)
        print(f"Step {step}: {action}")

        if action == 'SUCK':
            env.rooms[agent.location] = 'Clean'
        else:
            agent.move(action)

        step += 1


run_vacuum({
    'A': 'Clean',
    'B': 'Dirty',
    'C': 'Dirty'
})
