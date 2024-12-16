# tony-bot

# dependency
sudo apt install ros-<ros2-distro>-joint-state-publisher-gui
sudo apt install ros-<ros2-distro>-xacro

# workspace
ros2 pkg create --build-type ament_cmake sam_bot_description

# launching project after successful colcon build
ros2 launch urdf_viz display.launch.py