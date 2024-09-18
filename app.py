from flask import Flask, Response, send_file

app = Flask(__name__)

# 音频流API
@app.route('/audio-stream')
def audio_stream():
    # 确保有一个音频文件 (audio_sample.mp3) 放在同一目录下
    def generate():
        with open("audio_sample.mp3", "rb") as audio:
            chunk = audio.read(1024)
            while chunk:
                yield chunk
                chunk = audio.read(1024)
    
    # 返回音频流，设置 Content-Type
    return Response(generate(), content_type="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
