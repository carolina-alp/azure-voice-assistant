# Azure-voice-assistant
# Descripción del proyecto

Este proyecto tiene como objetivo crear un asistente activado por voz que responda preguntas sobre figuras públicas utilizando Azure AI Cognitive Services. El asistente reconoce comandos de voz, analiza la seguridad del texto ingresado, extrae entidades, obtiene información de la API Knowledge Graph y sintetiza respuestas en voz.

## Estructura del proyecto

1. **Reconocimiento de voz y detección de palabras de activación**

Archivo: `Speech_to_text_async.py`

Este archivo reconoce comandos de voz desde un micrófono y detecta una palabra de activación para iniciar al asistente. Inicialmente, el proyecto pedía desarrollar un asistente llamado Alessandro, pero debido a la alta sensibilidad del programa, este no identificaba de forma correcta el nombre de Alessandro sino de palabras similares tales como Alejandro, Sandro, etc. Por este motivo se vio conveniente cambiar el nombre del modelo a Coco, que tiende a ser mejor identificado.

2. **Análisis de seguridad del contenido**

Archivo: `content_safety.py`

Este archivo analiza la seguridad de la entrada de texto mediante Azure Content Safety.

3. **Interacción del gráfico de conocimiento**

Archivo: `Ask_google.py`

Este archivo consulta la API de Knowledge Graph para obtener información sobre entidades reconocidas.

4. **Resumen de texto y reconocimiento de entidades**

Archivo: `resumen_entidad_reconocimiento.py`

Utiliza Azure Text Analytics para resumir texto y reconocer entidades, centrándose en las personas.

Utiliza:

* `sample_extractive_summarization()`, para resumir.
* `entity_recognition_example(document)`, para reconocimiento de entidades.

5. **Síntesis de texto a voz**

Archivo: `text_to_speech.py`

Este archivo sintetiza texto en voz mediante Azure Speech Service.

## Configuración del entorno

Se debe crear un environment desde Anaconda Navigator. La versión de Python utilizada es la 3.10 para no tener problemas en la ejecución. Se deben instalar los paquetes de Python necesarios:

pip install -r requisitos.txt

Y configurar los servicios cognitivos de Azure:

Voz: SPEECH_KEY y SPEECH_REGION en el archivo .env.
Seguridad del contenido: CONTENT_SAFETY_KEY y CONTENT_SAFETY_ENDPOINT en el archivo .env.
API: API_GOOGLE_KEY en el archivo .env.
Análisis de texto: LANGUAGE_KEY y LANGUAGE_ENDPOINT en el archivo .env.
## Ejecución
Se debe comenzar la pregunta con la palabra de activación "Coco" seguida de la consulta.
Se debe tener cuidado de que las claves API, estas no deben estar expuestas.


