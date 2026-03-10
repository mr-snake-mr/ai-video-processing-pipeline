from faster_whisper import WhisperModel

def transcribe_audio(video_path):
    print("Loading Whisper model... (first time will download model)")
    
    model = WhisperModel("base", device="cpu", compute_type="int8")

    print("Transcribing...")
    segments, info = model.transcribe(video_path)

    print(f"Detected language: {info.language}")
    print("Segments:\n")

    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

if __name__ == "__main__":
    transcribe_audio("test_video.mp4")