from tian_ji_model import TianJiModel
import json
import sys

horses = int(sys.argv[1])

tian_ji_model = TianJiModel(horses)


winning = []

state_id = -1

for state in tian_ji_model.states:
    state_id += 1
    if state['tian_ji_score'] > state['king_score'] and len(state['tian_ji_horses']) == 0:
        winning.append(state_id)

print(tian_ji_model.model.js_dump_model(winning))