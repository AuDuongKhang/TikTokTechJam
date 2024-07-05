import os
import yaml
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import subprocess

def video_to_skeleton(path_video):
    # Load the model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Paths to input and output videos
    input_video_path = path_video
    output_video_path = './result/pose.mp4'

    # Khởi tạo VideoCapture cho video đầu vào
    cap = cv2.VideoCapture(input_video_path)

    # Kiểm tra nếu không mở được video đầu vào
    if not cap.isOpened():
        print("Không thể mở video")
        exit()

    # Thuộc tính của video đầu vào
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = 512
    height = 512
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_length = 25
    if num_frames > 125:
        fps = 125 * cap.get(cv2.CAP_PROP_FPS) // int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        num_frames = 125
    else:
        video_length = int(num_frames // 5)

    # Khởi tạo VideoWriter cho video đầu ra
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    print(num_frames)
    print(fps)
    # Đọc và xử lý từng khung hình
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (512,512))
        # Chuyển đổi khung hình sang định dạng RGB (Mediapipe yêu cầu RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Phát hiện pose trên khung hình
        results = pose.process(rgb_frame)

        # Tạo một khung hình đen có cùng kích thước với khung hình gốc
        black_frame = np.zeros_like(frame)

        # Nếu phát hiện được các điểm pose
        if results.pose_landmarks:
            # Vẽ các điểm và kết nối các điểm trên khung hình đen
            mp_drawing.draw_landmarks(
                black_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),  # Màu trắng cho skeleton
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)   # Màu trắng cho connections
            )

        # Ghi khung hình đã chỉnh sửa vào video đầu ra
        out.write(black_frame)

    # Giải phóng các đối tượng VideoCapture và VideoWriter, đóng các cửa sổ đang mở
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Giải phóng tài nguyên của Mediapipe
    pose.close()

    return video_length

def set_prompt(prompt, video_length):
    file_path = './configs/pose_sample.yaml'

    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    config['validation_data']['prompts'] = [
        prompt,
    ]

    config['validation_data']['negative_prompt'] = "Low quality, Disfigured, Extra limbs"
    config['validation_data']['video_length'] = video_length
    config['validation_data']['width'] = 128
    config['validation_data']['height'] = 128
    config['validation_data']['num_inference_steps'] = 1
    config['gradient_checkpointing'] = False

    # Ghi lại tệp YAML
    with open(file_path, 'w') as file:
        yaml.safe_dump(config, file)

    print("Prompts đã được sửa đổi thành công!")

def process_video_pose(prompt, path_video):
    video_length = video_to_skeleton(path_video)
    set_prompt(prompt, video_length)

    # Set environment variable
    os.environ['TORCH_DISTRIBUTED_DEBUG'] = 'DETAIL'

    # Define the command to run
    command = [
        'accelerate', 'launch', 'txt2video.py',
        '--config=configs/pose_sample.yaml',
        '--skeleton_path=result/pose.mp4'
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output and error (if any)
    print(result.stdout)
    print(result.stderr)

   
