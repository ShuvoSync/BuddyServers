FROM alpine:3.22

ARG TARGETARCH

ARG ttyd_binary="https://github.com/ShuvoSync/BuddyServers-ttyd/releases/download/v1.0.0/buddyservers-ttyd-${TARGETARCH}"

COPY BuddyServers-${TARGETARCH} /buddyservers

RUN apk update && apk upgrade && \
    apk add --no-cache wget json-c libcrypto3 libssl3 libuv libwebsockets libwebsockets-evlib_uv tmux musl zlib && \
    echo "set -g status off" > ~/.tmux.conf && \
    chmod +x buddyservers && \
    wget -O /usr/bin/buddyservers-ttyd "$ttyd_binary" && \
    chmod +x /usr/bin/buddyservers-ttyd

# Force update BusyBox to patch CVE-2025-46394 & CVE-2024-58251
RUN set -eux; \
    ver="$(apk info -e busybox || true)"; \
    case "$ver" in *busybox*) true ;; *) exit 1 ;; esac; \
    if apk policy busybox | grep -q '1\.37\.0-r19'; then \
    echo "Installing patched BusyBox build from edge…"; \
    echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories; \
    apk update; \
    apk add --no-cache --upgrade 'busybox>=1.37.0-r20'; \
    sed -i '$ d' /etc/apk/repositories; \
    fi

COPY launcher.sh /usr/local/bin/launcher.sh
RUN chmod +x /usr/local/bin/launcher.sh


# Initialize default values
VOLUME ["/root/.buddyservers"]
EXPOSE 8080 7001 25565

ENV WEB_PORT=8080 \
    WEB_USERNAME=root \
    WEB_PASSWORD=buddyservers

CMD ["/usr/local/bin/launcher.sh"]
