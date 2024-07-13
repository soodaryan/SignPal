from utils.voice_to_text_project.voice_to_text import VoiceToText
from utils.ISLGenerator.ISL_converter import ISLConverter
def main():
    vtt = VoiceToText()
    converter = ISLConverter()
    audio = vtt.record_audio()
    text = vtt.convert_to_text(audio)
    print(f"Recognized text: {text}")
    print(f"ISL Converted: {converter.text_to_isl(text)}")

if __name__ == "__main__":
    main()