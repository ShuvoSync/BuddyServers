# BuddyServers Docker Image - Quick Reference

**Maintained by**: [Kaleb Efflandt](https://github.com/macarooni-man)

**Supported tags and architectures**:

- Tags: `latest`, `beta`, any release version
- Architectures: `amd64`, `arm64`

**Image source**:

- Docker Hub: [macarooniman/buddyservers](https://hub.docker.com/r/macarooniman/buddyservers/tags)

<br><br>

# How to Use This Image

Although optional, our Docker image (and headless mode) is meant as a minimal feature case to host our custom remote management solution, Telepath, and connect from another device using the GUI. You can learn more about the Telepath API [on our website](https://buddyservers.com/guides/telepath).

Otherwise, by using this image as a standalone server, you'll still be able to create any server, tunnel through our playit.gg integration, or edit the "server.properties" file. A Telepath connection is required to add worlds, mods/plug-ins, utilize the custom scripting language, and a lot more useful and advanced functionality.

<br><br>

## Command Reference

BuddyServers headless uses commands to interact with it. Once opened, it will bring you to a prompt. Pressing `?` at any time will show help for the current command, or sub-command. To set up a basic Paper server, enter the following commands:

`server create paper:latest My Server`

`server launch My Server`

You can press `ESC` to detach from the console and create or launch other servers. To view BuddyServers commands for Minecraft, type `!help` in the console.

To go back to a server console, you can use the `console` command.

You can also launch BuddyServers with the `--launch` or `-l` flag to start a server automatically:

`BuddyServers --launch "My Server, Server 2"`

<br><br>

## Running the Container

### Basic Usage

To run BuddyServers with default settings:

```bash
env WEB_PORT=8080 WEB_USERNAME='root' WEB_PASSWORD='buddyservers' \
sh -c 'docker run -d --name buddyservers \
  -e WEB_PORT -e WEB_USERNAME -e WEB_PASSWORD \
  -p "$WEB_PORT:$WEB_PORT" -p 7001:7001 -p 25565:25565 \
  -v buddyservers-data:/root/.buddyservers \
  --restart unless-stopped \
  macarooniman/buddyservers:latest'
```

This command:

- Runs BuddyServers in a container
- Exposes key ports:
  - `8080` for the TTYD terminal (web interface)
  - `7001` for the Telepath API
  - `25565` for the default port of a Minecraft server
- Stores data in a Docker volume named `buddyservers-data`
- Secures the TTYD instance using the following credentials:
  - **Username**: `root`
  - **Password**: `buddyservers`

- ⚠️ In order to use this image, you'll have to change the default credentials. To do so, simply modify the `WEB_USERNAME` and `WEB_PASSWORD` parameters with the desired credentials.
  - Example: `WEB_USERNAME='U$ern4me' WEB_PASSWORD='P@s$w0rd'`

Note that binary of both BuddyServers and ttyd are pre-compiled for optimal compatibility. If you'd like to build these from source, please reference the guide below.

<br>

### Using Docker Compose

To manage BuddyServers with Docker Compose, create a `docker-compose.yml`:

```yaml
version: "3"
services:
  app:
    image: macarooniman/buddyservers:latest
    container_name: buddyservers
    stdin_open: true
    tty: true
    restart: unless-stopped

    environment:

      # Default web interface port
      WEB_PORT: "8080"

      # Change the web interface credentials
      WEB_USERNAME: "root"
      WEB_PASSWORD: "buddyservers"

    ports:

      # Web interface (make this the same as WEB_PORT)
      - "8080:8080"

      # Telepath API (buddyservers)
      - "7001:7001"

      # Add more ports based on the servers you create
      - "25565:25565"

    volumes:
      - buddyservers-data:/root/.buddyservers

volumes:
  buddyservers-data:
```

To run BuddyServers using Docker Compose, in the same directory run:

```bash
docker-compose up -d
```

<br><br>

## Accessing the TTYD Web Interface

After running the container, open your browser and navigate to `http://localhost:8080` for access to the TTYD web-based terminal. The default credentials are:

- **Username**: `root`
- **Password**: `buddyservers`

- ⚠️ In order to use this image, you'll have to change the default credentials. To do so, simply modify the `WEB_USERNAME` and `WEB_PASSWORD` parameters with the desired credentials.
  - Example: `WEB_USERNAME: 'U$ern4me' WEB_PASSWORD: 'P@s$w0rd'`

<br><br>

## Data Persistence

To ensure your BuddyServers data persists across container restarts, mount a volume:

```bash
docker run -d \
  --name buddyservers \
  -v buddyservers-data:/root/.buddyservers \
  macarooniman/buddyservers:latest
```

In Docker Compose, the volume is defined as:

```yaml
volumes:
  buddyservers-data:
```

This volume will store all configuration files, server data, and back-ups.

<br><br>

# Building the Image Locally

Pre-requisites:

- [Clone BuddyServers repo](https://github.com/macarooni-man/BuddyServers)
- [Clone BuddyServers-ttyd repo](https://github.com/macarooni-man/BuddyServers-ttyd)
- [Alpine Linux 3.21](https://dl-cdn.alpinelinux.org/alpine/v3.21/releases/)

After cloning the repositories on Alpine, move to the root of the `BuddyServers` repository and run the following script to build BuddyServers:

```bash
# Install dependencies
apk add python3 py3-pip gcc pangomm-dev pkgconfig python3-dev zlib-dev libffi-dev musl-dev linux-headers mtdev-dev mtdev

# Build BuddyServers
cd build-tools
chmod +x build-docker.sh
./build-docker.sh
```

After building BuddyServers, move to the root of the `BuddyServers-ttyd` repository and run the following script to build buddyservers-ttyd:

```bash
# Install dependencies
apk add build-base libwebsockets-evlib_uv bsd-compat-headers cmake json-c-dev libuv-dev libwebsockets-dev openssl-dev>3 samurai zlib-dev

# Build buddyservers-ttyd
mkdir build && cd build
cmake ..
make && make install
mv -f ./ttyd ../../BuddyServers/docker
```

After building these binaries, move to `BuddyServers/docker` and build the Docker image locally with:

```bash
docker build -t yourusername/buddyservers:latest .
```

If you need to build for different architectures, such as `amd64` or `arm64`, you can use Docker Buildx:

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t yourusername/buddyservers:latest --push .
```

<br><br>

## Dockerfile Overview

[View the Dockerfile used for this image on our GitHub](https://github.com/macarooni-man/BuddyServers/blob/main/docker/Dockerfile)