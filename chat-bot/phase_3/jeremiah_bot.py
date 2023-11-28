"""
Author: Jeremiah Lee
This Phase-3 functionality of our chat bot allows the user to give a command to the bot
such as: Translate this: Hola, me llamo Jeremias 
and give a response in the specified language (or enlgish if not specified)
"""

import requests, subprocess, time, re
#packages langid, langcodes, libretranslate

class LibreTranslateAPI:
    def __init__(self, api_url="http://localhost:5000/"):
        self.api_url = api_url
        try:
            self.proc = subprocess.Popen(["libretranslate", "--host", "localhost"])
            self.wait_for_server()
        except FileNotFoundError:
            print("Libretranslate command not found. Make sure it's installed and in your PATH.") 
    
    def wait_for_server(self):
        url = self.api_url
        max_retries = 10
        retry_interval = 1

        for _ in range(max_retries):
            try:
                response = requests.get(url)
                response.raise_for_status()
                return
            except requests.exceptions.RequestException:
                time.sleep(retry_interval)

    def translate(self, text, source_lang="auto", target_lang="en"):
        """
        Translate text using the LibreTranslate API.

        Parameters:
        - text: The text to be translated.
        - source_lang: The source language (auto-detect by default).
        - target_lang: The target language (English by default).

        Returns:
        - Translated text.
        """
        endpoint = f"{self.api_url}/translate"
        params = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
        }

        response = requests.post(endpoint, data=params)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result["translatedText"]
            return translated_text
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def done(self):
        self.proc.kill()

def parse_translation_request(msg):
    patterns = [
        r'translate this (\w+) into (\w+)\s*:?\s*(.+)', #trans this source into target
        r'translate this into (\w+)\s*:?\s*(.+)', #trans this into target
        r'translate this (\w+)\s*:?\s*(.+)', #trans this source
        r'translate this\s*:?\s*(.+)', #trans this
        r'translate\s*:?\s*(.+)' #trans
    ]
    
    for pattern in patterns:
        match = re.match(pattern, msg, re.IGNORECASE)
        if match:
            if len(match.groups()) == 3:
                language = [match.group(1),  match.group(2)]
                text = match.group(3)
            elif len(match.groups()) == 2:
                language = match.group(1)
                text = match.group(2)
            else:
                language = None
                text = match.group(1)
            return language, text
    
    return None, None

def get_iso_code(language):
    mapping = {
        "Afrikaans": "af",
        "Amharic": "am",
        "Aragonese": "an",
        "Arabic": "ar",
        "Assamese": "as",
        "Azerbaijani": "az",
        "Belarusian": "be",
        "Bulgarian": "bg",
        "Bengali": "bn",
        "Breton": "br",
        "Bosnian": "bs",
        "Catalan": "ca",
        "Czech": "cs",
        "Welsh": "cy",
        "Danish": "da",
        "German": "de",
        "Dzongkha": "dz",
        "Greek": "el",
        "English": "en",
        "Esperanto": "eo",
        "Spanish": "es",
        "Estonian": "et",
        "Basque": "eu",
        "Persian": "fa",
        "Finnish": "fi",
        "Faroese": "fo",
        "French": "fr",
        "Irish": "ga",
        "Galician": "gl",
        "Gujarati": "gu",
        "Hebrew": "he",
        "Hindi": "hi",
        "Croatian": "hr",
        "Haitian": "ht",
        "Hungarian": "hu",
        "Armenian": "hy",
        "Indonesian": "id",
        "Icelandic": "is",
        "Italian": "it",
        "Japanese": "ja",
        "Javanese": "jv",
        "Georgian": "ka",
        "Kazakh": "kk",
        "Khmer": "km",
        "Kannada": "kn",
        "Korean": "ko",
        "Kurdish": "ku",
        "Kyrgyz": "ky",
        "Latin": "la",
        "Luxembourgish": "lb",
        "Lao": "lo",
        "Lithuanian": "lt",
        "Latvian": "lv",
        "Malagasy": "mg",
        "Macedonian": "mk",
        "Malayalam": "ml",
        "Mongolian": "mn",
        "Marathi": "mr",
        "Malay": "ms",
        "Maltese": "mt",
        "Norwegian Bokmål": "nb",
        "Nepali": "ne",
        "Dutch": "nl",
        "Norwegian Nynorsk": "nn",
        "Norwegian": "no",
        "Occitan": "oc",
        "Oriya": "or",
        "Punjabi": "pa",
        "Polish": "pl",
        "Pashto": "ps",
        "Portuguese": "pt",
        "Quechua": "qu",
        "Romanian": "ro",
        "Russian": "ru",
        "Kinyarwanda": "rw",
        "Northern Sami": "se",
        "Sinhala": "si",
        "Slovak": "sk",
        "Slovenian": "sl",
        "Albanian": "sq",
        "Serbian": "sr",
        "Swedish": "sv",
        "Swahili": "sw",
        "Tamil": "ta",
        "Telugu": "te",
        "Thai": "th",
        "Tagalog": "tl",
        "Turkish": "tr",
        "Uyghur": "ug",
        "Ukrainian": "uk",
        "Urdu": "ur",
        "Vietnamese": "vi",
        "Volapük": "vo",
        "Walloon": "wa",
        "Xhosa": "xh",
        "Chinese": "zh",
        "Zulu": "zu",
    }
    
    language = language.title()
    
    if language in mapping:
        return mapping[language]
    return None
           
def jeremiah_bot(irc, msg, sender, channel):
    if not any(word in msg for word in ["translate", "Translate"]):
        return
    libretranslate = LibreTranslateAPI()
    lang, text = parse_translation_request(msg)
    source = None
    target = None
    translation = None
    
    if lang:
        if isinstance(lang, list):
            source = get_iso_code(lang[0])
            target = get_iso_code(lang[1])
        elif "into" in msg:
            target = get_iso_code(lang)
        else:
            source = get_iso_code(lang)
    
    #translate [lang1] into [lang2]: text
    if not source and not target:
        translation = libretranslate.translate(text)
        irc.send(
            channel, f"\"{text}\" to English is \"{translation}\"")
        # print(f"\"{text}\" to English is \"{translation}\"")
    elif not target:
        translation = libretranslate.translate(text, source_lang=source)
        irc.send(
            channel, f"{sender}: \"{text}\" to {lang} is \"{translation}\"")
        # print(f"\"{text}\" to {lang} is \"{translation}\"")
    else:
        translation = libretranslate.translate(text, source_lang=source, target_lang=target)
        irc.send(
            channel, f"{sender}: \"{text}\" to {lang[1]} is \"{translation}\"")
        # print(f"\"{text}\" to {lang[1]} is \"{translation}\"")
    libretranslate.done()