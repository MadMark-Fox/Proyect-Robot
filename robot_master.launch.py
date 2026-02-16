from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 1. Puente WebSockets (Puerto 9090)
        Node(package='rosbridge_server', executable='rosbridge_websocket', name='bridge'),

        # 2. Servidor de Vídeo (Puerto 8080)
        Node(package='web_video_server', executable='web_video_server', name='video', parameters=[{'port': 8080}]),

        # 3. Driver Motores
        Node(package='ros_base', executable='/usr/bin/python3', arguments=['/home/ubuntu/driver_motores.py'], name='motors'),

        # 4. Servidor Web para la App (Puerto 80)
        ExecuteProcess(cmd=['python3', '-m', 'http.server', '80', '--directory', '/home/ubuntu/robot_web'], output='screen')
    ])