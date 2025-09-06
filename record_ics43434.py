import pyaudio
import wave
from datetime import datetime
import os
import zmq   # 🔹 추가

# 配置参数
SAMPLERATE = 48000
CHANNELS = 2
DURATION = 10
CHUNK = 1024
FORMAT = pyaudio.paInt32
SAVE_PATH = os.path.expanduser("~/audio")
os.makedirs(SAVE_PATH, exist_ok=True)

# 🔹 ZMQ 설정
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://192.168.4.1:9001")   # MIC 전송용 포트

def record_and_save():
    pa = pyaudio.PyAudio()
    print(f"开始录音（每{DURATION}秒保存一次，按Ctrl+C停止）...")
    try:
        while True:
            # 生成文件名
            filename = f"{SAVE_PATH}/ics43434_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            
            # 打开流并录音
            stream = pa.open(format=FORMAT, channels=CHANNELS, rate=SAMPLERATE,
                            input=True, frames_per_buffer=CHUNK)
            print(f"录制中：{filename}")
            
            frames = [stream.read(CHUNK) for _ in range(int(SAMPLERATE/CHUNK*DURATION))]
            
            # 停止流并保存
            stream.stop_stream()
            stream.close()
            
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(pa.get_sample_size(FORMAT))
                wf.setframerate(SAMPLERATE)
                wf.writeframes(b''.join(frames))
            
            print(f"已保存：{filename}")

            # 🔹 ZMQ로 전송
            with open(filename, "rb") as f:
                socket.send_multipart([b"mic", f.read()])
            print(f"已发送：{filename}\n")
            
    except KeyboardInterrupt:
        print("\n程序停止")
    finally:
        pa.terminate()
        socket.close()
        context.term()

if __name__ == "__main__":
    record_and_save()
