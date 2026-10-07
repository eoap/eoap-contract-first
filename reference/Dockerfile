# Build from the repository root using the company wheel/runtime pattern.
FROM docker.io/rockylinux/rockylinux:10.2-minimal AS builder

RUN microdnf -y update && \
    microdnf -y install curl tar python3 python3-pip python3-setuptools gcc git && \
    microdnf clean all
RUN curl --fail --location https://github.com/pypa/hatch/releases/download/hatch-v1.14.0/hatch-x86_64-unknown-linux-gnu.tar.gz \
      -o /tmp/hatch.tar.gz && \
    tar -xzf /tmp/hatch.tar.gz -C /tmp && \
    install -m 0755 /tmp/hatch /usr/local/bin/hatch && \
    rm -f /tmp/hatch /tmp/hatch.tar.gz

WORKDIR /src/tool
COPY reference/pyproject.toml reference/README.md reference/LICENSE ./
COPY reference/src/ ./src/
RUN hatch build -t wheel && \
    python3 -m pip wheel --wheel-dir /wheels dist/*.whl

FROM docker.io/rockylinux/rockylinux:10.2-minimal AS runtime

ARG VERSION=1.0.0
LABEL org.opencontainers.image.version=$VERSION \
      org.opencontainers.image.source="https://github.com/eoap/waterbodies-learning" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.title="waterbodies-application"
RUN microdnf -y update && \
    microdnf -y install python3 python3-pip shadow-utils && \
    microdnf clean all
ENV HOME=/home/neo
RUN /usr/sbin/groupadd -g 2000 neo && \
    /usr/sbin/useradd -u 2000 -g 2000 -m -d /home/neo -s /sbin/nologin neo && \
    mkdir -p /app && \
    chown -R 2000:2000 /app /home/neo
USER neo
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:${PATH}"
RUN python3 -m venv /app/venv && \
    python -m pip install --no-cache-dir --upgrade pip
COPY --from=builder --chown=2000:2000 /wheels/ /app/dist/
RUN python -m pip install --no-cache-dir --no-index --no-deps /app/dist/*.whl && \
    python -m pip check && \
    waterbodies --help && \
    python -m pip uninstall --yes pip && \
    rm -rf /app/dist
CMD ["waterbodies", "--help"]
