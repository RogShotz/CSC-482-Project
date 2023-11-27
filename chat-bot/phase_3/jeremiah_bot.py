"""
Author: Jeremiah Lee
This Phase-3 functionality of our chat bot allows the user to give a command to the bot
such as: Translate this: Hola, me llamo Jeremias 
and give a response in the specified language (or enlgish if not specified)"""

import nltk, requests, subprocess, time


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
        
libretranslate = LibreTranslateAPI()

input_text = "Me llamo Jeremias"
translated_text = libretranslate.translate(input_text, target_lang="es")
libretranslate.done()

if translated_text:
    print(f"Original text: {input_text}")
    print(f"Translated text: {translated_text}")
    