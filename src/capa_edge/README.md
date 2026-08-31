# Capa Edge: Industrial Telemetry Simulation & Firmware
Módulo encargado de generar o capturar telemetría en tiempo real desde el nivel de campo (sensores de vibración $G$ y temperatura $^{\circ}\text{C}$).

---

## Contenido del Módulo

* **`simulador_edge.py`**: Script en Python que simula la operación de un brazo robótico industrial (`siemens_robot_arm_06`), publicando datos en el broker MQTT local y generando picos críticos aleatorios para evaluar la parada de la línea.
* **`esp32-c6.py`**: Script de apoyo / prueba para la integración con microcontroladores Espressif ESP32-C6 sobre redes de bajo consumo.
* **`docker-compose.yml`**: Configuración auxiliar para ejecutar el simulador en un contenedor aislado si fuera necesario.

---

## Ejecución del Simulador
1. Requisitos
```bash
pip install paho-mqtt
```

2. Lanzar la simulación
```bash
python3 simulador_edge.py
```

---

## Ejemplo de Salida:
```bash
[Edge] Telemetría enviada: Vb: 2.27G | Temp: 64.02°C
⚠️ [Edge] Generando pico de vibración crítico simulado...
[Edge] Telemetría enviada: Vb: 5.02G | Temp: 56.28°C
```
