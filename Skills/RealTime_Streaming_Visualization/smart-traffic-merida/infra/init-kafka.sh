#!/bin/bash

# Esperar a que Kafka esté listo para recibir comandos
echo "Esperando a que Kafka esté disponible..."
# Intentar conectarse al broker hasta que responda
until kafka-topics --bootstrap-server kafka:9092 --list > /dev/null 2>&1; do
  echo "Kafka aún no está listo - esperando..."
  sleep 2
done

# Crear el tópico de tráfico si no existe
echo "Creando tópico: merida-traffic-sensors"
kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic merida-traffic-sensors --partitions 1 --replication-factor 1

echo "Infraestructura de Kafka lista."