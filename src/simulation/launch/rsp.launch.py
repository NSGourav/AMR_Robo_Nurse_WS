import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    # --- Launch Arguments ---
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    namespace = LaunchConfiguration('namespace')
    frame_prefix = LaunchConfiguration('frame_prefix')
    params_file = LaunchConfiguration('params_file')

    # --- URDF Processing ---
    pkg_path = os.path.join(get_package_share_directory('servbot'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    
    # CORRECTED: The Command is now a clean list of arguments
    robot_description_config = Command([
        'xacro', ' ', xacro_file, ' ',
        'use_ros2_control:=', use_ros2_control, ' ',
        'sim_mode:=', use_sim_time, ' ',
        'prefix:=', namespace
    ])
    
    # --- Robot State Publisher Node ---
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        namespace=namespace,
        parameters=[
            params_file,
            {
                'robot_description': robot_description_config,
                'use_sim_time': use_sim_time,
                'frame_prefix': frame_prefix
            }
        ]
    )

    # --- Launch Description ---
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('use_ros2_control', default_value='true'),
        DeclareLaunchArgument('namespace', default_value=''),
        DeclareLaunchArgument('frame_prefix', default_value=''),
        DeclareLaunchArgument(
            'params_file',
            default_value=os.path.join(pkg_path, 'config', 'my_controllers.yaml')),
        node_robot_state_publisher
    ])