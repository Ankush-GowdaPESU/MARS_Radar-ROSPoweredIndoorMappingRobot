import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('radar_mapper')
    urdf_file = os.path.join(pkg, 'urdf', 'robot.urdf.xacro')
    world_file = os.path.join(pkg, 'worlds', 'indoor.sdf')
    bridge_cfg = os.path.join(pkg, 'config', 'bridge.yaml')
    slam_cfg = os.path.join(pkg, 'config', 'slam.yaml')

    robot_desc = xacro.process_file(urdf_file).toxml()

    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'),
                         'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': f'-r {world_file}'}.items())

    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               parameters=[{'robot_description': robot_desc, 'use_sim_time': True}])

    spawn = Node(package='ros_gz_sim', executable='create',
                 arguments=['-topic', 'robot_description',
                            '-name', 'radar_bot',
                            '-x', '0', '-y', '0', '-z', '0.1'],
                 output='screen')

    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                  parameters=[{'config_file': bridge_cfg, 'use_sim_time': True}],
                  output='screen')

    static_tf_radar = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0',
                   'radar_link',
                   'radar_bot/base_footprint/radar'],
        parameters=[{'use_sim_time': True}],
        output='screen')

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('slam_toolbox'),
                         'launch', 'online_sync_launch.py')]),
        launch_arguments={
            'use_sim_time': 'true',
            'slam_params_file': slam_cfg,
        }.items())

    rviz = Node(package='rviz2', executable='rviz2',
                arguments=['-d', os.path.join(pkg, 'rviz', 'view.rviz')],
                parameters=[{'use_sim_time': True}])

    return LaunchDescription([gz, rsp, spawn, bridge, static_tf_radar, slam, rviz])
    
