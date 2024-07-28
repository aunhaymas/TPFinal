#!/bin/bash

#lsof -i:5000 
   # Verificar si el entorno virtual existe
if [ ! -f venv/bin/activate ]; then
  echo "No existe venv/"
  python3 -m venv venv
fi
trap cerrar EXIT 

function cerrar() {
  echo "Cerrando flask server"
  pkill -f "flask run --debug"
  pkill -f "python3 main.py"

  echo "Cerrando python3 server"
  pkill -f "python3 -m http.server"
  gnome-terminal --tab -- bash -c "git restore data/; exec bash"
}


echo "Activando el entorno virtual..."
if [[ -n "$VIRTUAL_ENV" ]]; then #Por seguridad
  source venv/bin/activate
  pip install -r requirements.txt
fi

echo "Iniciando el servidor backend Flask..."
cd backend/ && flask run --debug &

# Abro una nueva pestaña en la terminal
echo "Iniciando el servidor frontend..."
gnome-terminal --tab -- bash -c "cd frontend/ && python3 -m http.server; exec bash"

gnome-terminal --tab -- bash -c "code ."
wait
