import json
import random
import time
import paho.mqtt.client as mqtt

# Conectar al broker Docker local
client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    # Simulación de telemetría de un brazo robótico
    payload = {
        "sensor_id": "robot_arm_01",
        "vibration": round(random.uniform(1.2, 5.8), 2),
        "temperature": round(random.uniform(45.0, 85.0), 2),
        "timestamp": time.time()
    }
    
    client.publish("factory/telemetry", json.dumps(payload))
    print(f"Enviado: {payload}")
    time.sleep(1) # 1 hercio (un dato por segundo)
