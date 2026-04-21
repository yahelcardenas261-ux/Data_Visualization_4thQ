# 🚦 Smart Traffic Mérida: Sistema de Monitoreo en Tiempo Real

Este proyecto implementa una arquitectura de datos moderna para el monitoreo de tráfico vehicular en puntos estratégicos de Mérida, Yucatán. Utiliza un stack tecnológico basado en microservicios para capturar, procesar y visualizar métricas de movilidad urbana en tiempo real.

## 🏗️ Arquitectura del Sistema

El sistema se compone de los siguientes módulos:

* **Producer (Simulador):** Genera datos sintéticos basados en el flujo vehicular real de zonas como Paseo de Montejo y Periférico Norte.
* **Apache Kafka:** Actúa como el backbone de mensajería para el transporte de eventos.
* **Consumer (ETL):** Procesa los streams de datos, valida la integridad y calcula niveles de congestión.
* **InfluxDB:** Base de datos de series de tiempo para almacenamiento eficiente de métricas.
* **Dashboard (Plotly Dash):** Interfaz visual interactiva con actualización automática y filtros por sensor.

## 🚀 Instalación y Ejecución

### Requisitos previos
* Docker y Docker Compose
* Fedora 43 / Linux (Compatible con SELinux mediante flags `:z`)

### Pasos para iniciar
1.  **Configurar variables de entorno:**
    Copia el archivo de ejemplo y ajusta según sea necesario:
    ```bash
    cp .env.example .env
    ```

2.  **Desplegar contenedores:**
    Desde la raíz del proyecto, ejecuta:
    ```bash
    docker compose up --build
    ```

3.  **Acceso al Dashboard:**
    Una vez que los servicios estén activos, abre en tu navegador:
    [http://localhost:8050](http://localhost:8050)

## 📊 Visualizaciones Incluidas
* **Monitor de Carga:** Gráfico de barras con clasificación de tráfico (Bajo, Moderado, Pesado).
* **Densidad Geográfica:** Mapa de dispersión por puntos de control.
* **Análisis Histórico:** Gráfico de líneas interactivo con selección de sensor mediante Dropdown.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.11
* **Streaming:** Apache Kafka & Zookeeper
* **Database:** InfluxDB 2.7
* **Frontend:** Plotly Dash
* **Orquestación:** Docker Compose
