#!/usr/bin/env python

from rebel_ros.srv import *
import robel_parser as rp
import rospy

def parse(request):
	# Parse request
	expression = request.expression
	word = rp.eval(rp.parse(expression))
	# If expression, expand
	# If generic behavior name, choose a corresponding expression
	# Return expanded string or sequence?

	print "Evaluationg expression: \"%s\" to: \"%s\"" % (expression, word)
	return RebelResponse(word)

def rebel_server():
	rospy.init_node('rebel_parser_server')
	s = rospy.Service('rebel_parser_server', Rebel, parse)
	print "Ready to parse"
	rospy.spin()

if __name__ == "__main__":
	rebel_server()