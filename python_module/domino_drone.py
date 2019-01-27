from drone_model import *
from strat_simpl import StrategyComparer
import sys
import json

n = int(sys.argv[1])
k = int(sys.argv[2])
heuristic = int(sys.argv[3])

energies = []
for _ in range(0, n):
    energies.append(k)

drone_model = DroneModel(no_drones=n, energies=energies, map=CracowMap(), is_random=False)

no_states = len(drone_model.states)

winning_states = []
max_visited = 0

for i, state in enumerate(drone_model.states):
    visited = set()
    for vis in state['visited']:
        visited.update(vis)
    if len(visited) > max_visited:
        max_visited = len(visited)

for i, state in enumerate(drone_model.states):
    visited = set()
    for vis in state['visited']:
        visited.update(vis)
    if len(visited) >= max_visited:
        winning_states.append(i)

strategy_comparer = StrategyComparer(drone_model.model, ['N', 'S', 'W', 'E', 'Wait'])

agents = []
for i in range(0, n):
    agents.append(i)

if heuristic == 0:
    (result, strategy) = strategy_comparer.generate_strategy_dfs(0, set(winning_states), agents, strategy_comparer.basic_h)
elif heuristic == 1:
    (result, strategy) = strategy_comparer.generate_strategy_dfs(0, set(winning_states), agents, strategy_comparer.control_h)
elif heuristic == 2:
    (result, strategy) = strategy_comparer.generate_strategy_dfs(0, set(winning_states), agents, strategy_comparer.epistemic_h)
elif heuristic == 3:
    (result, strategy) = strategy_comparer.generate_strategy_dfs(0, set(winning_states), agents, strategy_comparer.visited_states_h)

drone_model.listify_states()
if result:
    print("1")
else:
    print("0")
print(drone_model.model.js_dump_strategy(strategy))
