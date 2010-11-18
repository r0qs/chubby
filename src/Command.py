from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from Caracter import Caracter

class CommandHandler(object):

                            #0  1  2  3  4  5  6  7  8  9  10 11 12 13
    _automata_transitions= [[11,0, 0, 4, 0, 0, 0, 0, 0, 11,0, 11,13,0],#up
                            [9, 2, 0, 0, 0, 0, 0, 0, 0, 10,0, 12,0, 0],#down
                            [0, 6, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],#left
                            [1, 0, 0, 0, 5, 0, 7, 0, 0, 0, 0, 0, 0, 0]]#right
    # The final states
    final_list = [5,8,10,11,13]
    final_state = 0

    def __init__(self, caracter):
    	self.caracter = caracter
        self.actual_state = 0

    def refresh_state(self, in_key):
        self.final_state = 0
        input_code = -1
        if in_key == K_UP: input_code = 0
        elif in_key == K_DOWN: input_code = 1
        elif in_key == K_LEFT: input_code = 2
        elif in_key == K_RIGHT: input_code = 3

        self.actual_state = self._automata_transitions[input_code][self.actual_state]

        if self.actual_state == 5: self.caracter.doRoll()
        elif self.actual_state == 8: self.caracter.doSprint()
        elif self.actual_state == 10: self.caracter.doGetDown()
        elif self.actual_state == 11: self.caracter.doJump()
        elif self.actual_state == 13: self.caracter.doClimb()
        #print "estado atual:" + str(self.actual_state)
        
        if self.final_state in self.final_list :
            self.actual_state = 0
            return self.final_state
            
        return self.actual_state
