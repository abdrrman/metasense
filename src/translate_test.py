from googletrans import Translator

def translate_to_and_fro(text):
    translator = Translator()

    # Detect language
    detection = translator.detect(text)
    original_lang = detection.lang
    print(f"Detected language: {original_lang}")

    # Translate to English
    translation = translator.translate(text, dest='en')
    print(f"Translated to English: {translation.text}")

    # Translate back to original language
    back_translation = translator.translate(translation.text, dest=original_lang)
    print(f"Translated back to {original_lang}: {back_translation.text}")

# Usage
translate_to_and_fro('Hola mundo')