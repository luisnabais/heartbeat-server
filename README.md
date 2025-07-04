# heartbeat-server

This code can be seen on any of these repositories:
[GitLab](https://gitlab.com/luisnabais/heartbeat-server)
[GitHub](https://github.com/luisnabais/heartbeat-server)
[Codeberg](https://codeberg.org/luisnabais/heartbeat-server)

## Description
Flask script running inside a docker container, which exposes a heartbeat endpoint (to be used by my [heartbeat-client](https://gitlab.com/luisnabais/heartbeat-client) project) to see if those servers are alive. It allows multiple servers to be connected.
Script can also be executed locally or any other way, as long as dependencies are met.

## Instructions
### Run container
1. Set variable values (NTFY_TOPIC, NTFY_TOKEN and HEARTBEAT_TIMEOUT ) in .env file or docker-compose.yml
2. Execute the command: `docker-compose up -d`

### Build container
If you don't want/need to use the pre-built container and/or want/need to build the container by yourself, execute the command:
`docker build -t heartbeat-server:latest .` (my advice is to not use latest, but a version system of your own)