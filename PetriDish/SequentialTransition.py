import sys

class Transition():

    def __init__(self, id = 0, inputs = None, outputs = None, position = [0,0]):
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
        self.position = position

    def __str__(self):
        return "Transition " + str(self.id)

    def add_input(self, input):
        self.inputs.append(input)
        self.M = len(self.inputs)

    def add_output(self, output):
        self.outputs.append(output)
        self.N = len(self.outputs)

    def set_position(self, pos):
        self.position = pos

    def eligible(self):
        print(str(self) + " is checking eligibility...")
        elig = True
        for state in self.inputs:
            if not state.ready():
                print(str(state) + " is not ready.")
                elig = False
            else:
                print(str(state) + " is ready!")
        return elig

    def fire(self):
        print(str(self) + " fires!")
        for state in self.inputs:
            state.output()
            print("1 token consumed from " + str(state))
        for state in self.outputs:
            state.input()
            print("1 token produced to " + str(state))
