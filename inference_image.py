from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os
from datetime import datetime


# Create results directory if it doesn't exist
results_dir = "results/images"
os.makedirs(results_dir, exist_ok=True)

# Upload one or more test images
original_image_path = "runs\test_images\cup.jpeg"

# Load your trained model
model = YOLO("runs/best.pt")  # or path in Drive

# Run inference and show side-by-side results
original = cv2.imread(original_image_path)
if original is None:
    raise FileNotFoundError(f"Could not find or open the image at: {original_image_path}")

original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

results = model(original_image_path, conf=0.25, imgsz=640)
annotated = results[0].plot()
annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

# Generate timestamp for unique filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"detection_{timestamp}.jpg"

# Save the annotated image
output_path = os.path.join(results_dir, output_filename)
cv2.imwrite(output_path, annotated)

print(f"Detection result saved to: {output_path}")

# Show both images
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(original_rgb)
ax[0].set_title("Input Image")
ax[0].axis("off")
ax[1].imshow(annotated_rgb)
ax[1].set_title("YOLOv8 Detection")
ax[1].axis("off")
plt.show()
