#!/usr/bin/env python
# license removed for brevity
import rospy
import threading
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import logging

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
        threading.Thread.__init__(self)

    def run(self):
        while not rospy.is_shutdown():
            self.sleeper.sleep()

    def evaluate_task(self, task):
        '''At this point, any other expressions except for concurrency and merge *SHOULD* have been expanded'''
        logging.info("Received task: {}".format(task))
        print(task)
        if '|' in task.data:
            return self.process_concurrency(task.data)
        elif '~' in task.data:
            return self.process_merge(task.data)
        else:
            return task.data

    def execute_task(self, task):
        zoot = Twist()
        zoot.linear.x = 0.0
        zoot.linear.y = 0.0
        zoot.linear.z = 0.0
        zoot.angular.x = 0.0
        zoot.angular.y = 0.0
        zoot.angular.z = 0.0

        for t in task.data:
            print(t)
            if t == 'w':
                zoot.linear.x = 3.0
            if t == 'a':
                zoot.angular.z = 3.0
            if t == 'd':
                zoot.angular.z = -3.0
        self.pub.publish(zoot)
        self.sleeper.sleep()


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
        for e in c_events:
            if len(e) < longest_event:
                e += ' ' * (longest_event - len(e))  # pad the end with blanks
            z_events.append(e)
        # 3. "Transpose" the events; turn concurrent symbols into one sequence
        z_events = list(zip(*z_events))

        print("Processing concurrent events: {}".format(z_events))
        return z_events

    def process_merge(self, events):
        '''Merge events values'''
        print("Processing merge events: {}".format(events))
        return events

if __name__ == '__main__':
    try:
        rospy.init_node('cmd_publisher', anonymous=True)
        t = TaskExecutor()
        t.start()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass