from geometry_msgs.msg import TransformStamped
import numpy as np
import tf.transformations

def TransformStamped_to_transform_matrix(transformStamped):
    quaternion = np.array([
        transformStamped.transform.rotation.x,
        transformStamped.transform.rotation.y,
        transformStamped.transform.rotation.z,
        transformStamped.transform.rotation.w
    ])

    matrix = tf.transformations.quaternion_matrix(quaternion)

    matrix[0,3] = transformStamped.transform.translation.x
    matrix[1,3] = transformStamped.transform.translation.y
    matrix[2,3] = transformStamped.transform.translation.z

    return matrix

def transform_matrix_to_TransformStamped(matrix, frame_id, child_frame_id):
    transformStamped = TransformStamped()

    transformStamped.header.frame_id = frame_id
    transformStamped.child_frame_id = child_frame_id

    transformStamped.transform.translation.x = matrix[0,3]
    transformStamped.transform.translation.y = matrix[1,3]
    transformStamped.transform.translation.z = matrix[2,3]

    quaternion = tf.transformations.quaternion_from_matrix(matrix)

    transformStamped.transform.rotation.x = quaternion[0]
    transformStamped.transform.rotation.y = quaternion[1]
    transformStamped.transform.rotation.z = quaternion[2]
    transformStamped.transform.rotation.w = quaternion[3]
    
    return transformStamped
