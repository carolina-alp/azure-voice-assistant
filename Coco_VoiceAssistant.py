import speech_to_text_async
import content_safety
import summary_entity_recognition
import ask_google


ask_question = speech_to_text_async.speech_recognize_continuous_async_from_microphone_get_wake_word()

if ask_question is not None:
    print(ask_question)
    check_safety = content_safety.analyze_text(ask_question)
    
    if check_safety == 0:    
        recognized_entity = summary_entity_recognition.entity_recognition_example(ask_question)
        if recognized_entity is not None:
            description = ask_google.analyze_text(recognized_entity)
            print(description)

