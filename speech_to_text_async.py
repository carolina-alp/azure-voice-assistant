# Reconocer comandos de voz, habla continua y lenguaje

from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import time
import json
import text_to_speech


load_dotenv("env.txt",override=True)
speech_configuration = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'),
                                        region=os.environ.get('SPEECH_REGION'))


def speech_recognize_continuous_async_from_microphone(speech_config=speech_configuration):
    data_text = []
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="es-BO")

    done = False

    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        print('RECOGNIZING: {}'.format(evt.result.text))

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        print('RECOGNIZED: {}'.format(evt.result.text))
        if speechsdk.ResultReason.RecognizedSpeech==evt.result.reason and len(evt.result.text) > 0 :
            print('RECOGNIZED:', evt.result.text)
            data_text.append(evt.result.text) 


    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition"""
        print('CLOSING on {}'.format(evt.result.text))
 
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)



    # Perform recognition. `start_continuous_recognition_async asynchronously initiates continuous recognition operation,
    # Other tasks can be performed on this thread while recognition starts...
    # wait on result_future.get() to know when initialization is done.
    # Call stop_continuous_recognition_async() to stop recognition.
    result_future = speech_recognizer.start_continuous_recognition_async()

    result_future.get()  # wait for voidfuture, so we know engine initialization is done.
    print('Continuous Recognition is now running, say something.')

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or speech_recognizer will go out of scope and be destroyed while running.
        print('type "stop" then enter when done')
        stop = input()
        if (stop.lower() == "stop"):
            #print('Stopping async recognition.')
            
            speech_recognizer.stop_continuous_recognition_async()
            break
    #print("recognition stopped, main thread can exit now.")
    return str(" ".join(data_text))


def get_wake_word(text, wake_word):
    text_lower = text.lower()
    if wake_word in text_lower[:12]:
        #message='Claro!'
        #text_to_speech.synthesize_text_once(message)
        print(text_lower)
        text_lower = text_lower.replace("coco","")        
        return text_lower
    else:
        messaje='Intentalo de nuevo, empieza con "{}" seguido de tu pregunta"...'.format(wake_word.capitalize())
        text_to_speech.synthesize_text_once(messaje)  
        print('Para realizar tu busqueda, empieza con "{}" seguido de tu pregunta"...'.format(wake_word.capitalize())) 
        return None 

def speech_recognize_continuous_async_from_microphone_get_wake_word(wake_word='coco'):
    print('Para realizar tu busqueda, empieza con "{}" seguido de tu pregunta"...'.format(wake_word.capitalize()))
    input_text = speech_recognize_continuous_async_from_microphone()
    answer_text = get_wake_word(input_text, wake_word)
    return answer_text
    
if __name__ == "__main__":

    speech_recognize_continuous_async_from_microphone_get_wake_word()
