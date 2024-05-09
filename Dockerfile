FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

FROM gcr.io/distroless/python3-debian11
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
ENV INPUT_FILES=""

CMD /app/src/main.py