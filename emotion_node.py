import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from deepface import DeepFace
import cv2

class EmotionNode(Node):
    def __init__(self):
        super().__init__('emotion_detector')
        self.subscription = self.create_subscription(
            Image, '/image_raw', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(String, '/robot/emotion', 10)
        self.bridge = CvBridge()
        self.counter = 0

    def listener_callback(self, msg):
        self.counter += 1
        if self.counter % 10 != 0:
            return

        # Convertir ROS Image a OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        try:
            # actions=['emotion'] busca solo emociones
            objs = DeepFace.analyze(img_path = cv_image, actions = ['emotion'], enforce_detection=False)
            
            # Obtener la emoción dominante (ej: "sad", "happy", "neutral")
            dominant_emotion = objs[0]['dominant_emotion']
            
            # Publicar al sistema
            msg_out = String()
            msg_out.data = dominant_emotion
            self.publisher_.publish(msg_out)
            
            self.get_logger().info(f'Detectado: {dominant_emotion}')
            
        except Exception as e:
            self.get_logger().error('No se detectó cara o error en IA')

def main(args=None):
    rclpy.init(args=args)
    node = EmotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()