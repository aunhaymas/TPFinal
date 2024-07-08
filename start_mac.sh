#!/bin/bash

# Este script se puede utilizar siempre luego de haber utilizado 'install.sh'
# Levanta docker con la base de datos 'renaper' en otra terminal y espera 6 segundos 
open -a Terminal.app -e "bash ./scripts/docker.sh"
sleep 6

# Levanta el servidor de front-end en localhost:8000

open -a Terminal.app -e "bash ./scripts/frontend_server.sh"

# Levanta el virtualenv

source venv/bin/activate

# Levanta el servidor de back-end en localhost:5000

python3 ./src/backend/main.py
