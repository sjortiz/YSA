# Instalation

There are multiple ways of instaling this application

## Docker:

### Pre-requisist

Docker version 17 or superior.
Get it from here: https://www.docker.com/get-docker

### installation

1. Start the service
Run the default application:

```
# Start the application:
> docker run -p 8080:8080 -d --network FFAAS sjortiz/ysa:stable`
```
or build it yourself:
```
# build the docker image
> docker build -t sjortiz/ysa:latest .
> docker run -p 8080:8080 -d --network FFAAS sjortiz/ysa:latest`
```

1. Start the database
```
# Starts the database:
> docker run -it --name mongo -p 27017:27017 --network FFAAS -d  mongo:latest
```

## Docker-compose
TBD
