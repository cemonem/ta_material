cd /workspace/src/_lib/universal_robot; git checkout melodic-devel
sudo apt update
sudo apt install -y ros-melodic-moveit
apt-get update
apt-get --only-upgrade install ros-melodic-genpy
cd /workspace/src/;
rosdep install -y --from-paths . --ignore-src --rosdistro melodic
cd /workspace/;
catkin config --extend /opt/ros/melodic --cmake-args -DCMAKE_BUILD_TYPE=Release
catkin_make
source /workspace/devel/setup.bash
