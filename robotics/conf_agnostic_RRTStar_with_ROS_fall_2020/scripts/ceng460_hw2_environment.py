#!/usr/bin/env python
import cmd
import rospy
import moveit_commander
import sys
import moveit_msgs.msg
import math
import geometry_msgs.msg
from copy import deepcopy
import argparse
import code
import numpy as np
import tf.transformations
import ceng460_hw2_utils
import spawn_obstacles
import std_srvs.srv
import actionlib
import control_msgs.msg
import trajectory_msgs.msg

HW2_OBJECT_SIZE = (0.1, 0.1, 0.1)
EUC_VELOCITY = 1.0
MIN_EUC_TIME = 2.0

class Ceng460Hw2Environment:
    def __init__(self):
        rospy.init_node("ceng460_hw2_environment")

        parser = argparse.ArgumentParser()
        parser.add_argument("-obstacles", type=str, required=True)

        args = parser.parse_args(args=rospy.myargv()[1:])

        rospy.wait_for_service("gazebo/attach_object")
        rospy.wait_for_service("compute_ik")
        rospy.wait_for_service("check_state_validity")

        self.attach_service = rospy.ServiceProxy("gazebo/attach_object", std_srvs.srv.Trigger)
        self.compute_ik_service = rospy.ServiceProxy("compute_ik", moveit_msgs.srv.GetPositionIK)
        self.follow_joint_trajectory_action_client = actionlib.SimpleActionClient("arm_controller/follow_joint_trajectory", control_msgs.msg.FollowJointTrajectoryAction)
        self.follow_joint_trajectory_action_client.wait_for_server()

        self.check_state_validity = rospy.ServiceProxy("check_state_validity", moveit_msgs.srv.GetStateValidity)

        moveit_commander.roscpp_initialize(sys.argv)
        self.robot_commander =  moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface(synchronous=True, service_timeout=None)
        self.move_group = moveit_commander.MoveGroupCommander("manipulator", wait_for_servers=60.0)

        if args.obstacles == "true":
            spawn_obstacles.set_planning_scene(self.scene)
        init_pose_dict = rospy.get_param("hw2_object/init_pose")
        final_pose_dict = rospy.get_param("hw2_object/final_pose")

        self.final_object_pose = ceng460_hw2_utils.make_Pose(final_pose_dict["x"], final_pose_dict["y"], final_pose_dict["z"])

        box_pose = geometry_msgs.msg.PoseStamped()
        box_pose.header.frame_id = "world"
        box_pose.pose.orientation.w = 1.0
        box_pose.pose.position.x = init_pose_dict["x"]
        box_pose.pose.position.y = init_pose_dict["y"]
        box_pose.pose.position.z = init_pose_dict["z"]
        self.scene.add_box("hw2_object", box_pose, size=HW2_OBJECT_SIZE)

        self.attached = False

    def get_end_effector_global_pose(self):
        '''
        returns current global pose of the end_effector as geometry_msgs.msg.Pose type.
        '''
        poseStamped = self.move_group.get_current_pose()
        assert(poseStamped.header.frame_id == "world")
        return poseStamped.pose

    def get_object_global_pose(self):
        '''
        returns current global pose of the object as geometry_msgs.msg.Pose type.
        '''
        if self.attached:
            attached_object = self.scene.get_attached_objects()["hw2_object"]
            assert(attached_object.object.header.frame_id == "ee_link")
            attached_rel_mat = ceng460_hw2_utils.Pose_to_matrix(attached_object.object.primitive_poses[0])
            eef_mat = ceng460_hw2_utils.Pose_to_matrix(self.get_end_effector_global_pose())
            return ceng460_hw2_utils.matrix_to_Pose(np.matmul(eef_mat,attached_rel_mat))
        else:
            free_object = self.scene.get_objects()["hw2_object"]
            assert(free_object.header.frame_id == "world")
            return free_object.primitive_poses[0]

    def compute_ik(self, pose, frame, timeout=10.0):
        '''
        Computes joint values for end effector pose given in frame. joints are in the same order with the joint_values argument of
        move_joints method. pose is a geometry_msgs.msg.Pose type. frame is the reference frame string of the pose (e.g. "world","ee_link")
        '''
        poseStamped =  ceng460_hw2_utils.Pose_to_PoseStamped(pose, frame)
        req = moveit_msgs.srv.GetPositionIKRequest()
        req.ik_request.group_name = "manipulator"

        # There is no documentation regarding this doing anything. Still putting it in.
        req.ik_request.avoid_collisions = True

        req.ik_request.pose_stamped = poseStamped
        req.ik_request.timeout = rospy.Duration.from_sec(timeout)

        req.ik_request.robot_state.joint_state.name = ["shoulder_pan_joint",
            "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
        req.ik_request.robot_state.joint_state.position = self.get_current_joint_values()

        # There is no documentation regarding this doing anything. Still putting it in.
        if self.attached:
            req.ik_request.robot_state.attached_collision_objects = [self.scene.get_attached_objects()["hw2_object"]]

        try:
            resp = self.compute_ik_service(req)
        except rospy.ServiceException as exc:
            rospy.logfatal("Service did not process request: " + str(exc))

        if(resp.error_code.val != 1):
            rospy.logwarn("No ik solution found (error code %s) for pose %s"%(resp.error_code.val, poseStamped))

        return resp.solution.joint_state.position, resp.error_code.val == 1


    def attach(self):
        '''
        attempts to attach the object to the end_effector. returns True if successful.
        if successful, collision checks take the object into account in queries after this call as if it is attached.
        the attached object position will also be updated in the collision scene as the end effector moves.
        '''
        if self.attached:
            rospy.logwarn("object already attached!")
            return False
        try:
            resp = self.attach_service(std_srvs.srv.TriggerRequest())
        except rospy.ServiceException as exc:
            rospy.logfatal("Service did not process request: " + str(exc))

        if resp.success:
            self.scene.attach_box("ee_link", "hw2_object")
            self.attached = True

        return resp.success

    def detach(self):
        '''
        attempts to attach the object to the end_effector. returns True if successful.
        if successful, collision checks take the object into account in queries after this call as if it is free.
        '''
        if not self.attached:
            rospy.logwarn("object already detached!")
            return False
        try:
            resp = self.attach_service(std_srvs.srv.TriggerRequest())
        except rospy.ServiceException as exc:
            rospy.logfatal("Service did not process request: " + str(exc))

        if resp.success:
            self.scene.remove_attached_object("ee_link")
            self.attached = False

        return resp.success

    def move_joints(self, joint_values):
        '''
        takes a list containing joint values in float, in the range [-pi pi]
        the order of values should be: [shoulder_pan_joint,
        shoulder_lift_joint, elbow_joint, wrist_1_joint, wrist_2_joint, wrist_3_joint]
        joints draw the shortest linear (not in terms of end effector, in terms of angles) trajectory with constant velocity. accelerations are impulsive and ideal.
        The arrival time is determined wrt euclidean_distance/EUC_VELOCITY of the joint_values to current state. The arrival time cannot be lower than MIN_EUC_TIME.
        returns True if successful.
        '''

        joint_values = tuple(joint_values)

        trajectory = trajectory_msgs.msg.JointTrajectory()
        trajectory.joint_names = ["shoulder_pan_joint",
            "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
        next_point = trajectory_msgs.msg.JointTrajectoryPoint()
        next_point.positions = joint_values

        current_joint_values = self.get_current_joint_values()
        assert(len(joint_values) == 6)

        euclidean_time = np.sqrt(sum([ceng460_hw2_utils.angdiff(v,cv)**2 for (v,cv) in zip(joint_values, current_joint_values)]))/EUC_VELOCITY
        arrival_time = max(euclidean_time, MIN_EUC_TIME)
        next_point.time_from_start = rospy.Duration.from_sec(arrival_time)

        trajectory.points = [next_point]

        self.follow_joint_trajectory_action_client.send_goal(control_msgs.msg.FollowJointTrajectoryGoal(trajectory=trajectory))
        self.follow_joint_trajectory_action_client.wait_for_result()

        error_code = self.follow_joint_trajectory_action_client.get_result().error_code
        if(error_code != 0):
            rospy.logwarn("Something is seriously wrong. Did you hit somewhere? Could not follow trajectory. JointTrajectoryAction error_code: %s"%error_code)

        return error_code == 0

    def get_current_joint_values(self):
        '''returns current joint values in the same fashion as the joint_values argument of move_joints'''
        return self.move_group.get_current_joint_values()

    def check_collision(self, joint_values, attached_object_pose=None, attached_object_reference_frame="world"):
        '''
        checks if the configuration specified by joint_values is valid, returns True if no collision. If an object is attached,
        it is taken into collision calculations. joint_values are indicated the same way
        as move_joints method. The attached_object_pose argument takes a geometry_msgs.msg.Pose type.
        If this argument is not None, the collision checks are performed as if the object is attached to the
        end-effector, with the pose attached_objected_pose relative to the frame attached_object_reference_frame (no collision
        checks are performed to the possibly detached object itself). These two arguments are useful if one wants to "imagine" the object being
        attached to the end-effector when collision checking, without actually physically attaching to the object.
        '''
        joint_values = tuple(joint_values)
        removed_object = None

        get_state_validity_request = moveit_msgs.srv.GetStateValidityRequest()
        get_state_validity_request.group_name = "manipulator"
        get_state_validity_request.robot_state.joint_state.name = ["shoulder_pan_joint",
            "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
        get_state_validity_request.robot_state.joint_state.position = joint_values

        if self.attached and attached_object_pose == None:
            get_state_validity_request.robot_state.attached_collision_objects = [deepcopy(self.scene.get_attached_objects()["hw2_object"])]

        if attached_object_pose != None:
            #temporarily remove object and attach it at the specified pose
            if self.attached:
                removed_object = deepcopy(self.scene.get_attached_objects()["hw2_object"].object)
                self.scene.remove_attached_object("ee_link")
            else:
                removed_object = deepcopy(self.scene.get_objects()["hw2_object"])

            self.scene.remove_world_object("hw2_object")

            new_object = deepcopy(removed_object)
            new_object.header.frame_id = attached_object_reference_frame
            new_object.primitive_poses[0] = deepcopy(attached_object_pose)
            self.scene._PlanningSceneInterface__submit(new_object)
            self.scene.attach_box("ee_link","hw2_object")

            get_state_validity_request.robot_state.attached_collision_objects = [deepcopy(self.scene.get_attached_objects()["hw2_object"])]

        try:
            resp = self.check_state_validity(get_state_validity_request)
        except rospy.ServiceException as exc:
            rospy.logfatal("Service did not process request: " + str(exc))

        if removed_object != None:
            self.scene.remove_attached_object("ee_link")
            self.scene.remove_world_object("hw2_object")
            self.scene._PlanningSceneInterface__submit(removed_object)
            if self.attached:
                self.scene.attach_box("ee_link", "hw2_object")

        return resp.valid

    def declare_success(self):
        '''call this method when you place the box into its final position with identity global orientation.'''

        #https://math.stackexchange.com/questions/90081/quaternion-distance


        obj = ceng460_hw2_utils.Pose_to_matrix(self.get_object_global_pose())
        final_obj = ceng460_hw2_utils.Pose_to_matrix(self.final_object_pose)
        dist_diff = np.sqrt(np.sum((obj[0:3,3]-final_obj[0:3,3])**2))
        obj_quot = tf.transformations.quaternion_from_matrix(obj)
        final_quot = tf.transformations.quaternion_from_matrix(final_obj)

        quot_diff = 1-np.inner(obj_quot,final_quot)**2

        if quot_diff < 0.005 and dist_diff < 0.05 and not self.attached:
            rospy.loginfo("Congratulations on completing the assignment! Have a nice holiday!")
        else:
            rospy.loginfo("Unfortunately the task is still incomplete! Better luck next time!")







if __name__ == "__main__":
    try:
        pass
    except rospy.ROSInterruptException, KeyboardInterrupt:
        pass
