from bridge_model import BridgeModel
import json
import sys

n = int(sys.argv[1])
k = int(sys.argv[2])
v = int(sys.argv[3])

file_hands = open("bridge_hands.txt", "r")
json_hands = file_hands.readline()
file_hands.close()

hands = json.loads(json_hands)

bridge_model = BridgeModel(n, k, {'board': [-1, -1, -1, -1], 'lefts': [0, 0],
                                  'hands': hands, 'next': 0, 'history': [],
                                  'beginning': 0, 'clock': 0, 'suit': -1})

if v == 1:
    atl_model = bridge_model.model.to_atl_imperfect(bridge_model.get_actions())
else:
    atl_model = bridge_model.model.to_atl_perfect(bridge_model.get_actions())

winning = []

state_id = -1

for state in bridge_model.states:
    state_id += 1
    if state['lefts'][0] > state['lefts'][1] and state['lefts'][0] + state['lefts'][1] == k:
        winning.append(state_id)

result = atl_model.minimum_formula_many_agents([0], winning)

print(list(result))