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

# Ver peticiones entrantes a la IA en tiempo real
tail -f server.log
```
salida
```
91.230.168.251 - - [25/Jul/2026 06:09:25] "GET / HTTP/1.1" 404 -
195.184.76.164 - - [25/Jul/2026 06:11:10] "GET /favicon.ico HTTP/1.1" 404 -
65.49.1.162 - - [25/Jul/2026 06:41:45] "GET / HTTP/1.1" 404 -
65.49.1.164 - - [25/Jul/2026 06:43:04] "GET /favicon.ico HTTP/1.1" 404 -
65.49.1.166 - - [25/Jul/2026 06:43:26] "GET http://api.ipify.org/?format=json HTTP/1.1" 404 -
65.49.1.171 - - [25/Jul/2026 06:43:33] "CONNECT www.shadowserver.org:443 HTTP/1.1" 404 -
83.32.39.126 - - [25/Jul/2026 09:32:03] "POST /predict HTTP/1.1" 200 -
83.32.39.126 - - [25/Jul/2026 09:32:05] "POST /predict HTTP/1.1" 200 -
83.32.39.126 - - [25/Jul/2026 09:32:07] "POST /predict HTTP/1.1" 200 -
83.32.39.126 - - [25/Jul/2026 09:32:09] "POST /predict HTTP/1.1" 200 -
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

