from model_generator import ModelGenerator
import itertools


class SimpleVotingModel(ModelGenerator):
    number_of_candidates = 0
    number_of_voters = 0

    def __init__(self, number_of_candidates, number_of_voters):
        self.number_of_candidates = number_of_candidates
        self.number_of_voters = number_of_voters
        super().__init__(no_agents=(number_of_candidates + 1))
        self.generate_model()
        self.prepare_epistemic_relation()

    def generate_model(self):
        beginning_array = []
        for _ in range(0, self.number_of_voters):
            beginning_array.append('')

        beginning_array_minus_one = []
        for _ in range(0, self.number_of_voters):
            beginning_array_minus_one.append(-1)

        first_state = {'voted': beginning_array_minus_one[:], 'voters_action': beginning_array[:],
                       'coercer_actions': beginning_array[:], 'finish': beginning_array_minus_one[:]}
        state_number = 0

        self.add_state(first_state)
        state_number += 1
        current_state_number = -1

        for state in self.states:
            current_state_number += 1
            voting_product_array = []
            coercer_possible_actions = ['wait']
            for voter_number in range(0, self.number_of_voters):
                if state['voted'][voter_number] == -1:
                    voting_product_array.append(list(range(0, self.number_of_candidates)))
                    voting_product_array[voter_number].append('wait')
                elif state['voters_action'][voter_number] == '':
                    voting_product_array.append(['give', 'ng', 'wait'])
                elif state['coercer_actions'][voter_number] == '':
                    coercer_possible_actions.append('np' + str(voter_number + 1))
                    coercer_possible_actions.append('pun' + str(voter_number + 1))
                    voting_product_array.append(['wait'])
                else:
                    voting_product_array.append(['wait'])

            voting_product_array.append(coercer_possible_actions)

            for possibility in itertools.product(*voting_product_array):
                action = []
                for _ in range(0, self.number_of_voters + 1):
                    action.append('')
                new_state = {'voted': state['voted'][:], 'voters_action': state['voters_action'][:],
                             'coercer_actions': state['coercer_actions'][:], 'finish': state['finish'][:]}

                for voter_number in range(0, self.number_of_voters):
                    action[voter_number + 1] = possibility[voter_number]
                    voter_action_string = str(possibility[voter_number])
                    if voter_action_string[0] == 'g' or voter_action_string[0] == 'n':
                        new_state['voters_action'][voter_number] = voter_action_string
                    elif voter_action_string[0] != 'w':
                        new_state['voted'][voter_number] = possibility[voter_number]

                action[0] = possibility[self.number_of_voters]
                if action[0][0:3] == 'pun':
                    pun_voter_number = int(action[0][3:])
                    new_state['coercer_actions'][pun_voter_number - 1] = 'pun'
                    new_state['finish'][pun_voter_number - 1] = 1
                elif action[0][0:2] == 'np':
                    np_voter_number = int(action[0][2:])
                    new_state['coercer_actions'][np_voter_number - 1] = 'np'
                    new_state['finish'][np_voter_number - 1] = 1

                new_state_id = self.add_state(new_state)

                self.model.add_transition(current_state_number, new_state_id, action)

    def get_epistemic_state(self, state: hash, agent_number: int):
        if agent_number == 0:
            epistemic_state = {'coercer_actions': state['coercer_actions'][:], 'voted': state['voted'][:],
                               'voters_action': state['voters_action'][:], 'finish': state['finish'][:]}
            for voter_number in range(0, self.number_of_voters):
                if state['voters_action'][voter_number] == '' and state['voted'][voter_number] != -1:
                    epistemic_state['voted'][voter_number] = -2
                elif state['voters_action'][voter_number] == 'ng':
                    epistemic_state['voted'][voter_number] = -1
            return epistemic_state
        else:
            epistemic_state = {'coercer_actions': state['coercer_actions'][:], 'voted': state['voted'][:],
                               'voters_action': state['voters_action'][:], 'finish': state['finish'][:]}
            for voter_number in range(1, self.number_of_voters):
                epistemic_state['voters_action'][voter_number] = -1
                epistemic_state['voted'][voter_number] = -1
                epistemic_state['coercer_actions'][voter_number] = -1
                # epistemic_state['finish'][voter_number] = -1
            return epistemic_state

    def get_actions(self):
        result = [['wait']]

        for voter_number in range(1, self.number_of_voters + 1):
            result[0].append(f'np{voter_number}')
            result[0].append(f'pun{voter_number}')
            result.append(['give, ng, wait'])

            for candidate_number in range(0, self.number_of_candidates):
                result[-1].append(str(candidate_number))

        return result
