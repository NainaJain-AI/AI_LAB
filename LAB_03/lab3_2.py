class RailwayCrossingAgent:

    def get_action(self, train_detected, obstacle_detected, emergency_active):
        """
        train_detected    : 0 or 1
        obstacle_detected : 0 or 1
        emergency_active  : 0 or 1
        """

        # Priority 1: Emergency
        if emergency_active:
            return ("Lower", "ON", "RED")

        # Priority 2: Obstacle on crossing
        if obstacle_detected:
            return ("Lower", "ON", "RED")

        # Priority 3: Train approaching
        if train_detected:
            return ("Lower", "ON", "RED")

        # Priority 4: Normal safe condition
        return ("Raise", "OFF", "GREEN")
agent = RailwayCrossingAgent()

tests = [
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (1, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1)
]

print("T O E -> Gate | Siren | Signal")
print("--------------------------------")

for t, o, e in tests:
    gate, siren, signal = agent.get_action(t, o, e)
    print(f"{t} {o} {e} -> {gate} | {siren} | {signal}")

