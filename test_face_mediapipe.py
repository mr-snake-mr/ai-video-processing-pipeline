import cv2
import mediapipe as mp

def test_mediapipe_face(video_path):
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1,  # 0=short range, 1=long range
        min_detection_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Could not read frame")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        print("Faces detected:", len(results.detections))
    else:
        print("Faces detected: 0")


if __name__ == "__main__":
    test_mediapipe_face("test_video.mp4")