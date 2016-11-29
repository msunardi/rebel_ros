#!/usr/bin/env python

from rebel_ros.srv import *
import robel_parser as rp
import rospy

import makana_jimmy_program as mjp

vocab = mjp.position_library
vocab['muscle_combo_1'] = '((muscle_flex_1 & (muscle_flex_2 & (muscle_flex_3 & (muscle_flex_4 & (muscle_flex_5 & (muscle_flex_6 & muscle_flex_7)))))) * 0.5)'
vocab['muscle_combo_2'] = '((muscle_flex_7 & (muscle_flex_6 & (muscle_flex_5 & (muscle_flex_4 & (muscle_flex_3 & (muscle_flex_2 & muscle_flex_1)))))) * 0.5)'
vocab['combo_1'] = '(muscle_combo_1 + muscle_combo_2)'
vocab['wave2'] = '((wave2_1 & (wave2_2 & (wave2_3 & (wave2_4 & (wave2_5 & (wave2_6 & wave2_7)))))) & stand)'
vocab['wave1'] = '((wave_1 & (wave_2 & (wave_3 & (wave_4 & wave_5)))) & stand)'
# vocab['greeting'] = '(((wave_1 + wave_2) & (right_arm_down & left_arm_down)) * )'
vocab['greeting'] = '(((wave1 & (wave1 * 0.6)) + (wave2 & (wave2 * 0.6))) & stand)'
vocab['onguard'] = '((onguard_1 & (onguard_2 & (onguard_3 & (onguard_4 & (onguard_5 & onguard_6 ))))) & stand)'
vocab['why'] = '((why_1 & (why_2 & (why_3 & (why_4 & (why_5 & (why_6 & why_7)))))) & stand)'
vocab['jumping'] = '(head_90_left & (head_90_right & (raise_arms & hug)))'
vocab['leila_dances'] = '((head_40_right & (head_40_left & (raise_arms & (right_arm_wave & (left_arm_wave & look_up))))) * 0.8)'
vocab['police_freeze'] = '((police_freeze_1 & (police_freeze_2 & (police_freeze_3 & (police_freeze_4 & (police_freeze_5 & (police_freeze_6 & police_freeze_7)))))) & stand)'
vocab['muscle_flex'] = '((muscle_flex_1 & (muscle_flex_2 & (muscle_flex_3 & (muscle_flex_4 & (muscle_flex_5 & (muscle_flex_6 & muscle_flex_7)))))) & stand)'
vocab['yes'] = '((yes_1 & (yes_2 & yes_3)) & stand)'
vocab['wow'] = '((wow_1 & (wow_2 & (wow_3 & wow_4))) & stand)'
vocab['yawn'] = '((yawn_1 & (yawn_2 & yawn_3)) & stand)'
vocab['brah'] = '((brah_1 & (brah_2 & (brah_3 & (brah_4 & (brah_5 & (brah_6 & brah_7)))))) & stand)'
vocab['clap'] = '((clap_1 & (clap_2 & (clap_3 & (clap_4 & (clap_5 & (clap_6 & clap_7)))))) & stand)'
vocab['oops'] = '((oops_1 & (oops_2 & (oops_3 & (oops_4 & (oops_5 & oops_6))))) & stand)'

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