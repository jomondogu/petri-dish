import sys
import time
from threading import Thread

class Transition(Thread):

    def __init__(self, id = 0, inputs = None, outputs = None, position = [0,0]):
        super(Transition, self).__init__()
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
        self.locks = []
        self.fires = 0

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

    def release_locks(self):
        for lock in self.locks:
            lock.release()
            self.locks.remove(lock)

    def eligible(self):
        print(str(self) + " is checking eligibility...",flush=True)
        elig = True
        for state in self.inputs:
            if not state.ready():
                elig = False
            else:
                pass
                print(str(self) + ": " + str(state) + " is ready!",flush=True)
        return elig

    def fire(self):
        print(str(self) + " fires! ",end="",flush=True)
        for state in self.inputs:
            state.output()
            print("1 token consumed from " + str(state) + ". ",end="",flush=True)
        for state in self.outputs:
            state.input()
            print("1 token produced to " + str(state) + ". ",end="",flush=True)
        self.fires += 1

    def run(self):
        counter = 0
        while counter < 1000:
            time.sleep(0.001)
            locked = True
            for state in self.inputs + self.outputs:
                if not state.lock.acquire(False):
                    print(str(self) + ": " + str(state.id) + " is locked. Releasing all locks.",flush=True)
                    locked = False
                    self.release_locks()
                    break
                else:
                    print(str(self) + " locks " + str(state) + ".",flush=True)
                    self.locks.append(state.lock)
            if locked and self.eligible():
                self.fire()
            print(str(self) + " releases all locks.",flush=True)
            self.release_locks()
            counter += 1
        print("***" + str(self) + " fired " + str(self.fires) + " times!",flush=True)
