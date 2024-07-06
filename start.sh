#!/bin/bash

# Este script se puede utilizar siempre luego de haber utilizado 'install.sh'
# Levanta docker con la base de datos 'renaper' en otra terminal y espera 6 segundos 
gnome-terminal -- bash ./scripts/docker.sh
sleep 6

# Levanta el servidor de front-end en localhost:8000

gnome-terminal --working-directory ./src/frontend -- python3 -m http.server

# Levanta el virtualenv

source venv/bin/activate

# Levanta el servidor de back-end en localhost:5000

python3 ./src/backend/main.py
