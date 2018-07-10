## Docker

#### Pre-requisist

Docker version 17 or superior.
Get it from here: https://www.docker.com/get-docker

#### installation

1. Start the service
Run the default application:

```
# Start the application:
docker run -p 8080:8080 -d --network FFAAS sjortiz/ysa:stable`
```
or build it yourself:
```
# build the docker image
docker build -t sjortiz/ysa:latest .
docker run -p 8080:8080 -d --network FFAAS sjortiz/ysa:latest`
```

2. Start the database:
```
# Starts the database:
docker run -it --name mongo -p 27017:27017 --network FFAAS -d  mongo:latest
```

## Docker-compose

#### Pre-requisist

docker-compose version 1.21 or superior
Get it from here: https://docs.docker.com/compose/install/

#### Instalation

1. start the services:

```
# This spins up all that you need to run the application locally
docker-compose up -d
```
