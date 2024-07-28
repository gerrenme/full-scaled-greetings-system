from voice_gen import VoiceGenerator
import yadisk
import os
import random
from openai import OpenAI
from constants import GREETING_THEMES

private_vars = os.environ
YADISK_TOKEN: str = private_vars["YADISK_TOKEN"]
OPENAI_API_KEY: str = private_vars["OPENAI_API_KEY"]


class Tools:
    def __init__(self):
        self.voice_gen: VoiceGenerator = VoiceGenerator()
        self.yadisk_client: yadisk.YaDisk = yadisk.YaDisk(token=YADISK_TOKEN)
        self.openai_client: OpenAI = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=OPENAI_API_KEY
        )


    def create_audio(self, audio_text: str, username: str) -> bool:
        try:
            generated_audio = self.voice_gen.generate_audio(text=audio_text)
            self.voice_gen.save_audio(filename=f"../generated_audio/to_user_{username}.mp3", audio=generated_audio)
            return True

        except Exception as _ex:
            print(f"[VoiceGenerator->run]. Can't process partners file. Error :: {_ex}")
            return False


    def download_image_yadisk(self, image_type: str) -> str:
        filename: str = image_type + str(random.randint(a=1, b=12)) + ".jpg"
        try:
            self.yadisk_client.download(f"GreetingsSystem/{filename}", filename)
            return filename

        except Exception as _ex:
            print(f"[Tools->download_image_yadisk]. Can't download file {filename}. Error :: {_ex}")
            return ""


    def create_greeting(self):
        greeting_themes: list[str] = [random.choice(GREETING_THEMES), random.choice(GREETING_THEMES)]
        completion = self.openai_client.chat.completions.create(
            model="meta/llama-3.1-405b-instruct",
            messages=[{"role": "user", "content": f"Сгенерируй приятное поздравление на следующие темы: "
                                                  f"{greeting_themes[0]}, {greeting_themes[1]}"}],
            temperature=0.5,
            top_p=0.7,
            max_tokens=128,
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
