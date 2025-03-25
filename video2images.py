import cv2
import os

# Define path
video_path = "data/video/tsai.mp4"
output_folder = "data/tsai_video/images"

os.makedirs(output_folder, exist_ok=True)

# Read video
cap = cv2.VideoCapture(video_path)

frame_count = 0
frame_rate = 5
save_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Rotate frame
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    
    # Save frame
    if frame_count % frame_rate == 0:
        frame_path = os.path.join(output_folder, f"frame_{save_count:04d}.png")  # 0000 ~ 9999
        cv2.imwrite(
            filename=frame_path,
            img=frame
        )
        save_count += 1
    
    frame_count += 1

# Release video
cap.release()

print(f"Video has {frame_count} frames. Saved to {output_folder}")