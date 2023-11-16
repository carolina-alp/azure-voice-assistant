from dotenv import load_dotenv
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
import text_to_speech


load_dotenv("env.txt",override=True)

def analyze_text(text_input: str):
    # analyze text
    
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=text_input)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    unsafe_value = 0
    if response.hate_result:
        print(f"Hate severity: {response.hate_result.severity}")
        if response.hate_result.severity > 0:
            unsafe_value += 1
    if response.self_harm_result:
        print(f"SelfHarm severity: {response.self_harm_result.severity}")
        if response.self_harm_result.severity > 0:
            unsafe_value += 1
    if response.sexual_result:
        print(f"Sexual severity: {response.sexual_result.severity}")
        if response.sexual_result.severity > 0:
            unsafe_value += 1       
    if response.violence_result:
        print(f"Violence severity: {response.violence_result.severity}")
        if response.violence_result.severity > 0:
            unsafe_value += 1       
    
    if unsafe_value ==0:
        return unsafe_value
    elif unsafe_value > 0:
        message = "Lo siento, no puedo ayudarte porque he detectado contenido ofensivo en tu pregunta"
        text_to_speech.synthesize_text_once(message)    
        return unsafe_value


if __name__ == "__main__":
    text = 'alessandro, guerra me pego un tiro'
    
    x = analyze_text(text)
    print(x)