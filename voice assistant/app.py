import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai 
import base64


api_key = 'your openai api key'

def setup_openai_client(api_key):
    
    return openai.OpenAI(api_key=api_key)


def transcribe_text_to_voice(client, audio_path):
    audio_file= open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

def chat_completion_call(client, text):
    messages = [{"role": "user", "content": text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content


def text_to_speech_ai(client, speech_file_path, api_response):
    response = client.audio.speech.create(model="tts-1",voice="Onyx",input=api_response)
    response.stream_to_file(speech_file_path)    
    


def main():
    st.sidebar.title("API KEY CONFIGURATION")
    api_key = st.sidebar.text_input("Enter Your openai API Key", type="password")
    st.title("🧑‍💻 Munozi 💬 Talking Assistant")
    st.write("Hi🤖 just click on the voice recorder and let me know how I can help you today?")
    
    if api_key:
        client = setup_openai_client(api_key)
        recorded_audio = audio_recorder()
        if recorded_audio:
            ##Save the Recorded File
            audio_path = "audio_file.wav"
            with open(audio_path, "wb") as f:
                f.write(recorded_audio)

    #Transcribe the saved file to text
            text = transcribe_text_to_voice(client, audio_path)
            st.write(text)

    #Use API to get an AI response
            api_response = chat_completion_call(client, text)
            st.write(api_response)

    # Read out the text response using tts
            speech_file_path = 'audio_response.mp3'
            text_to_speech_ai(client, speech_file_path, api_response)
            st.audio(speech_file_path)
            st.write("AI Response", api_response)

    
if __name__ == "__main__":
    main()    