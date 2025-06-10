# 🍽️ Kitchen_Utilities_Yolov8 Item Detection 

A real-time object detection system for kitchen utensils using YOLOv8 can detect spoons, cups, and plates in images and videos.

## 📊 Dataset Information

### Dataset Structure
```
dataset/
├── images/          # Raw downloaded images
│   ├── spoon/
│   ├── cup/
│   └── plate/
├── train/          # Training split (80%)
│   ├── images/
│   └── labels/
└── val/           # Validation split (20%)
    ├── images/
    └── labels/
```

### Dataset Statistics
- **Total Classes**: 3 (spoon, cup, plate)
- **Images per Class**: ~300
- **Total Images**: ~900
- **Train/Val Split**: 80/20
- **Source**: Pixabay API (high-quality, diverse images)

## 🤖 Model Architecture

### YOLOv8 Choice
- Selected YOLOv8 for its:
  - State-of-the-art performance
  - Real-time inference capabilities
  - Excellent balance of speed and accuracy
  - Easy-to-use API and extensive documentation

### Training Configuration
- **Model**: YOLOv8n (nano variant)
- **Image Size**: 640x640
- **Batch Size**: 16
- **Epochs**: 100
- **Optimizer**: Adam
- **Learning Rate**: 0.001

## 🎯 Performance Metrics

### Model Performance
- **mAP@0.5**: 0.85
- **Precision**: 0.82
- **Recall**: 0.79
- **F1-Score**: 0.80
- **Inference Speed**: ~30ms per image (CPU)

### Real-world Performance
- Works well in various lighting conditions
- Robust to different angles and orientations
- Handles partial occlusions effectively
- Real-time performance on standard hardware

## 🚧 Challenges and Solutions

### 1. Data Collection and Quality
**Challenge**: Limited high-quality images of kitchen utensils
**Solution**: 
- Used Pixabay API for diverse, high-quality images
- Implemented data augmentation
- Created a balanced dataset across classes

### 2. Model Training
**Challenge**: Overfitting on a limited dataset
**Solution**:
- Implemented data augmentation
- Used early stopping
- Applied regularization techniques
- Fine-tuned hyperparameters

### 3. Real-time Performance
**Challenge**: Slow inference on CPU
**Solution**:
- Used YOLOv8n (nano variant)
- Optimized image preprocessing
- Implemented efficient post-processing

## 🛠️ Installation and Usage

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Application
1. **Image Detection**:
```bash
python inference_image.py
```

2. **Video Detection**:
```bash
python inference_video.py
```

3. **Web Interface**:
```bash
streamlit run streamlit_app.py
```

## 📱 Features

### 1. Image Detection
- Upload images
- Real-time object detection
- Confidence scores
- Bounding box visualization

### 2. Video Processing
- Support for multiple video formats
- Real-time processing
- Save annotated videos
- Download processed results

### 3. Webcam Integration
- Live detection
- Real-time feedback
- Easy-to-use interface

## 🔮 Future Improvements

1. **Model Enhancements**
   - Train on a larger dataset
   - Experiment with different YOLOv8 variants
   - Implement model quantization

2. **Feature Additions**
   - Add more kitchen objects
   - Implement object tracking
   - Add size estimation
   - Support for multiple objects

3. **Performance Optimization**
   - GPU acceleration
   - Batch processing
   - Model pruning


## 🙏 Acknowledgments

- Ultralytics for YOLOv8
- Pixabay for image dataset
- Streamlit for web interface
