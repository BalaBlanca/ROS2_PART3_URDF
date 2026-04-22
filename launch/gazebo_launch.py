import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(
        package='dif_bot_description').find('dif_bot_description')
    
    # Rutas de archivos
    default_model_path = os.path.join(
        pkg_share, 'src/description/dif_bot_description.urdf.xacro')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')
    world_path = os.path.join(pkg_share, 'world/my_world.sdf')

    # Nodo: Robot State Publisher
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )

    # Nodo: Joint State Publisher
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
    )

    # Nodo: RViz2
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    # Nodo: Spawn Entity (Modificado para Gazebo Sim/Ignition)
    # Se cambia 'gazebo_ros' por 'ros_gz_sim' y el ejecutable por 'create'
    spawn_entity = launch_ros.actions.Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'dif_bot', '-topic', 'robot_description'],
        output='screen'
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='model', default_value=default_model_path,
            description='Ruta al URDF'),
        
        launch.actions.DeclareLaunchArgument(
            name='rvizconfig', default_value=default_rviz_config_path,
            description='Ruta al config RViz'),

        # Ejecución de Gazebo Sim (Modificado)
        # '-r' sirve para que la simulación inicie corriendo automáticamente
        launch.actions.ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_path],
            output='screen'),

        joint_state_publisher_node,
        robot_state_publisher_node,
        spawn_entity,
        rviz_node,
    ])