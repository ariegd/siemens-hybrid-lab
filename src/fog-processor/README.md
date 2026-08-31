# Capa Fog: Local Processing & OT Action Engine
Procesador analítico local que actúa como intermediario entre la red de campo (OT) y la nube (IT). Recibe telemetría vía MQTT, consulta la API Cloud y ejecuta decisiones críticas (como la parada de línea `STOP_LINE`) localmente.

---

## Componentes de la Capa Fog
La capa Fog se orquesta mediante `src/docker-compose.yml` e incluye tres servicios principales:

1. **`mqtt-broker` (`eclipse-mosquitto`)**: Broker MQTT expuesto en el puerto `1883` para comunicación de campo.
2. **`fog-processor` (`ariegd/fog-processor`)**: Servicio en C/Python que procesa telemetría y evalúa la respuesta de la nube.
3. **`watchtower` (`containrrr/watchtower`)**: Servicio de Despliegue Continuo (CD) que busca imágenes actualizadas en Docker Hub cada 30 segundos y reinicia el procesador sin interrupción manual.

---

## Comandos de Despliegue Local
```bash
# 1. Crear el archivo de orquestación (`docker-compose.yml`)
cd ~/siemens-hybrid-lab
nano docker-compose.yml

# 2. Para compilar tu contenedor y arrancar el entorno Fog en tu portátil, ejecuta:
docker compose up --build -d

# 3. Monitorizar el Gemelo Digital local viendo los logs del procesador en tiempo real con este comando:
docker logs -f factory_fog_processor

# 4. En caso que sea necesario, como modificar `main.py`. Reiniciar el contenedor de tu portátil (Fog)
docker compose up -d --build fog-processor

# 5. Enganchaste a los logs por nombre de servicio
docker compose logs -f fog-processor
```

