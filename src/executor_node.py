#!/usr/bin/env python
# license removed for brevity
import rospy
import threading
from std_msgs.msg import String
from geometry_msgs.msg import Twist



class TaskExecutor(threading.Thread):


    def __init__(self):
        self.pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
        self.sleeper = rospy.Rate(10)
        rospy.Subscriber('rebel_task', String, self.execute_task)
        threading.Thread.__init__(self)

    def run(self):
        while not rospy.is_shutdown():
            self.sleeper.sleep()

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


# def cmd_publisher():
#
#
#     rate = rospy.Rate(10) # 10hz
#     while not rospy.is_shutdown():
#         # hello_str = "hello world %s" % rospy.get_time()
#         # rospy.loginfo(hello_str)
#         # pub.publish(hello_str)
#         rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('cmd_publisher', anonymous=True)
        t = TaskExecutor()
        t.start()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass