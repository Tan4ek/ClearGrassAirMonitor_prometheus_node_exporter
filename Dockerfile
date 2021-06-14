FROM python:3.8-alpine AS dependencies
COPY requirements.txt .

RUN apk add --no-cache \
        gcc musl-dev python3-dev libffi-dev openssl-dev cargo && \
        pip install --no-cache-dir --user --no-warn-script-location -r requirements.txt

FROM python:3.8-alpine AS build-image
COPY --from=dependencies /root/.local /root/.local

WORKDIR /app

COPY main.py ./main.py
# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5433

ENTRYPOINT ["python", "main.py"]