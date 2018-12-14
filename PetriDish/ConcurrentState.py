import sys
from threading import Lock

class State:

    def __init__(self, id = 0, inputs = None, outputs = None, tokens = 0, position = [0,0]):
        self.id = id
        if inputs is None:
            self.M = 0
            self.inputs = []
        else:
            self.M = len(inputs)
            self.inputs = inputs
        if outputs is None:
            self.N = 0
            self.outputs = []
        else:
            self.N = len(outputs)
            self.outputs = outputs
        self.tokens = tokens
        self.position = position
        self.lock = Lock()

    def __str__(self):
        return "State " + str(self.id) + " (Tokens: " + str(self.tokens) + ")"


    def add_input(self, input):
        self.inputs.append(input)
        self.M = len(self.inputs)

    def add_output(self, output):
        self.outputs.append(output)
        self.N = len(self.outputs)

    def add_tokens(self, num):
        self.tokens += num

    def set_position(self, pos):
        self.position = pos

    def ready(self):
        return True if self.tokens is not 0 else False

    def input(self):
        self.tokens += 1

    def output(self):
        if self.tokens > 0:
            self.tokens -= 1
        else:
            print("ERROR: " + str(self) + " contains too few tokens to output 1.")
            sys.exit()
