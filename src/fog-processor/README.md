# Desplegar el entorno local
1. Crear el archivo de orquestación (`docker-compose.yml`)
```
cd ~/siemens-hybrid-lab
nano docker-compose.yml
```
2. Para compilar tu contenedor y arrancar el entorno Fog en tu portátil, ejecuta:
```
docker compose up --build -d
```
3. Monitorizar el Gemelo Digital local viendo los logs del procesador en tiempo real con este comando:
```
docker logs -f factory_fog_processor
```
4. En caso que sea necesario, como modificar `main.py`. Reiniciar el contenedor de tu portátil (Fog)
```
docker compose up -d --build fog-processor
```
5. Enganchaste a los logs por nombre de servicio
```
docker compose logs -f fog-processor
```
