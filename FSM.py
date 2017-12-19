from transitions import Machine
from transitions_methods import Methods


class FSM:
    # The states
    states = [
        'initial', 'startPage',
        'new_class',
        'new_teacher', 'get_class_i', 'get_class_w', 'get_class_t'
        ]

    # The transitions
    transitions = [
        {'trigger': 'start', 'source': 'initial', 'dest': 'startPage', 'before': 'welcome'},

        # ADD CLASS FEATURE
        {'trigger': 'add_class', 'source': 'startPage', 'dest': 'new_class',
         'before': 'add_class_msg'},
        {'trigger': 'add_class_finished', 'source': 'new_class', 'dest': 'startPage',
         'before': 'class_added'},

        # ADD TEACHER FEATURE
        {'trigger': 'add_teacher', 'source': 'startPage', 'dest': 'new_teacher',
         'before': 'add_teacher_msg'},
        {'trigger': 'add_teacher_finished', 'source': 'new_teacher', 'dest': 'startPage',
         'before': 'teacher_added'},

        # GET A CLASS
        {'trigger': 'get_i', 'source': 'startPage', 'dest': 'get_class_i',
         'before': 'get_class_i_msg'},
        {'trigger': 'get_w', 'source': 'get_class_i', 'dest': 'get_class_w',
         'before': 'get_class_w_msg'},
        {'trigger': 'get_t', 'source': 'get_class_w', 'dest': 'get_class_t',
         'before': 'get_class_t_msg'},
        {'trigger': 'class_got', 'source': 'get_class_t', 'dest': 'startPage',
         'before': 'get_class_finished'},

    ]

    # Initializer
    def __init__(self, state):
        self.machine = Methods()
        Machine(model=self.machine, states=self.states, transitions=self.transitions, initial=state)
