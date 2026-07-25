# siemens-hybrid-lab
Replica de manera exacta la jerarquía Edge-Fog-Cloud del ecosistema Siemens-NVIDIA usando herramientas de código abierto.

# Puesta en marcha en local (Modo CI/CD Actual)
Para poner a funcionar todo el sistema con las imágenes del registro remoto, ejecutar los siguientes comandos desde la carpeta donde tenemos `docker-compose.yml`
1. Descargar las imágenes oficiales
```
docker compose pull
```
2. Levantar el entorno completo
(Docker levantará mqtt-broker, fog-processor y watchtower).
```
docker compose up -d
```
3. Verificar los contenedores en marcha
Para poner en marcha y monitorizar la arquitectura completa en tiempo real, lo ideal es trabajar con 3 terminales abiertas en paralelo (una para cada capa):
```
docker compose ps
```
4. Terminal 1: Capa Cloud (VM en GCP)
```
# Acceso por ssh a la mv en google cloud
gcloud compute ssh siemens-cloud-ai --zone=europe-southwest1-a

# En la VM de GCP (~/cloud-api)
docker compose pull
docker compose up -d

# Ver
docker logs -f factory_cloud_ai
```
salida
```
zodd@siemens-cloud-ai:~/cloud-api$ docker logs -f factory_cloud_ai
[2026-07-25 12:45:45 +0000] [1] [INFO] Starting gunicorn 26.0.0
[2026-07-25 12:45:45 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
[2026-07-25 12:45:45 +0000] [1] [INFO] Using worker: sync
[2026-07-25 12:45:45 +0000] [6] [INFO] Booting worker with pid: 6
[2026-07-25 12:45:45 +0000] [7] [INFO] Booting worker with pid: 7
[2026-07-25 12:45:45 +0000] [1] [INFO] Control socket listening at /root/.gunicorn/gunicorn.ctl
[2026-07-25 13:15:48 +0000] [1] [INFO] Handling signal: term
[2026-07-25 13:15:48 +0000] [7] [INFO] Worker exiting (pid: 7)
[2026-07-25 13:15:48 +0000] [6] [INFO] Worker exiting (pid: 6)
[2026-07-25 13:15:52 +0000] [1] [INFO] Shutting down: Master
```
5. Terminal 2: Capa Fog (Procesador Industrial Local)
```
# Ver el procesamiento MQTT -> Cloud AI en tiempo real
docker logs -f factory_fog_processor

# Otra pestaña si queremos ver cómo Watchtower busca actualizaciones
docker logs -f factory_watchtower
```
Salida
```
[Fog] Datos recibidos del Edge: {'sensor_id': 'siemens_robot_arm_06', 'vibration': 4.99, 'temperature': 63.22, 'timestamp': 1784972861.732563}
[Cloud AI] Respuesta recibida en 22.28ms
[Resultado] Anomalía: False | Acción: CONTINUE

[Fog] Datos recibidos del Edge: {'sensor_id': 'siemens_robot_arm_06', 'vibration': 4.89, 'temperature': 53.44, 'timestamp': 1784972863.7332025}
[Cloud AI] Respuesta recibida en 29.77ms
[Resultado] Anomalía: False | Acción: CONTINUE

[Fog] Datos recibidos del Edge: {'sensor_id': 'siemens_robot_arm_06', 'vibration': 5.62, 'temperature': 53.66, 'timestamp': 1784972865.7339747}
[Cloud AI] Respuesta recibida en 29.08ms
[Resultado] Anomalía: False | Acción: CONTINUE

[Fog] Datos recibidos del Edge: {'sensor_id': 'siemens_robot_arm_06', 'vibration': 1.73, 'temperature': 57.79, 'timestamp': 1784972867.7352903}
[Cloud AI] Respuesta recibida en 38.94ms
[Resultado] Anomalía: False | Acción: CONTINUE
```
6. Terminal 3: Capa Edge (Simulador de Telemetría)
```
python3 simulador_edge.py
```
Salida
```
[Edge] Telemetría enviada: Vb: 2.27G | Temp: 64.02°C
[Edge] Telemetría enviada: Vb: 2.72G | Temp: 56.75°C
[Edge] Telemetría enviada: Vb: 2.5G | Temp: 54.44°C
[Edge] Telemetría enviada: Vb: 1.9G | Temp: 58.98°C
⚠️ [Edge] Generando pico de vibración crítico simulado...
[Edge] Telemetría enviada: Vb: 5.02G | Temp: 56.28°C
⚠️ [Edge] Generando pico de vibración crítico simulado...
[Edge] Telemetría enviada: Vb: 4.96G | Temp: 68.11°C
[Edge] Telemetría enviada: Vb: 1.31G | Temp: 64.64°C
[Edge] Telemetría enviada: Vb: 2.76G | Temp: 54.95°C
```
7. En GitHub Actions
```
[1. Git Push] ──► [2. GitHub Actions: Build & Push] ──► [3. Docker Hub]
                                                                                     │
                         ┌───────────────────────────────────┴───────────────────────────────────┐
                         ▼                                                                                                                      ▼
      [4a. GitHub Actions: SSH a GCP]                                                                                                                       [4b. Watchtower en tu PC Local]
                         │                                                                                                                      │
                         ▼                                                                                                                      ▼
    [Pull & Restart `factory_cloud_ai`]                                                                                                             [Pull & Restart `factory_fog_processor`]
```

