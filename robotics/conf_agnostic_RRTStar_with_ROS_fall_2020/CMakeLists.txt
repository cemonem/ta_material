cmake_minimum_required(VERSION 3.0.2)
project(ceng460_hw2)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

find_package(catkin REQUIRED roscpp rospy gazebo_ros message_generation std_msgs std_srvs)

# find_package(Boost REQUIRED COMPONENTS system)
find_package(gazebo REQUIRED)

################################################
## Declare ROS messages, services and actions ##
################################################




###################################
## catkin specific configuration ##
###################################

catkin_package(
  DEPENDS
    message_runtime
    std_msgs
    std_srvs
    rospy
    gazebo_dev
    roscpp
    gazebo_ros
)

###########
## Build ##
###########

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

add_library(Ceng460Hw2WorldPlugin src/ceng460_hw2_world_plugin.cpp)
target_link_libraries(Ceng460Hw2WorldPlugin ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})