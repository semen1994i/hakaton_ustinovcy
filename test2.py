import wave
import json
from vosk import Model, KaldiRecognizer

# Убедитесь, что ваш аудиофайл имеет формат WAV с частотой дискретизации 16kHz и моно
def recognize_speech_vosk(file_path):
    # Загружаем русскую модель (скачать можно по ссылке ниже)
    model = Model("vosk-model-small-ru-0.22/vosk-model-small-ru-0.22")  # Укажите путь к модели

    # Открываем аудиофайл
    wf = wave.open(file_path, "rb")

    # Проверяем формат файла (должен быть 16kHz и моно)
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        print("Аудиофайл должен быть в формате WAV с частотой 16kHz и моно")
        return

    # Создаем распознаватель
    rec = KaldiRecognizer(model, wf.getframerate())

    # Распознаем аудио
    result_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            result_text += result.get("text", "") + " "

    # Финальное распознавание
    final_result = json.loads(rec.FinalResult())
    result_text += final_result.get("text", "")

    print("Распознанный текст:", result_text)

# Пример использования
audio_file_path = "test2.wav"  # Укажите путь к вашему файлу
recognize_speech_vosk(audio_file_path)
