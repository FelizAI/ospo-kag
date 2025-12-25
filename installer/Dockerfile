FROM node:24-alpine AS web-build
COPY ui ui
RUN cd ui && ls -la && if [ -d "dist" ]; then exit 0; fi && \
    npm install --prefer-offline --no-audit && \
    npm install -D concurrently && \
    NODE_OPTIONS="--max-old-space-size=4096" npx concurrently "npm run build" "npm run build-chat" && \
    find . -maxdepth 1 ! -name '.' ! -name 'dist' ! -name 'public' -exec rm -rf {} +

FROM ghcr.io/1panel-dev/maxkb-base:python3.11-pg17.6 AS stage-build
COPY --chmod=700 . /opt/maxkb-app
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ gettext libexpat1-dev libffi-dev && \
    apt-get clean all  && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /opt/maxkb-app
ARG MAXKB_SANDBOX_HOME
RUN gcc -shared -fPIC -o ${MAXKB_SANDBOX_HOME}/lib/sandbox.so /opt/maxkb-app/installer/sandbox.c -ldl && \
    rm -rf /opt/maxkb-app/ui && \
    pip install uv --break-system-packages && \
    python -m uv pip install -r pyproject.toml && \
    find /opt/maxkb-app  -depth \( -name ".git*" -o -name ".docker*" -o -name ".idea*" -o -name ".editorconfig*" -o -name ".prettierrc*" -o -name "README.md" -o -name "poetry.lock" -o -name "pyproject.toml"  \) -exec rm -rf {} + && \
    python /opt/maxkb-app/apps/manage.py compilemessages && \
    export PIP_TARGET=/opt/maxkb-app/sandbox/python-packages && \
    python -m uv pip install --target=$PIP_TARGET requests pymysql psycopg2-binary && \
    rm -rf /opt/maxkb-app/installer
COPY --from=web-build --chmod=700 ui /opt/maxkb-app/ui

FROM ghcr.io/1panel-dev/maxkb-base:python3.11-pg17.6
ARG DOCKER_IMAGE_TAG=dev \
    BUILD_AT \
    GITHUB_COMMIT

WORKDIR /opt/maxkb-app
COPY --from=stage-build /opt/maxkb-app /opt/maxkb-app
COPY --from=stage-build /opt/py3 /opt/py3
RUN mkdir -p /opt/maxkb-app/tmp

EXPOSE 8080
VOLUME /opt/maxkb
ENTRYPOINT ["bash", "-c"]
CMD [ "/usr/bin/start-all.sh" ]