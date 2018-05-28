#!/usr/bin/env python
# license removed for brevity
import rospy
import threading
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import logging
import ast
from rebel_ros.srv import *

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)

class TaskExecutor(threading.Thread):
    '''
    Executes words parsed by robel_parser
    - Also responsible for checking for *concurrency* and *merge* tasks and re-arrange the symbols accordingly
    '''

    def __init__(self):
        self.pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)  # Change to appropriate/desired executor
        self.sleeper = rospy.Rate(10)
        rospy.Subscriber('rebel_task', String, self.evaluate_task)
        rospy.wait_for_service('rebel_parser_server')
        self.rebel_parser = rospy.ServiceProxy('rebel_parser_server', Rebel)
        threading.Thread.__init__(self)

    def run(self):
        while not rospy.is_shutdown():
            self.sleeper.sleep()

    def evaluate_task(self, task):
        '''At this point, any other expressions except for concurrency and merge *SHOULD* have been expanded'''
        logging.info("Received task: {}".format(task))

        # Parse expression first
        rospy.loginfo("[gesture_callback] Got new gesture: %s" % task.data)
        print "Greeting.data: %s" % task.data
        get = self.rebel_parser(task.data)
        word = get.word
        sequence = get.sequence
        # seq = ast.literal_eval(sequence)

        task = word  # Temporary: replace task with sequence
        print(task)
        execution_plan = None

        # TODO: Consider a case with mixed concurrent and merged events e.g. (| A~B C)
        # Concurrency should be the last step - merge must be done before concurrency
        # Maybe create an intermediary symbol for merged events

        if '|' in task:    # Concurrent
            execution_plan = self.process_concurrency(task.data)
        elif '~' in task:  # Merge
            execution_plan = self.process_merge(task.data)
        else:
            le_task = []
            for f in task.strip().split(' '):
                if f != '':
                    le_task.append(f)
            print("Le_task: {}".format(le_task))
            # TODO: Check all the other (non-concurrent/merge) possible cases
            #le_task = [tuple(ftuple)]
            print("No concurrency or merge detected - executing: {}".format(le_task))
            execution_plan = le_task

        self.execute_task(execution_plan)

    # def execute_task(self, task):
    #     zoot = Twist()
    #     zoot.linear.x = 0.0
    #     zoot.linear.y = 0.0
    #     zoot.linear.z = 0.0
    #     zoot.angular.x = 0.0
    #     zoot.angular.y = 0.0
    #     zoot.angular.z = 0.0
    #
    #     for t in task.data:
    #         print(t)
    #         if t == 'w':
    #             zoot.linear.x = 3.0
    #         if t == 'a':
    #             zoot.angular.z = 3.0
    #         if t == 'd':
    #             zoot.angular.z = -3.0
    #     self.pub.publish(zoot)
    #     self.sleeper.sleep()


    def process_concurrency(self, events):
        '''Arrange events for concurrent execution'''
        is_timing = False
        timing = None

        # Check for timing info in the very last argument
        if type(events[-1]) in [float, list]:
            # Then it's timing argument - else, no timing argument is given
            is_timing = True
            timing = events[-1]

        # TODO: Decide how timing info is used

        # Collect the concurrent events
        c_events = events.split('|')
        longest_event = len(c_events[0])

        # 1. find the max length among the events
        for e in c_events[1:]:
            if len(e) > longest_event:
                longest_event = len(e)

        # 2. Pad events with length < longest_event with blanks
        z_events = []
        for i in range(len(c_events)):
            e = c_events[i]
            if len(e) < longest_event:
                e += ' ' * (longest_event - len(e))  # pad the end with blanks
            z_events.append(e)

        # 3. "Transpose" the events; turn concurrent symbols into one 'sequence'
        execution_plan = list(zip(*z_events))

        print("Processing concurrent events: {}".format(execution_plan))

        # TODO: Execute events
        return execution_plan

    def process_merge(self, events):
        '''Merge events values'''
        # TODO: Process merge events
        print("Processing merge events: {}".format(events))
        return events

    def execute_task(self, execution_plan):
        '''Execute execution_plan'''
        pass

if __name__ == '__main__':
    try:
        rospy.init_node('cmd_publisher', anonymous=True)
        t = TaskExecutor()
        t.start()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass