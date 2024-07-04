#!/bin/bash
sudo systemctl stop postgresql
sudo docker run --rm -it -e POSTGRES_PASSWORD=123 -p 5432:5432 -v $(pwd)/src/backend/data:/var/lib/postgresql/data postgres:16
