import cv2

def test_face_detection(video_path):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error reading frame")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print(f"Faces detected: {len(faces)}")

    cap.release()


if __name__ == "__main__":
    test_face_detection("test_video.mp4")