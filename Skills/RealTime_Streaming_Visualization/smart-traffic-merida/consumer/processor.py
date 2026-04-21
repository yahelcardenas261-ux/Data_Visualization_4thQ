import json, os, time
from datetime import datetime, timezone
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

KAFKA_BROKER  = os.getenv("KAFKA_BROKER",  "kafka:9092")
TOPIC         = os.getenv("KAFKA_TOPIC",   "your-events")
INFLUX_URL    = os.getenv("INFLUX_URL",    "http://influxdb:8086")
INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN",  "")
INFLUX_ORG    = os.getenv("INFLUX_ORG",    "")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "")

def validate(event: dict) -> bool:
    """Return False to discard the event."""
    required = ["sensor_id", "timestamp", "vehicle_count"]
    return all(k in event for k in required)

def transform(event: dict) -> dict:
    """
    Clean and enrich the event.
    Add computed fields, classify levels, etc.
    """
    # Usamos vehicle_count para determinar el nivel
    count = event.get("vehicle_count", 0)
    if count < 30:
        event["traffic_level"] = "low"
    elif count < 80:
        event["traffic_level"] = "moderate"
    else:
        event["traffic_level"] = "heavy"
    return event

def to_influx_point(event: dict) -> Point:
    return (
        Point("traffic_measurement") # Nombre de la tabla
        .tag("sensor_id",   event["sensor_id"])
        .tag("location",    event.get("location", "Mérida")) # Añadimos la ubicación
        .tag("level",       event.get("traffic_level", "low"))
        .field("vehicles",  int(event["vehicle_count"]))
        .field("speed",     float(event["avg_speed"]))
        .field("emergency", 1 if event.get("emergency_active") else 0)
        .time(event["timestamp"]) # Usa el tiempo del evento, no el actual
    )

def connect_kafka():
    while True:
        try:
            c = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                value_deserializer=lambda m: json.loads(m.decode()),
                group_id="processor-group",
                auto_offset_reset="latest",
            )
            print(f"[CONSUMER] Connected to Kafka")
            return c
        except NoBrokersAvailable:
            print("[CONSUMER] Waiting for Kafka…")
            time.sleep(5)

def connect_influx():
    while True:
        try:
            client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
            client.ping()
            print(f"[CONSUMER] Connected to InfluxDB")
            return client.write_api(write_options=SYNCHRONOUS)
        except Exception as e:
            print(f"[CONSUMER] Waiting for InfluxDB… ({e})")
            time.sleep(5)

def main():
    consumer  = connect_kafka()
    write_api = connect_influx()
    count = 0
    for msg in consumer:
        event = msg.value
        if not validate(event):
            continue
        event = transform(event)
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=to_influx_point(event))
        count += 1
        print(f"  [{count}] {event['sensor_id']} → level: {event.get('traffic_level')}")

if __name__ == "__main__":
    main()