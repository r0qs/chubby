from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

class CommandHandler(object):

                            #0  1  2  3  4  5  6  7  8  9  10 11 12 13
    _automata_transitions= [[11,0, 0, 4, 0, 0, 0, 0, 0, 11,0, 0, 13,0],#up
                            [9, 2, 0, 0, 0, 0, 0, 0, 0, 10,0, 12,0, 0],#down
                            [0, 6, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],#left
                            [1, 0, 0, 0, 5, 0, 7, 0, 0, 0, 0, 0, 0, 0]]#right

    def __init__(self):
        self.actual_state = 0
        self.doRoll     = False
        self.doSprint   = False
        self.doGetDown  = False
        self.Jump       = False
        self.doClimb    = False

    def refresh_state(self, in_key):
        global actual_state
        global commands_automata

        input = -1
        if in_key == K_UP: input = 0
        elif in_key == K_DOWN: input = 1
        elif in_key == K_LEFT: input = 2
        elif in_key == K_RIGHT: input = 3
        actual_state = commands_automata[input][actual_state]

        if actual_state == 5: self.doRoll        = True
        if actual_state == 8: self.doSprint      = True
        if actual_state == 10: self.doGetDown    = True
        if actual_state == 11: self.doJump       = True
        if actual_state == 13: self.doClimb      = True
        print "estado atual:" + str(actual_state)

    def clear_commands(self):
        self.doRoll     = False
        self.doSprint   = False
        self.doGetDown  = False
        self.Jump       = False
        self.doClimb    = False

    def reset_automata(self):
        self.actual_state = 0
