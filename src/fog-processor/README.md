# Capa Fog: Local Processing & OT Action Engine

Procesador analítico local que actúa como intermediario entre la red de campo (OT) y la nube (IT). Recibe telemetría vía MQTT, consulta la API Cloud y ejecuta decisiones críticas (como la parada de línea `STOP_LINE`) localmente.

---

## Tabla de Contenidos
- [1. Componentes de la Capa Fog](#1-componentes-de-la-capa-fog)
- [2. Configuración de Conexión Cloud (Cambio de VM)](#2-configuración-de-conexión-cloud-cambio-de-vm)
- [3. Configuración del Código Fuente (main.py)](#3-configuración-del-código-fuente-mainpy)
- [4. Comandos de Despliegue y Actualización Local](#4-comandos-de-despliegue-y-actualización-local)
- [5. Monitoreo y Salidas de Simulación](#5-monitoreo-y-salidas-de-simulación)
  - [5.1. Salida de la Capa Edge (Simulador)](#51-salida-de-la-capa-edge-simulador)
  - [5.2. Salida de la Capa Fog (Procesador Local)](#52-salida-de-la-capa-fog-procesador-local)

---

## 1. Componentes de la Capa Fog
La capa Fog se orquesta mediante `src/docker-compose.yml` e incluye tres servicios principales:

1. **`mqtt-broker` (`eclipse-mosquitto`)**: Broker MQTT expuesto en el puerto `1883` para comunicación de campo con el Edge.
2. **`fog-processor` (`ariegd/fog-processor`)**: Servicio en Python/C que procesa la telemetría enviada por los sensores y evalúa la respuesta de inferencia de la nube.
3. **`watchtower` (`containrrr/watchtower`)**: Servicio de Despliegue Continuo (CD) local que busca imágenes actualizadas en Docker Hub cada 30 segundos y reinicia el procesador sin intervención manual.

---

## 2. Configuración de Conexión Cloud (Cambio de VM)
Si la Máquina Virtual en Google Cloud Platform (GCP) se recrea o cambia su dirección IP pública externa, es necesario actualizar la variable de entorno `CLOUD_API_URL` en el archivo `src/docker-compose.yml`:

```yaml
  fog-processor:
    image: ariegd/fog-processor:latest
    container_name: factory_fog_processor
    depends_on:
      - mqtt-broker
    environment:
      - MQTT_HOST=mqtt-broker
      - CLOUD_API_URL=http://<NUEVA_IP_EXTERNA_GCP>:8000/predict
    networks:
      - factory-network
```

---

## 3. Configuración del Código Fuente (`main.py`)
Asegúrate de que la aplicación en `src/fog-processor/main.py` lea la variable de entorno de forma dinámica utilizando os.getenv en lugar de usar una dirección URL fija (hardcoded):

```python
import os

# Lectura dinámica de variables de entorno
MQTT_BROKER = os.getenv("MQTT_HOST", "localhost")
MQTT_TOPIC = "factory/telemetry"
CLOUD_API_URL = os.getenv("CLOUD_API_URL", "http://<NUEVA_IP_EXTERNA_GCP>:8000/predict")
```

---

## 4. Comandos de Despliegue y Actualización Local

### Arranque inicial de la infraestructura Fog
```bash
cd ~/Documentos/@Documentos/Doctorado2026/projects/siemens-hybrid-lab/src
docker compose up -d
```

### Actualización manual rápida tras la acción del Pipeline CI/CD   
Aunque Watchtower busca y aplica cambios automáticamente cada 30 segundos, puedes forzar la descarga e instalación inmediata de la última imagen compilada por GitHub Actions en Docker Hub ejecutando:

```bash
# 1. Descargar la versión más reciente del procesador Fog desde Docker Hub
docker compose pull fog-processor

# 2. Reiniciar el servicio aplicando la nueva imagen y variables de entorno
docker compose up -d fog-processor
```

---

## 5. Monitoreo y Salidas de Simulación

### 5.1. Salida de la Capa Edge (Simulador)
Ejecución del simulador de telemetría del brazo robótico desde la terminal local:

```bash
python3 simulador_edge.py
```

**Log de salida:**

```plaintext
Empezando simulación del brazo robótico (Edge)... Presiona Ctrl+C para parar.
[Edge] Telemetría enviada: Vb: 2.66G | Temp: 55.53°C
[Edge] Telemetría enviada: Vb: 2.89G | Temp: 55.93°C
[Edge] Telemetría enviada: Vb: 2.95G | Temp: 64.53°C
⚠️ [Edge] Generando pico de vibración crítico simulado...
[Edge] Telemetría enviada: Vb: 5.71G | Temp: 58.04°C
[Edge] Telemetría enviada: Vb: 3.27G | Temp: 69.36°C
[Edge] Telemetría enviada: Vb: 1.87G | Temp: 62.24°C
[Edge] Telemetría enviada: Vb: 2.29G | Temp: 63.56°C
⚠️ [Edge] Generando pico de vibración crítico simulado...
```

### 5.2. Salida de la Capa Fog (Procesador Local)
Monitorización en tiempo real de la recepción de datos MQTT y consultas de inferencia hacia la API en Google Cloud:

```bash
docker logs -f factory_fog_processor
```

**Log de salida:**

```plaintext
Iniciando Procesador Fog de la Planta...
Conectado al Broker MQTT local con código: 0

[Fog] Datos recibidos del Edge: {'sensor_id': 'siemens_robot_arm_06', 'vibration': 2.66, 'temperature': 55.53, 'timestamp': 1788288364.1210434}
[Cloud AI] Respuesta recibida en 114.18ms
[Resultado] Anomalía: False | Acción: CONTINUE

[Fog] Datos recibidos del Edge: {'sensor_id': 'siemens_robot_arm_06', 'vibration': 2.89, 'temperature': 55.93, 'timestamp': 1788288366.1214218}
[Cloud AI] Respuesta recibida en 145.65ms
[Resultado] Anomalía: False | Acción: CONTINUE

[Fog] Datos recibidos del Edge: {'sensor_id': 'siemens_robot_arm_06', 'vibration': 2.95, 'temperature': 64.53, 'timestamp': 1788288368.121775}
[Cloud AI] Respuesta recibida en 179.13ms
[Resultado] Anomalía: False | Acción: CONTINUE
```
