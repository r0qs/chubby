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

        input_code = -1
        if in_key == K_UP: input_code = 0
        elif in_key == K_DOWN: input_code = 1
        elif in_key == K_LEFT: input_code = 2
        elif in_key == K_RIGHT: input_code = 3

        self.actual_state = self._automata_transitions[input_code][self.actual_state]

        if self.actual_state == 5: self.doRoll          = True
        elif self.actual_state == 8: self.doSprint      = True
        elif self.actual_state == 10: self.doGetDown    = True
        elif self.actual_state == 11: self.doJump       = True
        elif self.actual_state == 13: self.doClimb      = True
        print "estado atual:" + str(self.actual_state)

        return self.actual_state

    def clear_commands(self):
        self.doRoll     = False
        self.doSprint   = False
        self.doGetDown  = False
        self.Jump       = False
        self.doClimb    = False
