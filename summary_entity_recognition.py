from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractiveSummaryAction
) 
import pandas as pd
import text_to_speech

load_dotenv("env.txt",override=True)

key = os.environ.get('LANGUAGE_KEY')
endpoint = os.environ.get('LANGUAGE_ENDPOINT')


# Autenticarse
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client


# Ejemplo para resumir texto
def sample_extractive_summarization(documents):

    client = authenticate_client()
    document = [documents]

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractiveSummaryAction(max_sentence_count=1)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("Error: '{}' - Mensaje: '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            print("Resumen: \n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            )

    return " ".join([sentence.text for sentence in extract_summary_result.sentences])

# Example function for recognizing entities from text
def entity_recognition_example(documents):
    client = authenticate_client()
    try:
        result = client.recognize_entities(documents = [documents])[0]

        #print("Named Entities:\n")

        data_list = []

        for entity in result.entities:
            data_list.append([entity.text, entity.category, entity.confidence_score])
            
        columns = ['Name','Category','Confidence Score']
        df = pd.DataFrame(data_list, columns=columns)


        if len(df[df['Category'] == 'Person'])> 0:
            entity = df[df['Category'] == 'Person'].iloc[0].Name

            return entity

        elif len(df[df['Category'] == 'Person']) == 0:
            entity = []
            message = "Lo siento, soy un asistente únicamente orientado a darte información sobre figuras públicas."
            text_to_speech.synthesize_text_once(message)

            return None

    
    except Exception as err:
        print("Encountered exception. {}".format(err))





if __name__ == "__main__":
    document = "Taylor Alison Swift es una cantautora, \
                productora, directora, actriz y empresaria estadounidense. \
                Criada en Wyomissing, se mudó a Nashville a los 14 años para \
                realizar una carrera de música country." 
    
    summarization = sample_extractive_summarization(document)
    entity = entity_recognition_example(document)