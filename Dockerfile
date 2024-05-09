FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

FROM gcr.io/distroless/python3-debian11
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app

CMD python /app/src/main.py $INPUT_FILES