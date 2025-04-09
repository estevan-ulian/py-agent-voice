from dotenv import load_dotenv
from pynput import keyboard
from queue import Queue
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
import os
import numpy as np
import sounddevice as sd
import whisper
import wave
import openai
import io
import soundfile as sf
import threading
import pandas as pd


load_dotenv()

class TalkingLLM():
    def __init__(self, model="gpt-3.5-turbo-0125", whisper_size="medium", df_file='df_rent.csv', key_press="<cmd>"):
        self.dataset = f"datasets/{df_file}"
        self.is_record = False
        self.key_press = key_press
        self.audio_data = []
        self.samplerate = 44100
        self.channels = 1
        self.dtype = 'int16'
        self.client = openai.Client()
        self.whisper = whisper.load_model(name=whisper_size)
        self.tts_voice = "alloy"
        self.model = model
        self.agent_queue = Queue()
        self.create_agent()

    def start_or_stop_recording(self):
        if self.is_record:
            self.is_record = False
            self.save_and_transcribe()
            self.audio_data = []
        else:
            print("Recording...")
            self.audio_data = []
            self.is_record = True

    def create_agent(self):
        df = pd.read_csv(self.dataset)
        self.agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model=self.model),
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

    def save_and_transcribe(self):
        print('Saving the recording...')
        if "temp.wav" in os.listdir():
            os.remove("temp.wav")
        wav_file = wave.open("test.wav", 'wb')
        wav_file.setnchannels(self.channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(self.samplerate)
        wav_file.writeframes(np.array(self.audio_data, dtype=self.dtype))
        wav_file.close()

        result = self.whisper.transcribe("test.wav", fp16=False)
        print("Usuário: ", result["text"])
        response = self.agent.invoke(result['text'])
        print('Agent: ', response['output'])
        self.agent_queue.put(response['output'])

    def convert_and_play(self):
        tts_text = ''
        while True:
            tts_text = self.agent_queue.get()
            if '.' in tts_text or '?' in tts_text or '!' in tts_text:
                
                spoken_response = self.client.audio.speech.create(model="tts-1",
                                                                  voice=self.tts_voice,
                                                                  response_format="opus",
                                                                  input=tts_text)

                buffer = io.BytesIO()
                for chunk in spoken_response.iter_bytes(chunk_size=4096):
                    buffer.write(chunk)
                buffer.seek(0)

                with sf.SoundFile(buffer, 'r') as sound_file:
                    data = sound_file.read(dtype=self.dtype)
                    sd.play(data, sound_file.samplerate)
                    sd.wait()
                tts_text = ''

    def run(self):
        t1 = threading.Thread(target=self.convert_and_play)
        t1.start()
        print(f"Pressione {self.key_press} para iniciar/parar a gravação.")

        def callback(indata, frames, time, status):
            if status:
                print(status)
            if self.is_record:
                self.audio_data.extend(indata.copy())

        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=callback):
            def on_activate():
                self.start_or_stop_recording()

            def for_canonical(f):
                return lambda k: f(l.canonical(k))

            hotkey = keyboard.HotKey(
                keyboard.HotKey.parse(self.key_press), on_activate=on_activate
            )
            with keyboard.Listener(
                on_press=for_canonical(hotkey.press),
                on_release=for_canonical(hotkey.release)
            ) as l:
                l.join()


if __name__ == "__main__":
    talking_llm = TalkingLLM(
        model="gpt-3.5-turbo-0125",
        whisper_size="base",
        key_press="<caps_lock>",
        df_file='df_rent.csv'
    )
    talking_llm.run()
