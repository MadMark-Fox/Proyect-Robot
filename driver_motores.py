import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

# --- CONFIGURACIÓN DE PINES (MODIFICA ESTO SI ES NECESARIO) ---
# Motor Izquierdo
ENA = 12
IN1 = 23
IN2 = 24

# Motor Derecho
ENB = 13
IN3 = 5
IN4 = 6

class DriverMotores(Node):
    def __init__(self):
        super().__init__('driver_motores')
        # Nos suscribimos a las órdenes de la App
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        
        # Configuración de GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        pines = [ENA, IN1, IN2, ENB, IN3, IN4]
        GPIO.setup(pines, GPIO.OUT)

        # Configurar PWM (Control de velocidad) a 100Hz
        self.pwm_a = GPIO.PWM(ENA, 100)
        self.pwm_b = GPIO.PWM(ENB, 100)
        self.pwm_a.start(0)
        self.pwm_b.start(0)

        self.get_logger().info('Driver de Motores Iniciado. Esperando comandos...')

    def listener_callback(self, msg):
        # 1. Leer los datos del mensaje Twist
        velocidad_x = msg.linear.x   # Avance (entre -1.0 y 1.0)
        giro_z = msg.angular.z       # Giro (entre -1.0 y 1.0)

        # 2. Calcular velocidad para cada motor (Mezcla diferencial)
        # Izquierda = Avance - Giro
        # Derecha   = Avance + Giro
        vel_izq = velocidad_x - giro_z
        vel_der = velocidad_x + giro_z

        # 3. Limitar valores (Clamp) para no pasarnos de 1.0
        vel_izq = max(min(vel_izq, 1.0), -1.0)
        vel_der = max(min(vel_der, 1.0), -1.0)

        # 4. Mover los motores
        self.mover_motor(self.pwm_a, IN1, IN2, vel_izq)
        self.mover_motor(self.pwm_b, IN3, IN4, vel_der)

    def mover_motor(self, pwm, pin_a, pin_b, velocidad):
        # Convertir velocidad (-1.0 a 1.0) a Duty Cycle (0 a 100)
        duty_cycle = abs(velocidad) * 100
        
        if velocidad > 0:
            # Hacia delante
            GPIO.output(pin_a, GPIO.HIGH)
            GPIO.output(pin_b, GPIO.LOW)
        elif velocidad < 0:
            # Hacia atrás
            GPIO.output(pin_a, GPIO.LOW)
            GPIO.output(pin_b, GPIO.HIGH)
        else:
            # Parar
            GPIO.output(pin_a, GPIO.LOW)
            GPIO.output(pin_b, GPIO.LOW)
        
        # Aplicar la potencia
        pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        # Parada de emergencia al cerrar
        self.pwm_a.stop()
        self.pwm_b.stop()
        GPIO.cleanup()

def main(args=None):
    rclpy.init(args=args)
    driver = DriverMotores()
    try:
        rclpy.spin(driver)
    except KeyboardInterrupt:
        pass
    finally:
        driver.stop()
        driver.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()