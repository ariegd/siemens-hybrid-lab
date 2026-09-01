# Capa Cloud: AI Inference Engine

Servidor de inferencia para detección de anomalías en vibración y temperatura de componentes industriales. Utiliza un modelo de clasificación (`scikit-learn`) desplegado con **Flask** y **Gunicorn** dentro de un contenedor Docker en una instancia de **Google Cloud Platform (GCP)**.

---

## Tabla de Contenidos
- [1. Aprovisionamiento de Infraestructura en GCP](#1-aprovisionamiento-de-infraestructura-en-gcp)
- [2. Transferencia de Código (Local -> GCP VM)](#2-transferencia-de-código-local---gcp-vm)
- [3. Preparación del Entorno Docker en la VM](#3-preparación-del-entorno-docker-en-la-vm)
- [4. Estructura de Archivos en ~/cloud-api](#4-estructura-de-archivos-en-cloud-api)
- [5. Despliegue y Operación de la API Cloud](#5-despliegue-y-operación-de-la-api-cloud)
- [6. Sincronización con la Capa Fog (Local)](#6-sincronización-con-la-capa-fog-local)

---

## 1. Aprovisionamiento de Infraestructura en GCP

### Configuración inicial (gcloud CLI / Cloud Shell)
```bash
# 1. Iniciar sesión y seleccionar el proyecto
gcloud auth login
gcloud config set project TU_PROJECT_ID_REAL

# 2. Crear regla de firewall para abrir el puerto 8000
gcloud compute firewall-rules create allow-ai-api-8000 \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:8000 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=api-server \
    --description="Permitir acceso a la API de IA en puerto 8000"

# 3. Crear la Máquina Virtual en Madrid (europe-southwest1-a)
gcloud compute instances create siemens-cloud-ai \
    --zone=europe-southwest1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=api-server
```

---

## 2. Transferencia de Código (Local -> GCP VM)
Desde la raíz de tu proyecto en la máquina local (`zodd@nootbster`), transfiere la carpeta del módulo cloud a la VM:

```bash
gcloud compute scp --recurse src/capa_cloud zodd@siemens-cloud-ai:~/cloud-api --zone=europe-southwest1-a
```

---

## 3. Preparación del Entorno Docker en la VM   
Conéctate vía SSH a la instancia de GCP:

```bash
gcloud compute ssh zodd@siemens-cloud-ai --zone=europe-southwest1-a
```

Una vez dentro de la VM, instala Docker y configura los permisos del usuario:

```bash
# Instalación de paquetes de Docker y Compose
sudo apt update && sudo apt install -y docker.io docker-compose

# Configurar permisos de usuario sin sudo
sudo usermod -aG docker $USER
newgrp docker

# (Opcional) Habilitar compatibilidad con el comando moderno 'docker compose'
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo ln -s $(which docker-compose) /usr/local/lib/docker/cli-plugins/docker-compose
```

---

## 4. Estructura de Archivos en `~/cloud-api`
Asegúrate de que el directorio del proyecto en la VM (`~/cloud-api`) contenga los siguientes archivos:

* `app2.py`: API REST Flask y modelo de regresión logística.
* `requirements.txt`: Dependencias (flask, numpy, scikit-learn, gunicorn).
* `Dockerfile`: Receta de empaquetado multicapa en python:3.11-slim.
* `docker-compose.yml`: Orquestador del servicio de inferencia.

Contenido de `docker-compose.yml`

```yaml
services:
  cloud-ai-api:
    image: ariegd/cloud-ai:latest
    build: .
    container_name: factory_cloud_ai
    ports:
      - "8000:8000"
    restart: always
```

---

## 5. Despliegue y Operación de la API Cloud
Compilar y levantar el servicio

```bash
cd ~/cloud-api

# Compilar la imagen y levantar en segundo plano
docker-compose up -d --build
```

Comandos de verificación y monitoreo

```bash
# Ver estado del contenedor
docker-compose ps

# Monitorear logs de Gunicorn en tiempo real
docker logs -f factory_cloud_ai

# Probar la inferencia localmente vía cURL
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"vibration": 5.2, "temperature": 85.0}'
```

---

## 6. Sincronización con la Capa Fog (Local)
Para conectar tu nodo Fog local con la VM en GCP, actualiza la dirección IP pública externa de GCP en el archivo `src/docker-compose.yml` de tu máquina local:

```yaml
fog-processor:
    image: ariegd/fog-processor:latest
    environment:
      - MQTT_HOST=mqtt-broker
      - CLOUD_API_URL=http://<IP_EXTERNA_GCP>:8000/predict
```
