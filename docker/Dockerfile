FROM golang:1.21-alpine

WORKDIR /app
COPY . .

RUN go build -o sentinel-ingestion

EXPOSE 8080

CMD ["./sentinel-ingestion"]


FROM gcc:latest

WORKDIR /app
COPY . .

RUN g++ drift_engine.cpp -o drift_engine

CMD ["./drift_engine"]
