# Robo Nurse – Autonomous Mobile Robot (ROS2 Navigation)

## Overview
Robo Nurse is a differential-drive Autonomous Mobile Robot developed using ROS2 Humble for reliable indoor service navigation. The system integrates custom kinematic modeling, PID-based motion control, SLAM-driven mapping, and Nav2-based autonomous planning to enable stable and collision-free autonomous movement in structured indoor environments. The complete navigation stack was validated in both simulation and real-world deployment.

## System Architecture
The system follows a modular layered architecture:
### Low-Level Control Layer
- Custom odometry computation for differential-drive kinematics
- PID-based velocity control for accurate trajectory tracking
- Real-time tuning for stable motion execution
### Localization & Mapping Layer
- SLAM-based map generation
- AMCL-based localization
- LiDAR and wheel-odometry fusion for state estimation
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
- Achieved stable trajectory tracking through tuned PID control
- Successfully generated consistent 2D maps using SLAM
- Demonstrated reliable autonomous navigation in simulation and hardware

## Demonstration
🎥 Simulation Demo: [Watch Here](https://youtube.com/yourlink)
🎥 Hardware Demo: [Watch Here](https://youtube.com/yourlink)

## CAD Model
🛠 CAD Model (Full Assembly): [View on GrabCAD](https://grabcad.com/yourlink)
