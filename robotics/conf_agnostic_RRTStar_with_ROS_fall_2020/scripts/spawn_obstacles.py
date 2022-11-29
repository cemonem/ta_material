#!/usr/bin/env python
import rospy
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest, SpawnModelResponse
from geometry_msgs.msg import Pose,PoseStamped
import argparse
import sys
import tf.transformations
import ceng460_hw2_utils
import numpy as np

#spawn an obstacle arrangement
#also functions for setting the planning scene for moveit

DILATION = 0.05
OBSTACLES = [(0.2,1.2,0,0.8,0.8,0.8),
             (0,0,-0.3,0.7,1.4,0.05),
             (-0.6,-0.6,0,0.8,0.05,0.8),
             (0.1,0,0.4,0.25,0.25,0.05)]
def modify_sdf(sdf,sx,sy,sz):
    return sdf.replace("<size>1 1 1</size>","<size>%f %f %f</size>"%(sx,sy,sz))

def spawn_box(pos_shape, gazebo, *argv):
    x,y,z,sx,sy,sz = pos_shape

    if gazebo:
        sdf,spawn_model_func,model_name = argv
        req = SpawnModelRequest()
        req.model_name = model_name
        req.model_xml = modify_sdf(sdf,sx,sy,sz)
        req.robot_namespace = model_name
        req.reference_frame = "world"
        req.initial_pose = Pose()
        req.initial_pose.position.x = x
        req.initial_pose.position.y = y
        req.initial_pose.position.z = z
        try:
            spawn_model_func(req)
        except rospy.ServiceException as exc:
            print "could not spawn all objects",str(exc)
    else:
        planning_scene_intf,model_name = argv
        box_pose = PoseStamped()
        box_pose.header.frame_id = "world"
        box_pose.pose.orientation.w = 1.0
        box_pose.pose.position.x = x
        box_pose.pose.position.y = y
        box_pose.pose.position.z = z
        planning_scene_intf.add_box(model_name, box_pose, size=(sx+DILATION,sy+DILATION,sz+DILATION))


def set_planning_scene(planning_scene_intf):
    for i,obs in enumerate(OBSTACLES):
        spawn_box(obs,False,planning_scene_intf,"obs_%d"%i)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-file", type=str, required=True)

        args = parser.parse_args(args=rospy.myargv()[1:])
        rospy.init_node("spawn_obstacles")
        rospy.loginfo("spawning obstacles with arguments: %s"% args)

        try:
            with open(args.file,"r") as f:
                sdf = f.read()
        except IOError:
            rospy.logerr("Unable to read %s"% args.file)
            exit()

        rospy.wait_for_service("/gazebo/spawn_sdf_model")
        spawn_model_func = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)

        for i,obs in enumerate(OBSTACLES):
            spawn_box(obs,True, sdf, spawn_model_func, "obs_%d"%i)

    except rospy.ROSInterruptException:
        pass