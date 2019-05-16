from simple_voting_model import SimpleVotingModel
import sys

no_voters = int(sys.argv[1])
no_candidates = int(sys.argv[2])

simple_voting = SimpleVotingModel(no_candidates, no_voters)

winning = []

state_id = -1
voter_number = 0

for state in simple_voting.states:
    state_id += 1
    if state['finish'][voter_number] == 1 and state['coercer_actions'][voter_number] != 'pun' and state['voted'][
            voter_number] != 1:
        winning.append(state_id)

print(simple_voting.model.js_dump_model(winning))