# Conteo y clasificación de vehículos con COCO-SSD en Lima

Proyecto final del curso Inteligencia Artificial Aplicada, Universidad de Lima (2026-2). ODS 11: Ciudades y comunidades sostenibles.

Aplicación web que detecta, clasifica y cuenta vehículos (autos, motos, buses y camiones) en videos de tráfico, directamente en el navegador, con el modelo COCO-SSD y TensorFlow.js. Incluye un notebook de Google Colab que compara el conteo de la página con un conteo manual.

El código se desarrolló con apoyo de Claude (Anthropic, 2026) mediante programación asistida por IA.

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `index.html` | La aplicación web de conteo. |
| `analisis_conteo.ipynb` | Notebook de Colab: EDA, error por tipo y horario, matriz de confusión y regresión. |
| `plantillas/conteo_manual.csv` | Plantilla para el conteo manual por minuto. |
| `simular.py` | Genera los conteos estimados de la aplicación a partir del conteo manual (indicación del docente). |
| `datos/` | Conteo manual real, archivos estimados de la aplicación y figuras del análisis. |

## Cómo usar la aplicación

1. Abre `index.html` en Google Chrome (doble clic, o desde la versión publicada en GitHub Pages). Necesita internet la primera vez para descargar el modelo.
2. Espera el mensaje "Modelo listo".
3. Elige el video y escribe el horario (por ejemplo, `mañana`). Ese nombre tiene que coincidir con el que usen en `conteo_manual.csv`.
4. Haz dos clics sobre el video para trazar la línea de conteo atravesando todos los carriles.
5. Presiona **Iniciar conteo**. La página avanza el video cuadro por cuadro; tarda más que la duración real del video.
6. Al terminar, descarga **Descargar por minuto (CSV)** y **Descargar cruces (CSV)**.
7. En **Muestra de clasificación**, presiona **Armar muestra**, elige para cada foto qué vehículo es de verdad y presiona **Descargar muestra (CSV)**.

Ajustes usados en el informe: confianza mínima 0.40, modelo MobileNet v2, zona de análisis alrededor de la línea, 10 cuadros por segundo.

### Cómo cuenta

- La página recorta una zona alrededor de la línea y solo busca vehículos ahí, para que los lejanos se vean más grandes.
- COCO-SSD detecta los objetos del recorte; solo se usan las clases `car`, `motorcycle`, `bus` y `truck`.
- Si dos cajas se superponen con IoU mayor a 0.6, se queda la de mayor confianza.
- Cada detección se empareja con el vehículo del cuadro anterior más cercano a su posición prevista (seguimiento por centroide con velocidad).
- Un vehículo se cuenta una sola vez, cuando el trayecto de su centro cruza la línea y ya apareció en al menos 2 cuadros. Su clase es la que el modelo le asignó más veces.

## Cómo correr el análisis

1. Abre `analisis_conteo.ipynb` en Google Colab (Archivo > Subir notebook).
2. Sube a la carpeta de Colab: los `por_minuto_*.csv` y `muestra_*.csv` de la página, y `conteo_manual.csv` ya lleno.
3. Ejecuta todo (Entorno de ejecución > Ejecutar todas). Las figuras se guardan como PNG.
4. Para la regresión en Orange: abre `datos_regresion.csv` con el widget File, conéctalo a Linear Regression y Test and Score, con `total_manual` como variable objetivo.

## Publicar la página con GitHub Pages

En el repositorio: Settings > Pages > Source: `main` y carpeta `/ (root)`. En un par de minutos queda en `https://<usuario>.github.io/<repositorio>/`.
