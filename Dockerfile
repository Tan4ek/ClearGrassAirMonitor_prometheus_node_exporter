FROM python:3.13.18-slim-bookworm AS dependencies
COPY requirements.txt .

RUN apt-get update && \
        apt-get install -y --no-install-recommends gcc libc6-dev libffi-dev libssl-dev pkg-config && \
        rm -rf /var/lib/apt/lists/* && \
        pip install --no-cache-dir --user --no-warn-script-location -r requirements.txt

FROM python:3.13.18-slim-bookworm AS build-image
COPY --from=dependencies /root/.local /root/.local

WORKDIR /app

COPY main.py ./main.py
# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5433

ENTRYPOINT ["python", "main.py"]
