from transitions import Machine
from transitions_methods import Methods


class FSM:
    # The states
    states = ['initial', 'startPage', 'featuresPage']

    # The transitions
    transitions = [
        {'trigger': 'start', 'source': 'initial', 'dest': 'startPage', 'before': 'welcome'},
        {'trigger': 'features', 'source': 'startPage', 'dest': 'featuresPage'},
        {'trigger': 'cancel', 'source': 'featuresPage', 'dest': 'startPage'},
        {'trigger': 'ask_for_class', 'source': 'featuresPage', 'dest': 'featuresPage'}
    ]

    # Initializer
    def __init__(self, state):
        self.machine = Methods()
        Machine(model=self.machine, states=self.states, transitions=self.transitions, initial=state)
