import cv2
import numpy as np

def test_face_dnn(video_path):
    # Load pre-trained face detector model (OpenCV DNN)
    model_file = cv2.data.haarcascades.replace(
        "haarcascades",
        "dnn/face_detector/opencv_face_detector_uint8.pb"
    )
    config_file = cv2.data.haarcascades.replace(
        "haarcascades",
        "dnn/face_detector/opencv_face_detector.pbtxt"
    )

    # Fallback if not bundled
    try:
        net = cv2.dnn.readNet(model_file, config_file)
    except:
        print("DNN model not found in OpenCV build.")
        return

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Could not read frame.")
        return

    h, w = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    face_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            face_count += 1

    print("Faces detected (DNN):", face_count)


if __name__ == "__main__":
    test_face_dnn("test_video.mp4")