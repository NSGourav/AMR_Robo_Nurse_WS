# Robo Nurse – Autonomous Mobile Robot (ROS2 Navigation)

## Overview
Robo Nurse is a differential-drive Autonomous Mobile Robot developed using ROS2 Humble to achieve reliable indoor navigation. The system integrates custom kinematic modeling, PID-based motion control, SLAM-driven mapping, and Nav2-based autonomous planning. The complete navigation stack was validated in both simulation and real-world deployment.

## System Architecture
The robot operates using a layered architecture:
### Low-Level Control Layer
- Custom odometry computation for differential-drive kinematics
- PID-based velocity control for accurate trajectory tracking
- Real-time tuning for stable motion execution
### Localization & Mapping Layer
- SLAM-based map generation
- AMCL-based localization
- Sensor fusion using LiDAR and odometry
### Navigation Layer
- ROS2 Nav2 stack integration
- Global path planning
- Local obstacle avoidance
- Waypoint-based mission execution

## Launch
```bash
ros2 launch amr_navigation bringup.launch.py
```

## Results

## Demonstration
🎥 Simulation Demo: [Watch Here](https://youtube.com/yourlink)
🎥 Hardware Demo: [Watch Here](https://youtube.com/yourlink)

## CAD Model
🛠 CAD Model (Full Assembly): [View on GrabCAD](https://grabcad.com/yourlink)
