from simple_voting_model import SimpleVotingModel
import sys

no_voters = int(sys.argv[1])
no_candidates = int(sys.argv[2])
v = int(sys.argv[3])

simple_voting = SimpleVotingModel(no_candidates, no_voters)
print(simple_voting.model.js_dump())

if v == 1:
    atl_model = simple_voting.model.to_atl_imperfect(simple_voting.get_actions())
else:
    atl_model = simple_voting.model.to_atl_perfect(simple_voting.get_actions())

winning = []

state_id = -1
voter_number = 1

for state in simple_voting.states:
    state_id += 1
    if state['finish'][voter_number] == 1 and state['coercer_actions'][voter_number] != 'pun' and state['voted'][
            voter_number] != 1:
        winning.append(state_id)

agents = [1]

result = atl_model.minimum_formula_many_agents(agents, winning)

print(list(result))