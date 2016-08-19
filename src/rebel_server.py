#!/usr/bin/env python

from rebel_ros.srv import *
import robel_parser as rp
import rospy

import makana_jimmy_program as mjp

vocab = mjp.position_library
vocab['muscle_combo_1'] = '((((muscle_flex_1 & muscle_flex_3) & hands_in_the_air_1) * 0.5) & stand)'
vocab['muscle_combo_2'] = '(((muscle_flex_2 & muscle_flex_4) & hands_in_the_air_2) * 0.5)'
vocab['combo_1'] = '(muscle_combo_1 + muscle_combo_2)'
vocab['wave2'] = '(wave2_1 + (wave2_2 + (wave2_3 + (wave2_4 + (wave2_5 + (wave2_6 + wave2_7))))))'
vocab['wave1'] = '(wave_1 + (wave_2 + (wave_3 + (wave_4 + wave_5))))'
vocab['greeting'] = '(((wave_1 + wave_2) & (right_arm_down & left_arm_down)) * )'

def parse(request):
	# Parse request	
	# If expression, expand
	expression = request.expression
	# word = rp.eval(rp.parse(expression))
	# word = parsex(expression)
	sequence = []
	expansion = []
	sequence, expansion = rp.foobarbaz(expression, vocab)
	# If generic behavior name, choose a corresponding expression
	# print "Word: %s" % word

	# THIS IS A HACK! THE SEQUENCE WILL KEEP EXPANDING OTHERWISE
	# Still need to figure out why it is so
	expansion_length = len(expansion[-1].split(" "))
	sequence = sequence[-expansion_length:]
	print "Sequence [PRE]: %s" % sequence

	# Return expanded string or sequence?
	
	# sequence = [vocab[k] for k in word.replace('\n','').replace('\r','').split( )]
	sequence = mjp.JimmyDo(sequence)


	print "Evaluating expression: \"%s\" to: \"%s\"" % (expression, expansion)
	print "Sequence: %s" % sequence
	
	# expansion = None
	# print expansion
	if len(expansion) > 0:
		response = str(expansion[-1])
		print "Response: %s" % response
	# for s, v in sequence:
	# 	print "%s: %s" % (s, v)
	return RebelResponse(response, str(sequence))
	# return {'word': response, 'sequence': sequence}

def rebel_server():
	rospy.init_node('rebel_parser_server')
	s = rospy.Service('rebel_parser_server', Rebel, parse)
	print "Ready to parse"
	rospy.spin()

if __name__ == "__main__":
	rebel_server()