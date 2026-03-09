# Robot 🤖

[![ROS 2](https://img.shields.io/badge/ROS2-Humble/Foxy-blue)](https://docs.ros.org/)
[![Python](https://img.shields.io/badge/Python-3.10-yellow)](https://www.python.org/)

Proyecto de Fin de Grado (TFG) para el ciclo de **Administración de Sistemas Informáticos en Red (ASIR)**. Consiste en un robot autónomo y controlado a distancia con capacidades de soporte a guardias mediante visión artificial.

---

## 📝 Descripción del Proyecto
El **ASIR-TFGRobot** es un sistema robótico diseñado para labores de vigilancia. Su núcleo combina la potencia de **ROS 2** para la gestión de procesos y un sistema de **visión artificial** capaz de detectar emociones humanas, permitiendo una interacción avanzada y un control remoto fluido a través de una interfaz web.

### Características Principales
* **Control Remoto:** Gestión del movimiento a través de una interfaz web (`index.html`).
* **Visión Artificial:** Detección de emociones en tiempo real para soporte en tareas de guardia.
* **Arquitectura Modular:** Basado en nodos de ROS 2 para facilitar la escalabilidad.

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.
* **Framework Robótico:** ROS 2.
* **IA y Visión:** OpenCV / Procesamiento de imagen.
* **Control de Hardware:** Driver de motores mediante GPIO.
* **Frontend:** HTML/JS para el panel de control.

---

## 📂 Estructura del Repositorio
* `emotion_node.py`: Nodo de ROS 2 encargado del procesamiento de imágenes y detección facial/emocional.
* `driver_motores.py`: Control lógico de los motores del robot.
* `robot_master.launch.py`: Archivo de lanzamiento que orquesta el inicio de todos los nodos.
* `index.html`: Interfaz de usuario para el control remoto del robot.
* `Proyecto Fin de Grado Marcos.pdf`: Documentación técnica completa.

---
