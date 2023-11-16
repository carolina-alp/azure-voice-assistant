from dotenv import load_dotenv
import os
import requests
import text_to_speech

load_dotenv("env.txt")
# Clave de API de Google
api_key = os.environ.get('API_GOOGLE_KEY')

# URL base de la API de Knowledge Graph
url = "https://kgsearch.googleapis.com/v1/entities:search"

def analyze_text(text_input: str):

    # Parámetros de la consulta
    params = {
        "query": text_input,
        "key": api_key,
        "limit": 1,  # Puedes ajustar el límite según tus necesidades
        "languages": "es"
    }

    # Realizar la solicitud a la API
    response = requests.get(url, params=params)
    data = response.json()

    # Procesar la respuesta
    if "itemListElement" in data and len(data["itemListElement"]) > 0:
        result = data["itemListElement"][0]["result"]

        description = result["detailedDescription"]["articleBody"]
        text_to_speech.synthesize_text_once(description)
  

    else:
        description = f"Lo siento, no puedo ayudarte porque no tengo información sobre {text_input}"
        text_to_speech.synthesize_text_once(description)
        
        #return description            
    

if __name__ == "__main__":
    text = 'Bidenju'  
    analyze_text(text)