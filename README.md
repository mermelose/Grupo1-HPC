# Grupo1-HPC

# Proyecto de Web Scraping y Aceleración con Computación Paralela

## Descripción

Este proyecto se centra en el análisis y la mejora de los procesos de web scraping, utilizando técnicas de computación paralela, contenedores (Docker) y computación en la nube para acelerar la recolección de datos desde páginas web. El caso de estudio utilizado es la extracción de datos de jugadores de fútbol desde el sitio web Transfermarkt.

## Archivos del Proyecto

- **`codigo.py`**: Script en Python para realizar el web scraping de jugadores de fútbol desde Transfermarkt. Extrae información como el nombre, la nacionalidad, la edad, el club, entre otros.
- **`InformeParcial_MontalvoSalazarZhou.pdf`**: Informe parcial detallado sobre las técnicas de computación paralela, contenedores y cloud computing aplicadas para optimizar el scraping.
- **`PresentacionParcial_MontalvoSalazarZhou.pdf`**: Presentación con los resultados preliminares del proyecto y la metodología utilizada para evaluar distintas soluciones de optimización.

## Objetivos

- Comparar el rendimiento de diferentes técnicas de computación para acelerar los procesos de web scraping.
- Evaluar el impacto de la computación paralela, contenedores y computación en la nube en los tiempos de ejecución, escalabilidad y eficiencia de los procesos de scraping.

## Metodología

1. **Implementación Secuencial**: Se desarrolla un script básico de scraping sin paralelismo para establecer una línea base de comparación.
2. **Paralelismo Local**: Se implementa la paralelización mediante el uso de hilos y procesos locales para mejorar el rendimiento.
3. **Contenerización con Docker**: Se crea un entorno Docker para ejecutar múltiples instancias del scraper en paralelo, mejorando la eficiencia y portabilidad.
4. **Despliegue en la Nube**: Se evalúa el rendimiento del scraper ejecutado en la nube (Microsoft Azure) para analizar la escalabilidad y costo asociado.

## Requisitos

- Python 3.x
- Librerías:
  - `requests`
  - `beautifulsoup4`
  - `csv`
  - `time`
  - `random`
  - `datetime`

## Ejecución

1. Clona o descarga este repositorio.
2. Instala las dependencias necesarias con el siguiente comando:
   ```bash
   pip install requests beautifulsoup4
