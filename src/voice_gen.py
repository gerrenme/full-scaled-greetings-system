import torch
import soundfile as sf

from constants import VOICE_GEN_DATA


class VoiceGenerator:
    def __init__(self) -> None:
        self.model_sample_rate: int = 48000
        self.torch_device: torch.device = torch.device("cpu")

        self.model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts',
                                                  language=VOICE_GEN_DATA["language"], speaker=VOICE_GEN_DATA["id"])
        self.model.to(self.torch_device)


    def generate_audio(self, text: str):
        audio = self.model.apply_tts(text=text, speaker=VOICE_GEN_DATA["speaker"], sample_rate=self.model_sample_rate)
        return audio


    def save_audio(self, audio, filename: str) -> bool:
        try:
            sf.write(filename, audio.cpu().numpy(), self.model_sample_rate)
            return True

        except Exception as _ex:
            print(f"[VoiceGenerator->save_audio]. Can't save audio. Error :: {_ex}")
            return False
