import json
import time
import random
import os
from datetime import datetime, timezone
from kafka import KafkaProducer

# Configuración
TOPIC = os.getenv("KAFKA_TOPIC", "merida-traffic-sensors")
BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

# Puntos de control en Mérida
SENSORS = [
    {"id": "SENSOR_MONTEJO", "loc": "Paseo de Montejo"},
    {"id": "SENSOR_PERIFERICO_N", "loc": "Periférico Norte"},
    {"id": "SENSOR_CENTRO_60", "loc": "Calle 60 Centro"},
    {"id": "SENSOR_UPY", "loc": "Entrada UPY"}
]

def get_traffic_data():
    sensor = random.choice(SENSORS)
    # Simulamos que hay más tráfico si es "hora pico" (hora actual)
    is_rush_hour = 7 <= datetime.now().hour <= 9 or 17 <= datetime.now().hour <= 20
    
    return {
        "sensor_id": sensor["id"],
        "location": sensor["loc"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "vehicle_count": random.randint(10, 150) if is_rush_hour else random.randint(0, 50),
        "avg_speed": round(random.uniform(10.0, 90.0), 2),
        "emergency_active": random.random() < 0.05  # 5% de probabilidad de ambulancia
    }

def run():
    producer = None
    # Intento de conexión
    while not producer:
        try:
            producer = KafkaProducer(
                bootstrap_servers=BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except:
            print("Esperando a Kafka...")
            time.sleep(2)

    print(f"🚀 Productor de Mérida iniciado enviando a {TOPIC}...")
    
    while True:
        data = get_traffic_data()
        producer.send(TOPIC, data)
        print(f"  → {data['sensor_id']} | Vehículos: {data['vehicle_count']} | Ubicación: {data['location']}")
        time.sleep(2)

if __name__ == "__main__":
    run()