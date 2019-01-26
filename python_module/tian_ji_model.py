from model_generator import ModelGenerator
from array_tools import ArrayTools


class TianJiModel(ModelGenerator):
    no_horses = 0

    def __init__(self, no_horses: int):
        super().__init__(no_agents=2)
        self.no_horses = no_horses
        self.generate_model()
        self.prepare_epistemic_relation()

    def generate_first_state(self) -> hash:
        king_horses = list(range(0, self.no_horses))
        tian_ji_horses = list(range(0, self.no_horses))
        first_state = {'king_score': 0, 'tian_ji_score': 0, 'king_horses': king_horses,
                       'tian_ji_horses': tian_ji_horses,
                       'results': ArrayTools.create_value_array_of_size(self.no_horses, 0), 'king_choice': -1}
        return first_state

    def get_epistemic_state(self, state: hash, agent_number: int) -> hash:
        epistemic_state = {'king_score': state['king_score'], 'tian_ji_score': state['tian_ji_score'],
                           'tian_ji_horses': state['tian_ji_horses'], 'king_choice': state['king_choice']}
        return epistemic_state

    def generate_model(self):
        first_state = self.generate_first_state()
        self.add_state(first_state)
        current_state_number = -1
        for state in self.states:
            current_state_number += 1
            if len(state['king_horses']) == 0:
                continue

            if len(state['king_horses']) < len(state['tian_ji_horses']):
                continue

            for king_horse in state['king_horses']:
                new_king_horses = state['king_horses'][:]
                new_king_horses.remove(king_horse)
                new_king_state = {'king_score': state['king_score'], 'tian_ji_score': state['tian_ji_score'],
                                  'king_horses': new_king_horses,
                                  'tian_ji_horses': state['tian_ji_horses'], 'results': state['results'],
                                  'king_choice': king_horse}
                king_actions = ['Wait', f'Send{king_horse}']
                new_king_state_number = self.add_state(new_king_state)
                self.model.add_transition(current_state_number, new_king_state_number, king_actions)
                for tian_ji_horse in state['tian_ji_horses']:
                    new_tian_ji_horses = state['tian_ji_horses'][:]
                    new_tian_ji_horses.remove(tian_ji_horse)
                    new_king_score = state['king_score']
                    new_tian_ji_score = state['tian_ji_score']
                    new_results = state['results'][:]
                    if tian_ji_horse < king_horse:
                        new_tian_ji_score += 1
                        new_results[self.no_horses - len(new_tian_ji_horses) - 1] = 1
                    else:
                        new_king_score += 1
                        new_results[self.no_horses - len(new_tian_ji_horses) - 1] = -1

                    new_state = {'king_score': new_king_score, 'tian_ji_score': new_tian_ji_score,
                                 'king_horses': new_king_horses,
                                 'tian_ji_horses': new_tian_ji_horses, 'results': new_results, 'king_choice': -1}
                    actions = [f'Send{tian_ji_horse}', 'Wait']
                    new_state_number = self.add_state(new_state)
                    self.model.add_transition(new_king_state_number, new_state_number, actions)

    def get_actions(self):
        agent_actions = ['Wait']
        for horse_id in range(0, self.no_horses):
            agent_actions.append(f'Send{horse_id}')

        return [agent_actions, agent_actions[:]]