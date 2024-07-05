#!/bin/bash

# Instalacion de Docker. https://docs.docker.com/engine/install/ubuntu/
apt-get update
apt-get install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


#Si pasa algun error porque la base de datos no esta inicializada, ejecutar python3 main.py en la carpeta backend
echo "Creando sesion docker con el puerto 5432 y data en src/backend/data"
NOMBRE_CONTENEDOR='renaper' # Para identificar internamente al contenedor
systemctl stop postgresql # Docker no cierra automaticamente el servidor de backend
docker stop $NOMBRE_CONTENEDOR # Si no encuentra el contenedor sale una advertencia. ignorar
docker rm $NOMBRE_CONTENEDOR # si no encuentra el contenedor sale una advertencia. ignorar
ABRIR_POSTGRESQL="psql -U postgres"
LISTAR_PERSONAS="SELECT * FROM personas;" #la \\ indica que son comandos internos del programa anterior


docker run --rm -d --name $NOMBRE_CONTENEDOR -e POSTGRES_PASSWORD=123 -p 5432:5432 -v $(pwd)/src/backend/data:/var/lib/postgresql/data postgres:16
sleep 5 # Espera 5 segundos, para darle tiempo a docker a que inicialice todo lo necesario

echo "-----------------------------------------------------------------"
echo "Se ha iniciado correctamente una imagen de Docker con PostgreSQL."
echo "-----------------------------------------------------------------"

docker exec -it $NOMBRE_CONTENEDOR bash -c "$ABRIR_POSTGRESQL -d renaper" # Para mantener psql abierto
docker stop  renaper

