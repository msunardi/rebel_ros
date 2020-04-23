#!/usr/bin/env python

from rebel_ros.srv import *
import robel_parser as rp
import rospy

import jeeves_program as jp

vocab = {
    'home': [512, 512, 512, -1],
    'look_down': [1024, 0, -1, -1],
    'look_up': [0, 1024, -1, -1],
    'look_left': [-1, -1, 1024, -1],
    'look_right': [-1, -1, 0, -1],
    'tilt_left': [1024, 1024, -1, -1],
    'tilt_right': [0, 0, -1, -1],
    'self-test': '(& home look_up (* look_down 2.0) home (* look_left 1.5) (* look_right 3.5) home tilt_left tilt_right)',
    'eye_left': [-1, -1, -1, '5:3'],
    'eye_right': [-1, -1, -1, '1:3'],
    'eye_up': [-1, -1, -1, '3:1'],
    'eye_down': [-1, -1, -1, '3:5'],
    'eye_center': [-1, -1, -1, '3:3'],
    'eye_up_left': [-1, -1, -1, '5:1'],
    'eye_up_right': [-1, -1, -1, '2:2'],
    'eye_down_left': [-1, -1, -1, '5:5'],
    'eye_down_right': [-1, -1, -1, '1:5']
    # '5:3': '5:3',
    # '1:3': '1:3'
}

rp.acts += ['5:3', '1:3']

# Add new keys
rp.acts += vocab.keys()
rp.Xvocab = vocab  # hack to make subtraction work
# rp.update_vocab(vocab.keys())

def parse(request):
    # Parse request
    # If expression, expand
    expression = request.expression
    # word = rp.eval(rp.parse(expression))
    # word = parsex(expression)
    sequence = []
    expansion = []
    sequence, expansion = rp.expand_sequence(expression, vocab, expansion)
    # If generic behavior name, choose a corresponding expression
    # print "Word: %s" % word

    # THIS IS A HACK! THE SEQUENCE WILL KEEP EXPANDING OTHERWISE
    # Still need to figure out why it is so

    # TODO: FIX THIS BUG!!!
    print("parse(): expansion: {}".format(expansion))
    print("parse(): sequence RAW: {}".format(sequence))
#    expansion_length = len(expansion[-1].split(" "))
#    sequence = sequence[-expansion_length:]
    print("Sequence [PRE]: %s" % sequence)

    # Return expanded string or sequence?

    # sequence = [vocab[k] for k in word.replace('\n','').replace('\r','').split( )]
    print("Sequence before JimmyDo: {}".format(sequence))
    sequence = jp.JeevesDo(sequence)


    print("Evaluating expression: \"%s\" to: \"%s\"" % (expression, expansion))
    print("Sequence: %s" % sequence)

    # expansion = None
    # print expansion
    # response = ''
    # if len(expansion) > 0:
    #     for exp in expansion[1:]:
    #         response += str(exp)
    #         print("Response: {} (total: {})".format(response, len(expansion)))
    # for s, v in sequence:
    # 	print "%s: %s" % (s, v)
    return RebelResponse(expansion[0], str(sequence))
    # return {'word': response, 'sequence': sequence}

def rebel_server():
    rospy.init_node('jeeves_rebel_server')
    s = rospy.Service('jeeves_rebel_server', Rebel, parse)
    print("Ready to parse")
    rospy.spin()

if __name__ == "__main__":
    rebel_server()