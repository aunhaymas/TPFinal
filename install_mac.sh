#!/bin/bash

# Usar este script solamente cuando es la primera vez levantando la pagina.
# Este script instala docker, crea la base de datos en docker y luego se inicia la pagina. También instala los requerimientos del proyecto

# Crea el entorno virtual donde se instalará los requerimientos
python3 -m venv venv

# Instala los requerimientos de python
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Instala lo necesario para poder utilizar docker. INSTALAR DOCKER DESKTOP
#bash ./scripts/install_docker_mac.sh

# Crea la base de datos utilizando un contenedor de docker
bash ./scripts/create_db.sh

# Inicia la pagina
bash ./start_mac.sh

