import streamlit as st
import sounddevice as sd
import numpy as np

def main():
    st.title("Audio Recorder")

    chunk_duration = 0.1  # Duration of each audio chunk in seconds
    audio_chunks = []  # To store recorded audio chunks

    recording = False

    if st.button("Record"):
        global recording
        recording = True

    if recording:
        with st.spinner("Recording..."):
            audio_chunk = sd.rec(int(chunk_duration * 44100), samplerate=44100, channels=1)
            audio_chunks.append(audio_chunk)
    else:
        if audio_chunks:
            sd.stop()

    if st.button("Stop"):
        global recording
        recording = False

    if audio_chunks:
        st.write("Recorded Audio Chunks:")
        for idx, chunk in enumerate(audio_chunks):
            st.audio(chunk, format="wav", caption=f"Chunk {idx + 1}")

if __name__ == "__main__":
    main()
