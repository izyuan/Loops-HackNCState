import speech_recognition as sr
import time
import serial
import requests
import openai
import os
import pyaudio
from google.cloud import speech
from openai import OpenAI
arduino = serial.Serial('COM3', 9600, timeout=1)
def chat_with_openai(user_input, system_prompt = ""):
    print(user_input)
    print(system_prompt)
    try:
        client = OpenAI(api_key = "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")
        messages_in = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_in
        )
        print(completion)
        response_text = completion.choices[0].message.content
        print(response_text)
        messages_in.append({"role": "assistant", "content": response_text})
        return response_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
en_language_dict = { 
    "english": "en-US",
    "spanish": "es-ES",
    "french": "fr-FR",
    "german": "de-DE",
    "italian": "it-IT",
    "portuguese": "pt-BR",  # Brazilian Portuguese is more widely used internationally
    "russian": "ru-RU",
    "chinese": "zh-CN",  # Assuming Simplified Chinese
    "japanese": "ja-JP",
    "korean": "ko-KR",
    "arabic": "ar-SA",  # Saudi Arabian Arabic
    "hindi": "hi-IN",
    "bengali": "bn-BD",  # Bangladesh Bengali
    "dutch": "nl-NL",
    "greek": "el-GR",
    "hebrew": "he-IL",
    "turkish": "tr-TR",
    "thai": "th-TH",
    "swedish": "sv-SE",
    "polish": "pl-PL",
    "norwegian": "no-NO",
    "danish": "da-DK",
    "finnish": "fi-FI",
    "hungarian": "hu-HU",
    "czech": "cs-CZ",
    "romanian": "ro-RO",
    "vietnamese": "vi-VN",
    "indonesian": "id-ID",
    "malay": "ms-MY",
    "filipino": "tl-PH",
    "persian": "fa-IR",
    "ukrainian": "uk-UA",
    "serbian": "sr-RS",
    "croatian": "hr-HR",
    "bulgarian": "bg-BG",
    "slovak": "sk-SK",
    "lithuanian": "lt-LT",
    "latvian": "lv-LV",
    "estonian": "et-EE",
    "slovenian": "sl-SI",
    "maltese": "mt-MT",
    "icelandic": "is-IS",
    "irish": "ga-IE",
    "welsh": "cy-GB",
    "basque": "eu-ES",
    "catalan": "ca-ES",
    "luxembourgish": "lb-LU",
    "scots gaelic": "gd-GB",
    "macedonian": "mk-MK",
    "albanian": "sq-AL",
    "belarusian": "be-BY",
    "bosnian": "bs-BA",
    "georgian": "ka-GE",
    "azerbaijani": "az-AZ",
    "armenian": "hy-AM",
    "kazakh": "kk-KZ",
    "uzbek": "uz-UZ",
    "tajik": "tg-TJ",
    "kyrgyz": "ky-KG",
    "turkmen": "tk-TM",
    "mongolian": "mn-MN",
    "pashto": "ps-AF",
    "kurdish": "ku-TR",  # There's no specific ISO code for Kurdish; using Turkey's code as it's one of the regions where Kurdish is spoken
    "yoruba": "yo-NG",
    "zulu": "zu-ZA",
    "xhosa": "xh-ZA",
    "swahili": "sw-KE",  # Kenyan Swahili
    "amharic": "am-ET",
    "afrikaans": "af-ZA",
    "nepali": "ne-NP",
    "sinhala": "si-LK",
    "tamil": "ta-IN",
    "telugu": "te-IN",
    "kannada": "kn-IN",
    "malayalam": "ml-IN",
    "burmese": "my-MM",
    "khmer": "km-KH",
    "lao": "lo-LA",
    "maori": "mi-NZ",
    "samoan": "sm-WS",
    "tonga": "to-TO",
    "gujarati": "gu-IN"
}
fr_language_dict = {
    "anglais": "en-US",
    "espagnol": "es-ES",
    "français": "fr-FR",
    "allemand": "de-DE",
    "italien": "it-IT",
    "portugais": "pt-BR",
    "russe": "ru-RU",
    "chinois": "zh-CN",
    "japonais": "ja-JP",
    "coréen": "ko-KR",
    "arabe": "ar-SA",
    "hindi": "hi-IN",
    "bengali": "bn-IN",
    "néerlandais": "nl-NL",
    "grec": "el-GR",
    "hébreu": "he-IL",
    "turc": "tr-TR",
    "thaï": "th-TH",
    "suédois": "sv-SE",
    "polonais": "pl-PL",
    "norvégien": "no-NO",
    "danois": "da-DK",
    "finnois": "fi-FI",
    "hongrois": "hu-HU",
    "tchèque": "cs-CZ",
    "roumain": "ro-RO",
    "vietnamien": "vi-VN",
    "indonésien": "id-ID",
    "malais": "ms-MY",
    "philippin": "tl-PH",
    "persan": "fa-IR",
    "ukrainien": "uk-UA",
    "serbe": "sr-RS",
    "croate": "hr-HR",
    "bulgare": "bg-BG",
    "slovaque": "sk-SK",
    "lituanien": "lt-LT",
    "letton": "lv-LV",
    "estonien": "et-EE",
    "slovène": "sl-SI",
    "maltais": "mt-MT",
    "islandais": "is-IS",
    "irlandais": "ga-IE",
    "gallois": "cy-GB",
    "basque": "eu-ES",
    "catalan": "ca-ES",
    "luxembourgeois": "lb-LU",
    "gaélique écossais": "gd-GB",
    "macédonien": "mk-MK",
    "albanais": "sq-AL",
    "biélorusse": "be-BY",
    "bosniaque": "bs-BA",
    "géorgien": "ka-GE",
    "azerbaïdjanais": "az-AZ",
    "arménien": "hy-AM",
    "kazakh": "kk-KZ",
    "ouzbek": "uz-UZ",
    "tadjik": "tg-TJ",
    "kirghize": "ky-KG",
    "turkmène": "tk-TM",
    "mongol": "mn-MN",
    "pachto": "ps-AF",
    "kurde": "ku-TR",
    "yoruba": "yo-NG",
    "zoulou": "zu-ZA",
    "xhosa": "xh-ZA",
    "swahili": "sw-KE",
    "amharique": "am-ET",
    "afrikaans": "af-ZA",
    "népalais": "ne-NP",
    "cinghalais": "si-LK",
    "tamoul": "ta-IN",
    "télougou": "te-IN",
    "kannada": "kn-IN",
    "malayalam": "ml-IN",
    "birman": "my-MM",
    "khmer": "km-KH",
    "laotien": "lo-LA",
    "maori": "mi-NZ",
    "samoan": "sm-WS",
    "tongien": "to-TO",
    "gujarati": "gu-IN"
}
es_language_dict = {
    "inglés": "en-US",
    "español": "es-ES",
    "francés": "fr-FR",
    "alemán": "de-DE",
    "italiano": "it-IT",
    "portugués": "pt-BR",
    "ruso": "ru-RU",
    "chino": "zh-CN",
    "japonés": "ja-JP",
    "coreano": "ko-KR",
    "árabe": "ar-SA",
    "hindi": "hi-IN",
    "bengalí": "bn-IN",
    "neerlandés": "nl-NL",
    "griego": "el-GR",
    "hebreo": "he-IL",
    "turco": "tr-TR",
    "tailandés": "th-TH",
    "sueco": "sv-SE",
    "polaco": "pl-PL",
    "noruego": "no-NO",
    "danés": "da-DK",
    "finés": "fi-FI",
    "húngaro": "hu-HU",
    "checo": "cs-CZ",
    "rumano": "ro-RO",
    "vietnamita": "vi-VN",
    "indonesio": "id-ID",
    "malayo": "ms-MY",
    "filipino": "tl-PH",
    "persa": "fa-IR",
    "ucraniano": "uk-UA",
    "serbio": "sr-RS",
    "croata": "hr-HR",
    "búlgaro": "bg-BG",
    "eslovaco": "sk-SK",
    "lituano": "lt-LT",
    "letón": "lv-LV",
    "estonio": "et-EE",
    "esloveno": "sl-SI",
    "maltés": "mt-MT",
    "islandés": "is-IS",
    "irlandés": "ga-IE",
    "galés": "cy-GB",
    "vasco": "eu-ES",
    "catalán": "ca-ES",
    "luxemburgués": "lb-LU",
    "gaélico escocés": "gd-GB",
    "macedonio": "mk-MK",
    "albanés": "sq-AL",
    "bielorruso": "be-BY",
    "bosnio": "bs-BA",
    "georgiano": "ka-GE",
    "azerbaiyano": "az-AZ",
    "armenio": "hy-AM",
    "kazajo": "kk-KZ",
    "uzbeko": "uz-UZ",
    "tayiko": "tg-TJ",
    "kirguís": "ky-KG",
    "turcomano": "tk-TM",
    "mongol": "mn-MN",
    "pastún": "ps-AF",
    "kurdo": "ku-TR",
    "yoruba": "yo-NG",
    "zulú": "zu-ZA",
    "xhosa": "xh-ZA",
    "suajili": "sw-KE",
    "amárico": "am-ET",
    "afrikáans": "af-ZA",
    "nepalí": "ne-NP",
    "cingalés": "si-LK",
    "tamil": "ta-IN",
    "telugu": "te-IN",
    "canarés": "kn-IN",
    "malayalam": "ml-IN",
    "birmano": "my-MM",
    "jemer": "km-KH",
    "lao": "lo-LA",
    "maorí": "mi-NZ",
    "samoano": "sm-WS",
    "tongano": "to-TO",
    "gujarati": "gu-IN"
}
sw_language_dict = {
    "kiingereza": "en-US",
    "kispania": "es-ES",
    "kifaransa": "fr-FR",
    "kijerumani": "de-DE",
    "kiitaliano": "it-IT",
    "kireno": "pt-BR",
    "kirusi": "ru-RU",
    "kichina": "zh-CN",
    "kijapani": "ja-JP",
    "kikorea": "ko-KR",
    "kiarabu": "ar-SA",
    "kihindi": "hi-IN",
    "kibengali": "bn-IN",
    "kiholanzi": "nl-NL",
    "kigiriki": "el-GR",
    "kihebrania": "he-IL",
    "kituruki": "tr-TR",
    "kithai": "th-TH",
    "kiswidi": "sv-SE",
    "kipolandi": "pl-PL",
    "kinorwe": "no-NO",
    "kideni": "da-DK",
    "kifini": "fi-FI",
    "kihungaria": "hu-HU",
    "kicheki": "cs-CZ",
    "kiromania": "ro-RO",
    "kivietinamu": "vi-VN",
    "kiindonesia": "id-ID",
    "kimalei": "ms-MY",
    "kifilipino": "tl-PH",
    "kiajemi": "fa-IR",
    "kiukreni": "uk-UA",
    "kiserbia": "sr-RS",
    "kikroeshia": "hr-HR",
    "kibulgaria": "bg-BG",
    "kislovakia": "sk-SK",
    "kilithuania": "lt-LT",
    "kilatvia": "lv-LV",
    "kiestonia": "et-EE",
    "kislovenia": "sl-SI",
    "kimati": "mt-MT",
    "kiaislandi": "is-IS",
    "kiirelandi": "ga-IE",
    "kiwelisi": "cy-GB",
    "kibaski": "eu-ES",
    "kikatalani": "ca-ES",
    "kiluxemburgi": "lb-LU",
    "kigaeliki ya kiskoti": "gd-GB",
    "kimasedonia": "mk-MK",
    "kialbania": "sq-AL",
    "kibelarusi": "be-BY",
    "kibosnia": "bs-BA",
    "kijojia": "ka-GE",
    "kiazabajani": "az-AZ",
    "kiarmenia": "hy-AM",
    "kikazaki": "kk-KZ",
    "kiuzbeki": "uz-UZ",
    "kitajiki": "tg-TJ",
    "kikyrgyz": "ky-KG",
    "kiturkmeni": "tk-TM",
    "kimongolia": "mn-MN",
    "kipashto": "ps-AF",
    "kikurdi": "ku-TR",
    "kiyoruba": "yo-NG",
    "kizulu": "zu-ZA",
    "kixhosa": "xh-ZA",
    "kiswahili": "sw-KE",
    "kiamhari": "am-ET",
    "kiafrikaans": "af-ZA",
    "kinepali": "ne-NP",
    "kisinhala": "si-LK",
    "kitamil": "ta-IN",
    "kitelegu": "te-IN",
    "kikannada": "kn-IN",
    "kimalayalam": "ml-IN",
    "kiburma": "my-MM",
    "kikhmer": "km-KH",
    "kilao": "lo-LA",
    "kimaori": "mi-NZ",
    "kisamoa": "sm-WS",
    "kitonga": "to-TO",
    "kigujarati": "gu-IN"
}
stopListeningTriggers = {
    "en-US": "stop listening",
    "es-ES": "deja de escuchar",
    "fr-FR": "arrête d'écouter",
    "sw-KE": "acha kusikiliza"
}
stopTranslatingTriggers = {
    "en-US": "stop translating",
    "es-ES": "deja de traducir",
    "fr-FR": "arrête de traduire",
    "sw-KE": "acha kutafsiri"
}
translateFromTriggers = {
    "en-US": "translate from",
    "es-ES": "traducir desde",
    "fr-FR": "traduire de",
    "sw-KE": "tafsiri kutoka"
}
print_words = False
userLanguage = "english".lower()
print("LOOPS: " + userLanguage.lower() + " language")
def getLanguageCode(language, user_language = "english"):
    # Normalize the language input to lower case to match the dictionary keys
    language1 = language.lower()
    if(user_language == "english"): #Place to play with more language selection
        return en_language_dict.get(language)  # Returns None if the language is not found
    elif(user_language == "spanish"):
        return es_language_dict.get(language)  # Returns None if the language is not found
    elif(user_language == "french"):
        return fr_language_dict.get(language)  # Returns None if the language is not found
    elif(user_language == "swahili"):
        return sw_language_dict.get(language)  # Returns None if the language is not found
    else:
       send_words_to_arduino(f"Language not found ")
       return None
user_language_code = getLanguageCode(userLanguage.lower())

#DEFAULTS
wordList = []
print_words = False
#SOUND SETTINGS
RATE = 34000
CHUNK = int(RATE / 10)  # 100ms SPEED SETTINGS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/rushi/Downloads/onyx-day-399204-b0b4df23d5b7.json"
client = speech.SpeechClient()

def miracle():
    config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code=user_language_code,
    use_enhanced=True,
    model="phone_call",  
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )
    global wordList
    global print_words
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    print("Listening")
    audiogenerator = (stream.read(CHUNK) for _ in range(int(RATE / CHUNK * 3600)))
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audiogenerator)
    responses = client.streaming_recognize(streaming_config, requests)

    recent_words = {}  # Dictionary to track words and their last added time
    word_cooldown = 1  # Time in seconds to consider a word as duplicate
    for response in responses:
        for result in response.results:
            if not result.is_final:
                continue

            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            words = transcript.split(" ")
            print(words)
            if(print_words):send_words_to_arduino(transcript)
            if(checkTrigger("stop listening", words, 5)[0]):
                    send_words_to_arduino("Have a nice day! :)")
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    return
            if(checkTrigger("start hearing assistance", words, 5)[0]):
                send_words_to_arduino("starting hearing assistance")
                print_words = True
            if(checkTrigger("stop hearing assistance",words, 5)[0]):
                send_words_to_arduino("stopping hearing assistance")
                print_words = False  
            
            translationCheck, translationIndex, translationLength = checkTrigger("translate from", words, 5)
            if(translationCheck):
                translate_language = words[-translationIndex + translationLength].lower()
                translate_language_code = getLanguageCode(translate_language, "english")
                send_words_to_arduino(f"Translating from {translate_language} to {userLanguage}")            
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=RATE,
                    language_code=translate_language_code,
                    use_enhanced=True,
                    model="phone_call",  
                )
                streaming_config = speech.StreamingRecognitionConfig(
                    config=config,
                    interim_results=True
                )

                print(translate_language)
                print(translate_language_code)
                print(config)

                #Detect the language
                translate_stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK
                )
                print("Listening")
                audiogenerator = (stream.read(CHUNK) for _ in range(int(RATE / CHUNK * 3600)))
                requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audiogenerator)
                responses = client.streaming_recognize(streaming_config, requests)
                while True:
                    recent_words = {}  # Dictionary to track words and their last added time
                    word_cooldown = 1  # Time in seconds to consider a word as duplicate
                    for response in responses:
                        for result in response.results:
                            if not result.is_final:
                                continue

                            if not result.alternatives:
                                continue

                            transcript = result.alternatives[0].transcript
                            words = transcript.split(" ")
                            print(words)
                            print(transcript)
                            group_size = 5

                            # Split the words into groups
                            word_groups = [words[i:i+group_size] for i in range(0, len(words), group_size)]

                            for group in word_groups:
                                # Join the words in each group back into a string
                                group_text = " ".join(group)

                                # Translate the group text
                                translator = chat_with_openai(group_text, f"""Translate all text provided directly to {userLanguage}. Do not converse with me or speak to me. Simply take inputs of {translate_language} and output the exact meaning in {userLanguage} and nothing else.""")

                                # Print and send the translated text to Arduino
                                print(translator)
                                send_words_to_arduino(translator)

                    if(checkTrigger("stop translating",words, 5)[0]):
                        miracle()
                        return
                    elif(checkTrigger("stop listening",words, 5)[0]):
                        send_words_to_arduino("Have a nice day! :)")
                        translate_stream.stop_stream()
                        translate_stream.close()
                        p.terminate()
                        return


def checkTrigger (trig,wordList, number):
    lenwl = len(wordList)
    trig = trig.split(" ")
    i = len(trig)
    t = len(trig)
    if (trig == wordList[-i:]):
            return True, i, t 

    i = i + 1 
    while True:
        if (i > lenwl):
             return False, 0, 0
        elif (trig == wordList[-i: -i + t ]):
            return True, i, t 
        elif(i == number):
            break
        else: 
            i = i + 1 
    return False, 0, 0

def send_to_arduino(word):
    word_serial = word.encode('utf-8')  # Convert the word to bytes
    arduino.write(word_serial + b'\n')  # Send the word to Arduino, add newline to denote end of transmission
    time.sleep(.1)  # Wait for Arduino to process the data

def send_words_to_arduino(words):
    if(words is not None):
        to_unpack = words.split(" ")
        for unpack in to_unpack:
            send_to_arduino(unpack)

miracle()