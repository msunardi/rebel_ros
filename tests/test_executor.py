#!/usr/bin/env python

import sys
import rospy
from rebel_ros.srv import *

test_cases = ['(| yes wow)', '(& (| yes wow) (| wow yes))', '(| yes (| wow yes))', '(| yes wow freeze)']

def test_executor(xinput):
    rospy.wait_for_service('rebel_parser_server')
    try:
        rebel_parser = rospy.ServiceProxy('rebel_parser_server', Rebel)
        resp = rebel_parser(xinput)
        return resp.word, resp.sequence
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

def usage():
    print "Test"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        exp = str(sys.argv[1])
    else:
        print usage()
        sys.exit()
    print "Requesting expression: %s" % exp
    print "Parsed expression: %s ===> %s" % (exp, test_executor(exp))