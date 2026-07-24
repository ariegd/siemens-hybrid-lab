import json
import random
import time
import paho.mqtt.client as mqtt

# Conectar al broker local de Docker
client = mqtt.Client()
client.connect("localhost", 1883, 60)

print("Empezando simulación del brazo robótico (Edge)... Presiona Ctrl+C para parar.")

try:
    while True:
        # Generamos telemetría normal con picos anómalos aleatorios
        vibracion = round(random.uniform(1.0, 3.5), 2)
        temperatura = round(random.uniform(50.0, 70.0), 2)

        # Forzar anomalía simulada cada 5 ciclos
        if random.random() > 0.8:
            vibracion = round(random.uniform(4.6, 6.0), 2)
            print("⚠️ [Edge] Generando pico de vibración crítico simulado...")

        payload = {
            "sensor_id": "siemens_robot_arm_06",
            "vibration": vibracion,
            "temperature": temperatura,
            "timestamp": time.time()
        }

        client.publish("factory/telemetry", json.dumps(payload))
        print(f"[Edge] Telemetría enviada: Vb: {vibracion}G | Temp: {temperatura}°C")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulación finalizada.")
