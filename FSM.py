from transitions import Machine
from transitions_methods import Methods


class FSM:
    # The states
    states = ['initial', 'startPage', 'new_class']

    # The transitions
    transitions = [
        {'trigger': 'start', 'source': 'initial', 'dest': 'startPage', 'before': 'welcome'},
        {'trigger': 'add_class', 'source': 'startPage', 'dest': 'new_class', 'before': 'add_class_msg'},
        {'trigger': 'add_class_finished', 'source': 'new_class', 'dest': 'startPage',
         'before': 'class_added'},

    ]

    # Initializer
    def __init__(self, state):
        self.machine = Methods()
        Machine(model=self.machine, states=self.states, transitions=self.transitions, initial=state)
