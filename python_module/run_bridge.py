from bridge_model import BridgeModel
import json
import sys

n = int(sys.argv[1])
k = int(sys.argv[2])

hands = BridgeModel.generate_random_hands(n, k)

bridge_model = BridgeModel(n, k, {'board': [-1, -1, -1, -1], 'lefts': [0, 0],
                                  'hands': hands, 'next': 0, 'history': [],
                                  'beginning': 0, 'clock': 0, 'suit': -1})

file_hands = open("bridge_hands.txt", "w")
file_hands.write(json.dumps(hands))
file_hands.close()

winning = []

state_id = -1

for state in bridge_model.states:
    state_id += 1
    if state['lefts'][0] > state['lefts'][1] and state['lefts'][0] + state['lefts'][1] == k:
        winning.append(state_id)

bridge_model.transitions_to_readable()
print(bridge_model.model.js_dump_model(winning))