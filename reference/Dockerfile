# Build from the repository root using the company wheel/runtime pattern.
FROM docker.io/rockylinux/rockylinux:10.2-minimal AS builder

# Refresh the OS trust store before downloading build tools or runtimes.
RUN microdnf update -y && microdnf install -y ca-certificates && \
    update-ca-trust && microdnf clean all
# Explicitly distrust the root withdrawn in certifi 2026.10.19.
COPY reference/emsign-ecc-root-g3.pem /etc/pki/ca-trust/source/blocklist/emsign-ecc-root-g3.pem
RUN update-ca-trust

# Seed Hatch virtual environments from a verified patched pip wheel.
ADD --checksum=sha256:fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70 https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl /opt/python-bootstrap/pip-26.2.2-py3-none-any.whl
ENV VIRTUALENV_PIP=26.2.2 \
    VIRTUALENV_EXTRA_SEARCH_DIR=/opt/python-bootstrap \
    VIRTUALENV_DOWNLOAD=false \
    UV_SYSTEM_CERTS=true \
    SSL_CERT_FILE=/etc/pki/tls/certs/ca-bundle.crt \
    REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt

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
    python3 -m pip install --no-cache-dir --upgrade "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70" && \
    python3 -m pip install --no-cache-dir --upgrade "certifi>=2026.10.19" && \
    python3 -m pip wheel --wheel-dir /wheels dist/*.whl

FROM docker.io/rockylinux/rockylinux:10.2-minimal AS runtime

# Refresh the OS trust store before downloading build tools or runtimes.
RUN microdnf update -y && microdnf install -y ca-certificates && \
    update-ca-trust && microdnf clean all
# Explicitly distrust the root withdrawn in certifi 2026.10.19.
COPY reference/emsign-ecc-root-g3.pem /etc/pki/ca-trust/source/blocklist/emsign-ecc-root-g3.pem
RUN update-ca-trust

# Seed Hatch virtual environments from a verified patched pip wheel.
ADD --checksum=sha256:fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70 https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl /opt/python-bootstrap/pip-26.2.2-py3-none-any.whl
ENV VIRTUALENV_PIP=26.2.2 \
    VIRTUALENV_EXTRA_SEARCH_DIR=/opt/python-bootstrap \
    VIRTUALENV_DOWNLOAD=false \
    UV_SYSTEM_CERTS=true \
    SSL_CERT_FILE=/etc/pki/tls/certs/ca-bundle.crt \
    REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt

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
    python -m pip install --no-cache-dir --upgrade "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70" && \
    python -m pip install --no-cache-dir --upgrade "certifi>=2026.10.19" && \
    python -m pip install --no-cache-dir --upgrade pip
COPY --from=builder --chown=2000:2000 /wheels/ /app/dist/
RUN python -m pip install --no-cache-dir --no-index --no-deps /app/dist/*.whl && \
    python -m pip check && \
    waterbodies --help && \
    python -m pip uninstall --yes pip && \
    rm -rf /app/dist
CMD ["waterbodies", "--help"]
