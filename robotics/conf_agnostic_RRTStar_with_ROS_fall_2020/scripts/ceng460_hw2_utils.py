#!/usr/bin/env python
import numpy as np
from geometry_msgs.msg import Pose, Transform, PoseStamped
from copy import deepcopy
import tf.transformations

def Pose_to_matrix(pose):
    quaternion = np.array([
        pose.orientation.x,
        pose.orientation.y,
        pose.orientation.z,
        pose.orientation.w
    ])

    matrix = tf.transformations.quaternion_matrix(quaternion)

    matrix[0,3] = pose.position.x
    matrix[1,3] = pose.position.y
    matrix[2,3] = pose.position.z

    return matrix

def matrix_to_Pose(matrix):
    pose = Pose()

    pose.position.x = matrix[0,3]
    pose.position.y = matrix[1,3]
    pose.position.z = matrix[2,3]

    quaternion = tf.transformations.quaternion_from_matrix(matrix)

    pose.orientation.x = quaternion[0]
    pose.orientation.y = quaternion[1]
    pose.orientation.z = quaternion[2]
    pose.orientation.w = quaternion[3]

    return pose

def Transform_to_matrix(transform):
    quaternion = np.array([
        transform.rotation.x,
        transform.rotation.y,
        transform.rotation.z,
        transform.rotation.w
    ])

    matrix = tf.transformations.quaternion_matrix(quaternion)

    matrix[0,3] = transform.translation.x
    matrix[1,3] = transform.translation.y
    matrix[2,3] = transform.translation.z

    return matrix

def Pose_to_Transform(pose):
    transform = Transform()
    transform.translation.x = pose.position.x
    transform.translation.y = pose.position.y
    transform.translation.z = pose.position.z

    transform.rotation.x = pose.orientation.x
    transform.rotation.y = pose.orientation.y
    transform.rotation.z = pose.orientation.z
    transform.rotation.w = pose.orientation.w
    
    return transform

def Transform_to_Pose(transform):
    pose = Pose()
    pose.position.x = transform.translation.x
    pose.position.y = transform.translation.y
    pose.position.z = transform.translation.z

    pose.orientation.x = transform.translation.x
    pose.orientation.y = transform.translation.y
    pose.orientation.z = transform.translation.z
    pose.orientation.w = transform.translation.w

    return pose

def matrix_to_Transform(matrix):
    transform = Transform()

    transform.translation.x = matrix[0,3]
    transform.translation.y = matrix[1,3]
    transform.translation.z = matrix[2,3]

    quaternion = tf.transformations.quaternion_from_matrix(matrix)

    transform.rotation.x = quaternion[0]
    transform.rotation.y = quaternion[1]
    transform.rotation.z = quaternion[2]
    transform.rotation.w = quaternion[3]
    
    return transform

def Pose_to_PoseStamped(pose, frame):
    poseStamped = PoseStamped()
    poseStamped.pose = deepcopy(pose)
    poseStamped.header.frame_id = frame

    return poseStamped

def make_Pose(x, y, z, r=0, p=0, yw=0):
    pose = Pose()

    pose.position.x = x
    pose.position.y = y
    pose.position.z = z

    quaternion = tf.transformations.quaternion_from_euler(r, p, yw)

    pose.orientation.x = quaternion[0]
    pose.orientation.y = quaternion[1]
    pose.orientation.z = quaternion[2]
    pose.orientation.w = quaternion[3]

    return pose

def make_PoseStamped(x, y, z, r=0, p=0, yw=0, frame="world"):
    poseStamped = PoseStamped()

    poseStamped.pose.position.x = x
    poseStamped.pose.position.y = y
    poseStamped.pose.position.z = z

    quaternion = tf.transformations.quaternion_from_euler(r, p, yw)

    poseStamped.pose.orientation.x = quaternion[0]
    poseStamped.pose.orientation.y = quaternion[1]
    poseStamped.pose.orientation.z = quaternion[2]
    poseStamped.pose.orientation.w = quaternion[3]

    poseStamped.header.frame_id = frame

    return poseStamped

def angdiff(angle1, angle2):
    return ((angle1-angle2 + np.pi) % (2*np.pi)) - np.pi