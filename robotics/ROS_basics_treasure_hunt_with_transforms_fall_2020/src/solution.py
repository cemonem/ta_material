#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import tf2_ros
from ceng460hw1.srv import *
from ceng460hw1_utils import *
import numpy as np
from tf2_msgs.msg import TFMessage



class Robot:

    def __init__(self):
        rospy.init_node('robot')
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
        self.pub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
        self.zeroTime = rospy.Time()
    
    def send_diff_drive_vel_msg(self, linear, angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.pub.publish(msg)
    
    def get_global_transformStamped(self):
        try:
            trans = self.tfBuffer.lookup_transform("odom", "base_footprint", self.zeroTime)
            return trans
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            return None

    def move_to(self, x_goal, y_goal, P_vel, P_angular, rate=20, tolerance=0.02):
        pass
    
    def rotate_to(self, x_goal, y_goal, P_angular, rate=20, tolerance=0.02):
        pass
    
    def main(self):
        rospy.wait_for_message('tf', TFMessage)
        rospy.wait_for_service('spot_announcement')
        announce_spot = rospy.ServiceProxy('spot_announcement', SpotAnnouncement)

        first_announcement = SpotAnnouncementRequest()
        #first_announcement.spot.transform.translation.x = 3
        first_announcement.spot.child_frame_id = "0"
        first_resp = announce_spot(first_announcement)
        if not first_resp.success:
            rospy.logerr('something is wrong!')
            exit()
        rospy.loginfo('first response: %s'% first_resp)
        tf_transform = self.get_global_transformStamped()
        rospy.loginfo('tf_transform: %s' % tf_transform)
        rospy.loginfo('transform_matrix: %s' % TransformStamped_to_transform_matrix(tf_transform))
        self.send_diff_drive_vel_msg(1,1)
        rospy.sleep(3)
        self.send_diff_drive_vel_msg(0,0)

if __name__ == "__main__":
    try:
        robot = Robot()
        robot.main()
    except rospy.ROSInterruptException:
        pass