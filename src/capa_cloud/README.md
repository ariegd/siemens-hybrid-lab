# Capa Cloud: AI Inference Engine
Servidor de inferencia para detección de anomalías en vibración y temperatura de componentes industriales. Utiliza un modelo de clasificación desplegado con **Flask** y **Gunicorn** sobre una instancia de **Google Cloud Platform (GCP)**

---

## Aprovisionamiento de Infraestructura en GCP
**Opción 1: Desde la Cloud Shell (La más rápida)** No necesitas instalar nada en tu ordenador local. Ve a la consola web de Google Cloud y haz clic en el botón `Activar Cloud Shell` (es el icono de una terminal >_ ubicado arriba a la derecha, al lado del buscador). Una vez se abra la consola abajo, pega consecutivamente estos dos comandos:

1. Acceder a GCP de las siguientes formas
```bash
# 1. Instala la herramienta en tu sistema:
curl https://google.com | bash
exec -l $SHELL

# 2. Inicia sesión y vincula tu cuenta de GCP:
gcloud auth login

# 3. Selecciona tu proyecto actual:
gcloud config set project api-model-project
```

2.  Crear la regla de firewall para el puerto 8000
```bash
gcloud compute firewall-rules create permitir-api-8000 \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:8000 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=api-server

# sino funciona, entonces
gcloud compute firewall-rules create allow-ai-api-8000 \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:8000 \
    --source-ranges=0.0.0.0/0 \
    --description="Permitir acceso a la API de IA en puerto 8000"
```

3. Crear la Máquina Virtual en Madrid con 4 GB de RAM
(Nota técnica: El parámetro `--tags=api-server` une de forma inteligente la máquina virtual con la regla de firewall que creamos justo antes).
```bash
gcloud compute instances create api-instance-automatizada \
    --zone=europe-southwest1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=api-server
```

4. Acceder por ssh a la VM
```bash
# 1. Listar tus proyectos reales
gcloud projects list

# 2. Seleccionar el ID de proyecto correcto
gcloud config set project TU_PROJECT_ID_REAL

# 3.  Comprobar si la máquina virtual se está ejecutando
gcloud compute instances list

# 4. Conectarte por SSH a tu VM
gcloud compute ssh siemens-cloud-ai --zone=europe-southwest1-a
```

---

## Despliegue con Docker
**Estructura de archivos local**
* `app2.py`: API REST Flask con el modelo de aprendizaje automático.
* `Dockerfile`: Imagen optimizada basada en Python 3.11-slim con Gunicorn. 
* `requirements.txt`: Dependencias (`flask`, `numpy`, `scikit-learn`, `gunicorn`).

**Despliegue manual / ver logs**
```bash
# Construir la imagen
docker build -t ariegd/cloud-ai:latest .

# Ver logs del contenedor en GCP
docker logs -f factory_cloud_ai
```

---

## Crear el código de la IA (`app.py`)
```bash
# 1. vamos a crear el archivo del servidor.
nano app2.py

# 2. Arrancar el Servidor de IA
Para ejecutar el servidor asegurándote de que no se apague si cierras la terminal, utilizaremos `nohup`. 
nohup python3 app2.py > server.log 2>&1 &

# 3. Verificar que está levantado y escuchando correctamente en el puerto 8000
ss -tuln | grep 8000
```

---

## Vamos a crear el entorno e instalar todo
```bash
# 1. Asegurar las herramientas de Python en el sistema
sudo apt update && sudo apt install -y python3-pip python3-venv

# 2. Crear la carpeta del entorno virtual llamada 'venv'
python3 -m venv venv

# 3. Activar el entorno virtual (ahora sí existirá)
source venv/bin/activate

# 4. Instalar las dependencias del modelo
pip install flask numpy scikit-learn
```


