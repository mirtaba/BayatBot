from transitions import Machine
from transitions_methods import *

class FSM:
    # The states
    states = ['initial', 'startPage', 'featuresPage']

    # The transitions
    transitions = [
        {'trigger': 'start', 'source': 'initial', 'dest': 'startPage'},
        {'trigger': 'features', 'source': 'startPage', 'dest': 'featuresPage'},
        {'trigger': 'cancel', 'source': 'featuresPage', 'dest': 'startPage'},
        {'trigger': 'askForClass', 'source': 'featuresPage', 'dest': 'featuresPage'}
    ]

    # Initializer
    def __init__(self, user, state):
        Machine(user, states=self.states, transitions=self.transitions, initial=state)
