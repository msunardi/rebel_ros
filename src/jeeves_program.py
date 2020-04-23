import numpy as np
import random
import copy
import subprocess

ServoNames = ['TILT_RIGHT', 'TILT_LEFT', 'PAN', 'FACE_CMD']

def MakePositionList(Positions, Timing=None):
    # ServoNames = ['TILT_RIGHT', 'TILT_LEFT', 'PAN', 'FACE_CMD']
    body = {name: 512 for name in ServoNames[-1]}
    body[ServoNames[-1]] = ''
    timing = {'Time': 550, 'PauseTime': 100}
    CurrentPosition = [0,0,0,'']
    for servo in range(len(ServoNames)):
        # CurrentPosition[servo] = int(round(InitialPosition[servo] + Step[servo]*position))
        try:
            CurrentPosition[servo] = Positions[servo]
            body[ServoNames[servo]] = Positions[servo]
        except IndexError as ie:
            print("Index error: {}".format(servo))
    print(body, timing)
    return [body, timing]

def MergePositions(CurrentPosition, NextPosition):
    UpdatedNextPosition = copy.copy(NextPosition)
    print("UpdatedNextPosition Before: %s" % UpdatedNextPosition)
    for i in range(len(NextPosition)):
        if NextPosition[i] == -1:
                UpdatedNextPosition[i] = CurrentPosition[i]
    print("UpdatedNextPosition After: %s" % UpdatedNextPosition)
    return UpdatedNextPosition

def collectSequence(sequence):
    # ServoNames = ['TILT_RIGHT', 'TILT_LEFT', 'PAN', 'FACE_CMD']

    output = dict({key: [] for key in ServoNames})
    output['Time'] = []
    output['PauseTime'] = []

    l = len(sequence) - 1

    for i, s in enumerate(sequence):
        for n in ServoNames:
            output[n] += [s[0][n]]
        #HACK!! Manual add of Time and PauseTime
        if i == l:
            output['Time'] += [150]
            output['PauseTime'] += [200]
        else:
            # output['Time'] += [np.random.normal(loc=70, scale=3)]
            # output['PauseTime'] += [np.random.normal(loc=50, scale=2)]
            # output['Time'] += [70]
            # output['PauseTime'] += [10]
            # output['Time'] += [100 + (np.random.normal() * 100)]
            # output['PauseTime'] += [10 + np.random.random() * 200]
            output['Time'] += [100]
            output['PauseTime'] += [0]
    return output

def ProcessPositions(PositionSequence):
    print("Pos sequence: %s" % PositionSequence)
    CurrentPosition = [512, 512, 512, '']
    output_sequence = list()
    for i in range(len(PositionSequence)):
        if type(PositionSequence[i]) == str:
            output_sequence += [PositionSequence[i]]
            continue
        NextPosition = PositionSequence[i]
        print("NextPosition: %s" % NextPosition)
        NextPosition = MergePositions(CurrentPosition, NextPosition)
        # if  i != 0:
        output_sequence += [MakePositionList(NextPosition)]
        CurrentPosition = NextPosition
        print("CurrentPosition: %s" % CurrentPosition)

    # return output_sequence
    return collectSequence(output_sequence)

def JeevesDo(seq):
    print("\n***Seq length: {}\n****".format(len(seq)))
    return ProcessPositions(seq)    #