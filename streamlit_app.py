import streamlit as st
from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
import tempfile
import os
import time

# Page configuration
st.set_page_config(page_title="Kitchen Utilities Detector", layout="wide")
st.title("🍳 Kitchen Utilities Detector")

# Initialize session state for video processing
if 'video_processed' not in st.session_state:
    st.session_state.video_processed = False
if 'result_path' not in st.session_state:
    st.session_state.result_path = None

# Load and cache model
@st.cache_resource
def load_model():
    return YOLO("runs/best.pt")

model = load_model()

# Sidebar selection
mode = st.sidebar.selectbox("Select Mode", ["Image", "Video", "Webcam"])

if mode == "Image":
    st.header("Image Detection")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert('RGB')
        img_arr = np.array(img)
        results = model(img_arr)
        annotated = results[0].plot()
        # Show original and annotated
        st.image([img, annotated], caption=["Original", "Detected"], width=400)
        # Show detections table
        boxes = results[0].boxes
        if boxes:
            records = []
            for box in boxes:
                cls = model.names[int(box.cls)]
                conf = float(box.conf)
                records.append({"Object": cls, "Confidence": round(conf, 2)})
            st.table(records)

elif mode == "Video":
    st.header("Video Detection")
    
    # Reset state when new video is uploaded
    if 'current_video' not in st.session_state:
        st.session_state.current_video = None
    
    video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])
    
    if video_file is not None:
        # Check if this is a new video
        if st.session_state.current_video != video_file.name:
            st.session_state.video_processed = False
            st.session_state.result_path = None
            st.session_state.current_video = video_file.name
        
        # Save video to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(video_file.name)[1])
        tmp.write(video_file.read())
        tmp.flush()
        vid_path = tmp.name

        # Display original video
        st.video(vid_path)

        # Process video only if not already processed
        if not st.session_state.video_processed:
            if st.button("Start Detection"):
                with st.spinner("Detecting objects in video..."):
                    # Create output directory
                    out_dir = os.path.join('results', 'videos', 'annotated')
                    os.makedirs(out_dir, exist_ok=True)
                    
                    # Run detection
                    model.predict(
                        source=vid_path,
                        conf=0.25,
                        save=True,
                        project='results/videos',
                        name='annotated'
                    )
                    
                    # Find the result file
                    stem = os.path.splitext(os.path.basename(vid_path))[0]
                    result_path = None
                    
                    # Wait for the file to be created (max 30 seconds)
                    start_time = time.time()
                    while time.time() - start_time < 30:
                        if os.path.exists(out_dir):
                            files = os.listdir(out_dir)
                            for fname in files:
                                if fname.startswith(stem):
                                    result_path = os.path.join(out_dir, fname)
                                    break
                            if result_path:
                                break
                        time.sleep(1)
                    
                    if result_path and os.path.exists(result_path):
                        st.session_state.result_path = result_path
                        st.session_state.video_processed = True
                        st.success("Detection complete!")
                    else:
                        st.error("⚠️ Processing timed out. Please try again.")
        
        # Display results if available
        if st.session_state.video_processed and st.session_state.result_path:
            st.video(st.session_state.result_path)
            with open(st.session_state.result_path, 'rb') as f:
                st.download_button(
                    "Download Annotated Video",
                    f,
                    file_name=os.path.basename(st.session_state.result_path),
                    mime='video/mp4'
                )

else:  # Webcam
    st.header("Webcam Detection")
    if st.button("Start Webcam"):
        cap = cv2.VideoCapture(0)
        frame_disp = st.image([])
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            res = model(frame)
            ann = res[0].plot()
            frame_disp.image(cv2.cvtColor(ann, cv2.COLOR_BGR2RGB))
        cap.release()
        st.info("Webcam session ended.")
