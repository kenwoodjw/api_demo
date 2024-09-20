import os
import azure.cognitiveservices.speech as speechsdk
from flask import Flask, request, jsonify

app = Flask(__name__)

# Azure Speech API 配置
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "your_speech_key")
AZURE_REGION = os.getenv("AZURE_REGION", "your_service_region")

def speech_to_text(audio_file_path):
    """调用 Azure Speech-to-Text 进行语音识别"""
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 进行语音识别
    result = speech_recognizer.recognize_once()

    # 处理识别结果
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return {"text": result.text, "success": True}
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return {"error": "No speech could be recognized", "success": False}
    elif result.reason == speechsdk.ResultReason.Canceled:
        return {"error": f"Canceled: {result.cancellation_details.reason}", "success": False}

@app.route('/api/speech-to-text', methods=['POST'])
def handle_speech_to_text():
    """处理前端上传的音频文件并返回识别结果"""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided", "success": False}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "Empty audio file", "success": False}), 400

    # 保存音频文件到本地
    audio_path = os.path.join("/tmp", audio_file.filename)
    audio_file.save(audio_path)

    # 调用 Azure Speech-to-Text 进行识别
    result = speech_to_text(audio_path)

    # 删除本地音频文件
    os.remove(audio_path)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
