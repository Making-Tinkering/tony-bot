# tony-bot

# git - fetch and merge

git branch

git fetch --prune origin

git merge origin/main

# dependency

sudo apt install ros-humble-joint-state-publisher-gui

sudo apt install ros-humble-xacro

# workspace

ros2 pkg create --build-type ament_cmake <workspace_name>

# launching project after successful colcon build

ros2 launch urdf_viz display.launch.py