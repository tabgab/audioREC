import streamlit as st
from audiorecorder import audiorecorder
import os
import openai
import json
import streamlit.components.v1 as components
import requests
import numpy as np 
import logging

from io import BytesIO
from time import sleep
file_path = "audio.wav"

#API KEYS 
OPENAI_API_KEY = st.secrets.OPENAI_API_KEY
AssembyAI_API_KEY = st.secrets.AssembyAI_API_KEY


    


#Transcribe audio to text.

audioheaders = {
    'authorization': AssembyAI_API_KEY, 
    'content-type': 'application/json',
}

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

def upload_to_assemblyai(file_path):

    def read_audio(file_path):

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(5_242_880)
                if not data:
                    break
                yield data

    upload_response =  requests.post(upload_endpoint, 
                                     headers=audioheaders, 
                                     data=read_audio(file_path))

    return upload_response.json().get('upload_url')

def transcribe(upload_url): 

    json = {"audio_url": upload_url}
    
    response = requests.post(transcription_endpoint, json=json, headers=audioheaders)
    transcription_id = response.json()['id']

    return transcription_id

def get_transcription_result(transcription_id): 

    current_status = "queued"

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"

    while current_status not in ("completed", "error"):
        
        response = requests.get(endpoint, headers=headers)
        current_status = response.json()['status']
        
        if current_status in ("completed", "error"):
            return response.json()['text']
        else:
            sleep(10)

def call_gpt3(prompt):

    response = openai.Completion.create(engine = "text-davinci-001", 
                                        prompt = prompt, max_tokens = 50)
    return response["choices"][0]["text"]

def main():

    st.title("Talking to GPT-3")
    file_path = "audio.wav"

    