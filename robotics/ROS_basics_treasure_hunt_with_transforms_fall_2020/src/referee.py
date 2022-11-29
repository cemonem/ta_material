#!/usr/bin/env python
from ceng460hw1.srv import SpotAnnouncement, SpotAnnouncementResponse
import rospy
from geometry_msgs.msg import TransformStamped
import numpy as np
import tf.transformations
from ceng460hw1_utils import *
import sys
import tf2_ros
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest

class Referee:

    def __init__(self):
        rospy.init_node('referee')
        args = rospy.myargv()
        rospy.loginfo('loading treasure hunt file %s' % args[1])
        rospy.loginfo('loading treasure pose model file %s' % args[2])
        self.easy_mode = False
        if len(args) > 3:
            self.easy_mode = args[3] == "easy_mode"
        (self.spots_world_frames, self.clues_with_frames) = np.load(args[1])
        self.found_frames = []
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
        self.zeroTime = rospy.Time()

        with open(args[2],'r') as f:
            self.treasure_model = f.read()

        rospy.wait_for_service('/gazebo/spawn_sdf_model')
        self.spawn_sdf_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
    
    def spawn_treasure_pose_model(self, idd):
        tf_stamped = transform_matrix_to_TransformStamped(self.spots_world_frames[idd], "0", str(idd))
        req = SpawnModelRequest()

        req.model_name = "pose_"+str(idd)
        req.model_xml = self.treasure_model
        req.robot_namespace = "pose_"+str(idd)
        req.reference_frame = "world"

        req.initial_pose.position.x = tf_stamped.transform.translation.x
        req.initial_pose.position.y = tf_stamped.transform.translation.y
        req.initial_pose.position.z = tf_stamped.transform.translation.z

        req.initial_pose.orientation = tf_stamped.transform.rotation

        resp = self.spawn_sdf_model(req)
    
    def get_robot_global_transform(self):
        try:
            trans = self.tfBuffer.lookup_transform("odom", "base_footprint", self.zeroTime)
            return trans.transform
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            return None
    
    def run(self):
        self.service = rospy.Service('spot_announcement', SpotAnnouncement, self.handle_spot_announcement)
        rospy.spin()

    def handle_spot_announcement(self, req):

        try:
            spot_id = int(req.spot.child_frame_id)
            spot_gtruth = self.spots_world_frames[spot_id]
        except IndexError, ValueError:
            rospy.logerr("invalid child_frame_id received: %s"%(req.spot.child_frame_id))
            return SpotAnnouncementResponse()

        spot_guess = TransformStamped_to_transform_matrix(req.spot)
        if not np.allclose(spot_gtruth, spot_guess):
            rospy.logerr("incorrect treasure transform, check your transform calculation!")
            return SpotAnnouncementResponse()
        
        if not self.easy_mode:
            robot_transform = self.get_robot_global_transform()
            if not robot_transform:
                rospy.logerr("could not get global transform of the robot!")
                return SpotAnnouncementResponse()
            
            dist = np.sqrt((spot_gtruth[0,3]-robot_transform.translation.x)**2+(spot_gtruth[1,3]-robot_transform.translation.y)**2)

            if dist > 0.05:
                rospy.logerr("robot too far from the treasure!")
                return SpotAnnouncementResponse()
        
        if spot_id in self.found_frames:
            rospy.logwarn("you had already announced this spot!")
        else:
            self.spawn_treasure_pose_model(spot_id)
            self.found_frames.append(spot_id)

        rospy.loginfo("%s treasures found out of %s, Good Job!"%(len(self.found_frames), len(self.spots_world_frames)))
        if len(self.found_frames) == len(self.spots_world_frames):
            rospy.loginfo("All treasures are found, Congrats!")

        resp = SpotAnnouncementResponse()
        resp.success = True
        for clue in self.clues_with_frames[spot_id]:
            resp.clues.append(transform_matrix_to_TransformStamped(clue[1],str(clue[0][0]),str(clue[0][1])))

        return resp

if __name__ == "__main__":
    referee = Referee()
    referee.run()
