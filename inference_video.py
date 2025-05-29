from ultralytics import YOLO
import os
from datetime import datetime
import cv2
import shutil

# Create results directory if it doesn't exist
results_dir = "results/videos"
os.makedirs(results_dir, exist_ok=True)

# Input video path
video_path = "runs/test_video/130225-746395323.mp4"

# Generate timestamp for unique folder name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(results_dir, f"detection_{timestamp}")
os.makedirs(output_dir, exist_ok=True)

# Load model
model = YOLO("runs/best.pt")

print(f"Processing video: {video_path}")
print(f"Results will be saved to: {output_dir}")

# Run detection on the video
results = model.predict(
    source=video_path,
    conf=0.25,
    save=True,
    save_dir=output_dir,
    name='annotated_video'
)

# The video is saved in the runs/detect folder by default
default_output = os.path.join("runs", "detect", "annotated_video.mp4")
final_output = os.path.join(output_dir, "annotated_video.mp4")

# Move the video to our desired location
if os.path.exists(default_output):
    shutil.move(default_output, final_output)
    print(f"\nVideo processing complete!")
    print(f"Annotated video saved to: {final_output}")
    
    # Get video information
    cap = cv2.VideoCapture(final_output)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    cap.release()
    
    print(f"\nVideo details:")
    print(f"- Duration: {duration:.2f} seconds")
    print(f"- FPS: {fps:.2f}")
    print(f"- Total frames: {frame_count}")
else:
    print(f"\nError: Could not find the processed video at {default_output}")
