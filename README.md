# Radar-based Indoor Mapping using ROS2

## Overview
This project implements a real-time indoor mapping system using a radar-like sensor in Gazebo, integrated with ROS2 and SLAM Toolbox.

## Pipeline
Gazebo Simulation → Robot Model → Sensor Data → ROS2 Bridge → SLAM Toolbox → RViz

## Features
- Simulated radar sensor using LiDAR
- Real-time SLAM mapping
- ROS2–Gazebo integration
- Occupancy grid map generation

## Technologies Used
- ROS2 (Jazzy)
- Gazebo
- SLAM Toolbox
- RViz

## How to Run

Terminal 1:

colcon build --symlink-install
source install/setup.bash
ros2 launch radar_mapper mapping.launch.py

Terminal 2:

cd ~/radar_mapping_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
