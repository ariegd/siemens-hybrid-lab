import os
import json
import time
import requests
import paho.mqtt.client as mqtt

# Configuración mediante variables de entorno o estáticas
MQTT_BROKER = os.getenv("MQTT_HOST", "localhost")
MQTT_TOPIC = "factory/telemetry"
CLOUD_API_URL = os.getenv("CLOUD_API_URL", "http://34.175.205.123:8000/predict")

def on_connect(client, userdata, flags, rc):
    print(f"Conectado al Broker MQTT local con código: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        # 1. Recibir datos del Edge (ESP32 / Sensores)
        payload = json.loads(msg.payload.decode())
        print(f"\n[Fog] Datos recibidos del Edge: {payload}")
        
        # 2. Enviar lote a la IA en Google Cloud (Baja Latencia)
        start_time = time.time()
        response = requests.post(CLOUD_API_URL, json=payload, timeout=5)
        latency = (time.time() - start_time) * 1000
        
        # 3. Procesar respuesta de la IA
        if response.status_code == 200:
            result = response.json()
            print(f"[Cloud AI] Respuesta recibida en {latency:.2f}ms")
            print(f"[Resultado] Anomalía: {result['anomaly']} | Acción: {result['recommendation']}")
            
            # Aquí Siemens Industrial Edge ejecutaría la lógica de parada instantánea
            if result['anomaly']:
                print("🚨 [ALERTA OT] Deteniendo línea de producción localmente.")
        else:
            print(f"[Error Cloud] Código de estado: {response.status_code}")
            
    except Exception as e:
        print(f"[Error Fog] Problema procesando el mensaje: {e}")

# Inicializar cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Iniciando Procesador Fog de la Planta...")
client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()
