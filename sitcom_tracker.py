import cv2
import mediapipe as mp
import numpy as np
import subprocess
import os


def shot_based_sitcom_crop(input_video, output_video, start_time, end_time):

    temp_segment = "temp_segment.mp4"
    temp_silent = "temp_silent.mp4"

    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-to", str(end_time),
        "-i", input_video,
        "-c", "copy",
        temp_segment
    ])

    cap = cv2.VideoCapture(temp_segment)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ALWAYS 9:16
    target_width = int(height * 9 / 16)
    target_width -= target_width % 2

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_silent, fourcc, fps, (target_width, height))

    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    )

    prev_gray = None
    scene_threshold = 40
    current_center_x = width // 2
    scene_initialized = False
    frames_since_cut = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        scene_cut = False

        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            if np.mean(diff) > scene_threshold:
                scene_cut = True

        prev_gray = gray

        if scene_cut:
            scene_initialized = False
            frames_since_cut = 0

        if not scene_initialized and frames_since_cut < 10:

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb)

            if results.detections:

                x_min = width
                x_max = 0

                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x1 = int(bbox.xmin * width)
                    w_box = int(bbox.width * width)
                    x2 = x1 + w_box

                    x_min = min(x_min, x1)
                    x_max = max(x_max, x2)

                group_width = x_max - x_min

                # Add padding if 2 people
                if len(results.detections) >= 2:
                    padding = int(group_width * 0.25)
                    x_min -= padding
                    x_max += padding

                current_center_x = (x_min + x_max) // 2

                scene_initialized = True

        frames_since_cut += 1

        start_x = current_center_x - target_width // 2

        if start_x < 0:
            start_x = 0
        if start_x + target_width > width:
            start_x = width - target_width

        cropped = frame[:, start_x:start_x + target_width]
        out.write(cropped)

    cap.release()
    out.release()

    subprocess.run([
        "ffmpeg", "-y",
        "-i", temp_silent,
        "-i", temp_segment,
        "-filter_complex",
        "scale=1080:1920",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:a", "aac",
        output_video
    ])

    os.remove(temp_segment)
    os.remove(temp_silent)

    print("Finished:", output_video)


if __name__ == "__main__":
    shot_based_sitcom_crop(
        input_video="horizontal_input_h264.mp4",
        output_video="vertical_output.mp4",
        start_time=60,
        end_time=120
    )