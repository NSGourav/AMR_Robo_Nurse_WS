import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro

def generate_launch_description():
    
    # ===================================================================================
    # ================================ COMMON PARAMETERS ================================
    # ===================================================================================
    package_name='servbot'
    share_dir = get_package_share_directory(package_name)

    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # Path to the URDF xacro file
    xacro_file = os.path.join(share_dir, 'description', 'robot.urdf.xacro')

    # Path to the world file
    world_file = os.path.join(share_dir, 'worlds', 'custom.world')
    
    # Path to your main controllers file
    controllers_yaml_path = os.path.join(share_dir, 'config', 'my_controllers.yaml')


    # ===================================================================================
    # ============================ COMPONENTS LAUNCHED ONCE =============================
    # ===================================================================================
    
    # --- GAZEBO ---
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch', 'gzserver.launch.py'
            ])
        ]),
        launch_arguments={'world': world_file}.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch', 'gzclient.launch.py'
            ])
        ])
    )
    
    

    # ===================================================================================
    # =========================== COMPONENTS LAUNCHED PER ROBOT =========================
    # ===================================================================================
    
    # --- Swarm Configuration ---
    number_of_robots = 2
    
    per_robot_actions = []

    for i in range(number_of_robots):
        robot_name = f"robot_{i}"
        namespace = f"robot_{i}"
        
        x_pos = float(i) * +1.0
        y_pos = float(i)* +1.0

        # --- ROBOT STATE PUBLISHER (rsp) ---
        # Process the xacro file using the Python library, which is more robust
        robot_description_config = xacro.process_file(xacro_file, mappings={
            'sim_mode': 'true', 
            'use_ros2_control': 'true',
            'prefix': namespace
        }).toxml()

        # Create the Robot State Publisher node directly here
        rsp_node = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=namespace,
            parameters=[
                controllers_yaml_path,
                {
                    'use_sim_time': use_sim_time,
                    'robot_description': robot_description_config,
                    'frame_prefix': f'{namespace}/'
                }
            ],
            remappings=[
                ('/tf', f'{namespace}/tf'),
                ('/tf_static', f'{namespace}/tf_static')
            ],
            output='screen'
        )

        # --- SPAWN ENTITY ---
        spawn_entity_node = Node(
            package='gazebo_ros', 
            executable='spawn_entity.py',
            arguments=[
                '-topic', f'{namespace}/robot_description',
                '-entity', robot_name,
                '-x', str(x_pos),
                '-y', str(y_pos),
                '-z', '0.2'
            ],
            output='screen'
        )

        # --- TWIST MUX ---
        twist_mux_params = os.path.join(share_dir, 'config', 'twist_mux.yaml')
        twist_mux_node = Node(
            package="twist_mux",
            executable="twist_mux",
            namespace=namespace,
            parameters=[twist_mux_params, {'use_sim_time': use_sim_time}],
            remappings=[
                ('/cmd_vel_out', 'diff_cont/cmd_vel_unstamped'),
                ('/cmd_vel_joy', f'/robot_0/cmd_vel_joy' if i == 0 else f'/{robot_name}/cmd_vel_joy')
            ]
        )

        # --- CONTROLLER SPAWNERS ---
        diff_drive_spawner_node = Node(
            package="controller_manager",
            executable="spawner",
            namespace = namespace,
            arguments=["diff_cont", "-c", "controller_manager","--wait"],
            output='screen'
        )

        joint_broad_spawner_node = Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_broad", "-c", "controller_manager","--wait"],
            remappings=[
            ('/tf', f'{namespace}/tf'),
            ('/tf_static', f'{namespace}/tf_static')
            ],
            output='screen'
        )

        per_robot_actions.extend([
            rsp_node,
            spawn_entity_node,
            #twist_mux_node,
            #diff_drive_spawner_node,
            joint_broad_spawner_node
        ])

    # ===================================================================================
    # =============================== ASSEMBLE LAUNCH DESC ==============================
    # ===================================================================================
    ld = LaunchDescription()

    ld.add_action(DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use sim time if true'))

    ld.add_action(gazebo_server)
    ld.add_action(gazebo_client)
    
    
    for action in per_robot_actions:
        ld.add_action(action)
    
    return ld