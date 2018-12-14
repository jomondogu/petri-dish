# PETRI DISH V0.0.0.0.0.0
# CSC464 Final Project
# Matt Stewart

import sys
import time
from random import shuffle
from matplotlib import pyplot as plt
from matplotlib import animation
from SequentialState import State as sState
from ConcurrentState import State as cState
from SequentialTransition import Transition as sTransition
from ConcurrentTransition import Transition as cTransition

def readFromFile(filename, state_tuples, transition_tuples):
    file = open(filename, 'r')
    num_states = int((file.readline()).split(" ")[1].rstrip('\n'))
    for i in range(num_states):
        file.readline()
        state_id = file.readline().rstrip('\n')
        state_inputs = [input.rstrip('\n') for input in file.readline().split(",")]
        state_outputs = [output.rstrip('\n') for output in file.readline().split(",")]
        state_tokens = int(file.readline().rstrip('\n'))
        state_position = tuple([int(coordinate.rstrip('\n')) for coordinate in file.readline().split(",")])
        state_tuple = (state_id, state_inputs, state_outputs, state_tokens, state_position)
        state_tuples.append(state_tuple)
    file.readline()
    num_transitions = int((file.readline()).split(" ")[1].rstrip('\n'))
    for i in range(num_transitions):
        file.readline()
        transition_id = file.readline().rstrip('\n')
        transition_inputs = [input.rstrip('\n') for input in file.readline().split(",")]
        transition_outputs = [output.rstrip('\n') for output in file.readline().split(",")]
        transition_position = tuple([int(coordinate.rstrip('\n')) for coordinate in file.readline().split(",")])
        transition_tuple = (transition_id, transition_inputs, transition_outputs, transition_position)
        transition_tuples.append(transition_tuple)
    file.close()

def initializeSequential(state_tuples, transition_tuples, states, transitions):
    #initialize states
    for tuple in state_tuples:
        state = sState(tuple[0])
        state.add_tokens(tuple[3])
        state.set_position(tuple[4])
        states.append(state)
    #initialize transition objects
    for tuple in transition_tuples:
        transition = sTransition(tuple[0])
        transition.set_position(tuple[3])
        transitions.append(transition)
    #add transition objects to state inputs/outpus
    for i in range(len(states)):
        for input_id in state_tuples[i][1]:
            for transition in transitions:
                if input_id == transition.id:
                    states[i].add_input(transition)
        for output_id in state_tuples[i][2]:
            for transition in transitions:
                if output_id == transition.id:
                    states[i].add_output(transition)
    #add state objects to transition inputs/outputs
    for i in range(len(transitions)):
        for input_id in transition_tuples[i][1]:
            for state in states:
                if input_id == state.id:
                    transitions[i].add_input(state)
        for output_id in transition_tuples[i][2]:
            for state in states:
                if output_id == state.id:
                    transitions[i].add_output(state)

def initializeConcurrent(state_tuples, transition_tuples, states, transitions):
    #initialize states
    for tuple in state_tuples:
        state = cState(tuple[0])
        state.add_tokens(tuple[3])
        state.set_position(tuple[4])
        states.append(state)
    #initialize transition objects
    for tuple in transition_tuples:
        transition = cTransition(tuple[0])
        transition.set_position(tuple[3])
        transitions.append(transition)
    #add transition objects to state inputs/outpus
    for i in range(len(states)):
        for input_id in state_tuples[i][1]:
            for transition in transitions:
                if input_id == transition.id:
                    states[i].add_input(transition)
        for output_id in state_tuples[i][2]:
            for transition in transitions:
                if output_id == transition.id:
                    states[i].add_output(transition)
    #add state objects to transition inputs/outputs
    for i in range(len(transitions)):
        for input_id in transition_tuples[i][1]:
            for state in states:
                if input_id == state.id:
                    transitions[i].add_input(state)
        for output_id in transition_tuples[i][2]:
            for state in states:
                if output_id == state.id:
                    transitions[i].add_output(state)

#initialize plot
fig = plt.figure()
fig.canvas.set_window_title('Petri Dish: ' + sys.argv[1])
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

state_tuples = []
transition_tuples = []
readFromFile(sys.argv[1], state_tuples, transition_tuples)
states = []
transitions = []

if sys.argv[2] == "a":
    initializeSequential(state_tuples, transition_tuples, states, transitions)
    #create state, token & transition patches
    state_patches = []
    token_patches = []
    state_labels = []
    for state in states:
        state_patch = plt.Circle(state.position, 0.5, ec='k',fc='w')
        state_patches.append(state_patch)
        token_patch = plt.Circle(state.position, 0.25, fc='k')
        token_patches.append(token_patch)
    tokens_tuple = tuple(token_patches)
    transition_patches = []
    for transition in transitions:
        transition_patch = plt.Circle(transition.position, 0.2, fc = 'r')
        transition_patches.append(transition_patch)

    def init():
        #add all state & token patches
        for i in range(len(state_patches)):
            ax.add_patch(state_patches[i])
            ax.add_patch(token_patches[i])
            state_label = ax.text(states[i].position[0], states[i].position[1]-0.7, states[i].id, horizontalalignment='center', fontsize = 8)
            #set token patch visible if state has token
            if states[i].tokens > 0:
                tokens_tuple[i].set_visible(True)
            else:
                tokens_tuple[i].set_visible(False)
        #add all transition patches
        for i in range(len(transition_patches)):
            ax.add_patch(transition_patches[i])
            transition_label = ax.text(transitions[i].position[0], transitions[i].position[1]-0.4, transitions[i].id, horizontalalignment='center', fontsize = 8)
            #add input arrows
            for input in transitions[i].inputs:
                start_pos = input.position
                #TODO: truncate arrow distance slightly to display head
                end_pos = (transitions[i].position[0]-input.position[0],transitions[i].position[1]-input.position[1])
                transin = plt.arrow(start_pos[0], start_pos[1], end_pos[0]*0.9, end_pos[1]*0.9, fc='k', ec = 'k', head_width = 0.1, head_length = 0.1)
            #add output arrows
            for output in transitions[i].outputs:
                start_pos = transitions[i].position
                #TODO: truncate arrow distance slightly to display head
                end_pos = (output.position[0]-transitions[i].position[0],output.position[1]-transitions[i].position[1])
                transin = plt.arrow(start_pos[0], start_pos[1], end_pos[0]*0.9, end_pos[1]*0.9, fc='k', ec = 'k', head_width = 0.1, head_length = 0.1)
        return tokens_tuple

    fires = 0
    checks = 0

    def animate(i):
        global checks
        global fires
        shuffle(transitions)
        for transition in transitions:
            checks += 1
            if transition.eligible():
                transition.fire()
                fires += 1
        #for every state:
            #if state.tokens, token.set_visible
        for i in range(len(token_patches)):
            if states[i].tokens > 0:
                tokens_tuple[i].set_visible(True)
            else:
                tokens_tuple[i].set_visible(False)
        return tokens_tuple

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   frames=360,
                                   interval=100,
                                   blit=True)
    start_time = time.time()
    plt.show()
    elapsed_time = time.time() - start_time
    print("Transitions checked: " + str(checks))
    print("Time elapsed: " + str(elapsed_time))
    print("Total fires: " + str(fires))
    print("Exiting program.")
elif sys.argv[2] == "s":
    initializeSequential(state_tuples, transition_tuples, states, transitions)
    fires = 0
    checks = 0
    iterations = 0
    start_time = time.time()
    while iterations < 1000:
        shuffle(transitions)
        for transition in transitions:
            checks += 1
            if transition.eligible():
                moves = True;
                transition.fire()
                fires += 1
        iterations += 1
    elapsed_time = time.time() - start_time
    print("Transitions checked: " + str(checks))
    print("Time elapsed: " + str(elapsed_time))
    print("Total fires: " + str(fires))
    print("Exiting program.")
elif sys.argv[2] == "c":
    initializeConcurrent(state_tuples, transition_tuples, states, transitions)
    start_time = time.time()
    for transition in transitions:
        transition.start()
    for transition in transitions:
        transition.join()
    elapsed_time = time.time() - start_time
    print("Transitions checked: 8000")
    print("Time elapsed: " + str(elapsed_time))
    print("Exiting program.")
else:
    print("Unable to parse execution type ('c' for concurrent, 's' for sequential). Exiting Program.")
