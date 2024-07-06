#!/bin/bash

# Se inicia docker y se crea la base de datos 'renaper'
echo "Creando sesion docker con el puerto 5432 y data en src/backend/data para crear la base de datos"
NOMBRE_CONTENEDOR='renaper'

docker run --rm -d --name $NOMBRE_CONTENEDOR -e POSTGRES_PASSWORD=123 -p 5432:5432 -v $(pwd)/src/backend/data:/var/lib/postgresql/data postgres:16
# Espera 5 segundos, para darle tiempo a docker a que inicialice todo lo necesario
sleep 5

# Se inicia una sesion de PSQL
docker exec -it $NOMBRE_CONTENEDOR bash -c "psql -c 'create database renaper'"
docker stop $NOMBRE_CONTENEDOR

