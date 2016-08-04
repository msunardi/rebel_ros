#!/usr/bin/env python

from rebel_ros.srv import *
import robel_parser as rp
import rospy

import makana_jimmy_program as mjp

vocab = mjp.position_library
vocab['muscle_combo_1'] = '((((muscle_flex_1 & muscle_flex_3) & hands_in_the_air_1) * 0.5) & stand)'
# vocab['muscle_combo_2'] = '(((muscle_flex_2 & muscle_flex_4) & hands_in_the_air_2) * 0.5)'

def parse(request):
	# Parse request	
	# If expression, expand
	expression = request.expression
	# word = rp.eval(rp.parse(expression))
	# word = parsex(expression)
	sequence, expansion = rp.foobarbaz(expression, vocab, [])
	# If generic behavior name, choose a corresponding expression
	# print "Word: %s" % word

	# Return expanded string or sequence?
	
	# sequence = [vocab[k] for k in word.replace('\n','').replace('\r','').split( )]
	mjp.JimmyDo(sequence)

	print "Evaluating expression: \"%s\" to: \"%s\"" % (expression, expansion)
	print "Sequence: %s" % sequence
	return RebelResponse(expansion[-1])

def rebel_server():
	rospy.init_node('rebel_parser_server')
	s = rospy.Service('rebel_parser_server', Rebel, parse)
	print "Ready to parse"
	rospy.spin()

if __name__ == "__main__":
	rebel_server()