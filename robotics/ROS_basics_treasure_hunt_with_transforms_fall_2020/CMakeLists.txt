cmake_minimum_required(VERSION 3.0.2)
project(ceng460hw1)

add_compile_options(-std=c++11)


find_package(catkin REQUIRED COMPONENTS roscpp gazebo_ros gazebo_dev gazebo_msgs tf2_msgs std_msgs rospy geometry_msgs urdf xacro message_generation)

add_service_files(
   FILES
   SpotAnnouncement.srv
)

generate_messages(
   DEPENDENCIES
   std_msgs
   geometry_msgs
)

catkin_package(
   CATKIN_DEPENDS roscpp gazebo_ros gazebo_dev gazebo_msgs std_msgs rospy geometry_msgs message_runtime tf2_msgs
)

include_directories(${catkin_INCLUDE_DIRS})
