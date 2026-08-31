# Siemens Hybrid Lab: Edge-Fog-Cloud Architecture

![Pipeline Status](https://img.shields.io/github/actions/workflow/status/ariegd/siemens-hybrid-lab/main.yml?branch=master&label=CI%2FCD%20Pipeline&logo=githubactions&logoColor=white)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Docker Image Version](https://img.shields.io/docker/v/ariegd/fog-processor?label=Fog%20Processor&logo=docker&logoColor=white)
![Docker Image Version](https://img.shields.io/docker/v/ariegd/cloud-ai?label=Cloud%20AI&logo=docker&logoColor=white)

**Infraestructura & Cloud:**  
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-GCP_VM-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-Orchestration-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)

**DevOps & Continuous Delivery:**  
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD_Pipeline-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Docker Hub](https://img.shields.io/badge/Docker_Hub-Registry-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/)
[![Watchtower](https://img.shields.io/badge/Watchtower-Auto_CD-1890FF)](https://containrrr.dev/watchtower/)

**Backend & Inferencia IA:**  
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API_Server-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-AI_Inference-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

**OT & Protocolos de Campo:**  
[![MQTT](https://img.shields.io/badge/MQTT-Mosquitto_Broker-660066?logo=eclipse-mosquitto&logoColor=white)](https://mosquitto.org/)
[![ESP32-C6](https://img.shields.io/badge/Espressif-ESP32--C6-E7352C?logo=espressif&logoColor=white)](https://www.espressif.com/)

Réplica exacta de la jerarquía industrial Edge-Fog-Cloud del ecosistema Siemens-NVIDIA utilizando herramientas de código abierto. El sistema simula el monitoreo predictivo de un brazo robótico en planta, procesa anomalías en la capa Fog y consulta un modelo de IA hospedado en la nube para ejecutar paradas de emergencia en tiempo real.

---

## Tabla de Contenidos
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Flujo CI/CD y Despliegue Continuo](#flujo-cicd-y-despliegue-continuo)
- [Puesta en Marcha (Entorno Híbrido Completo)](#puesta-en-marcha-entorno-híbrido-completo)
  - [Terminal 1: Capa Cloud (VM en Google Cloud)](#terminal-1-capa-cloud-vm-en-google-cloud)
  - [Terminal 2: Capa Fog (Procesador Industrial Local)](#terminal-2-capa-fog-procesador-industrial-local)
  - [Terminal 3: Capa Edge (Simulador de Telemetría OT)](#terminal-3-capa-edge-simulador-de-telemetría-ot)

---

## Arquitectura del Sistema
```text
[ Capa Edge ] ──(MQTT)──► [ Capa Fog ] ──(HTTP)──► [ Capa Cloud ]
 Simulador OT     Broker + Processor       IA Inferencia
 (Robotic Arm)     (Watchtower CD)      (GCP VM / Gunicorn)
```
---

## Estructura del Repositorio
* `src/capa_cloud/`: Servidor de inferencia de IA en Google Cloud Platform (Flask + Gunicorn) [README](https://github.com/ariegd/siemens-hybrid-lab/tree/master/src/capa_cloud). 
* `src/fog-processor/`: Procesador analítico local y orquestación con Mosquitto y Watchtower [README](https://github.com/ariegd/siemens-hybrid-lab/tree/master/src/fog-processor). 
* `src/capa_edge/`: Telemetría de campo (Simulador en Python y firmware ESP32-C6) [README](https://github.com/ariegd/siemens-hybrid-lab/tree/master/src/capa_edge). 

---

## Flujo CI/CD y Despliegue Continuo
El proyecto integra un pipeline automatizado con GitHub Actions, Docker Hub y Watchtower

```Plaintext
[1. Git Push] ──► [2. GitHub Actions: Build & Push] ──► [3. Docker Hub]
                                                                          │
                                         ┌───────────────────┴────────────────────┐
                                        ▼                                        ▼
                          [4a. GitHub Actions: SSH a GCP]         [4b. Watchtower en PC Local]
                                     │                                           │
                                     ▼                                          ▼
                         [Pull & Restart `factory_cloud_ai`]  [Pull & Restart `factory_fog_processor`]
```

---

## Puesta en Marcha (Entorno Híbrido Completo)
Para ejecutar y monitorizar la arquitectura distribuida, trabaja con 3 terminales abiertas en paralelo:

**Terminal 1: Capa Cloud (VM en Google Cloud)**
```Bash
# Acceso vía SSH a la VM en GCP
gcloud compute ssh siemens-cloud-ai --zone=europe-southwest1-a

# Levantar o actualizar el contenedor de la API
cd ~/cloud-api
docker compose pull && docker compose up -d

# Monitorizar inferencias en tiempo real
docker logs -f factory_cloud_ai
```

**Terminal 2: Capa Fog (Procesador Industrial Local)**
```Bash
cd src/
docker compose pull && docker compose up -d

# Ver el procesamiento MQTT -> Cloud AI en tiempo real
docker logs -f factory_fog_processor

# Monitorizar actualizaciones automáticas de Watchtower
docker logs -f factory_watchtower
```

**Terminal 3: Capa Edge (Simulador de Telemetría OT)**
```Bash
cd src/capa_edge
python3 simulador_edge.py
```
