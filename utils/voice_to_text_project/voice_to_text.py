import speech_recognition as sr

class VoiceToText:
    def __init__(self, pause_threshold=3.0):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = pause_threshold 

    def record_audio(self):
        with sr.Microphone() as source:
            print("Listening... Speak now.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source)
                print("Finished listening.")
                return audio
            except sr.WaitTimeoutError:
                print("No speech detected")
                return None

    def convert_to_text(self, audio):
        if audio is None:
            return "No audio captured"
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Usage example
if __name__ == "__main__":
    vtt = VoiceToText()
    audio = vtt.record_audio()
    text = vtt.convert_to_text(audio)
    print(f"Recognized text: {text}")
