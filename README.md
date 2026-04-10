# 🚗 Automatic License Plate Recognition (ALPR)

An end-to-end **Automatic License Plate Recognition system** that detects vehicles, tracks them across frames, identifies license plates, extracts text using OCR, and generates a final annotated video output.

---

## 📌 Features

* 🚘 Vehicle detection using YOLOv8
* 🔄 Multi-object tracking using SORT
* 🪪 License plate detection (custom YOLO model)
* 🔠 Text extraction using OCR
* 🧹 OCR post-processing & correction
* 📉 Missing frame handling using interpolation
* 🎥 Final visualization with bounding boxes and plate numbers

---

## 🧠 System Overview

```
Video Input
   ↓
Vehicle Detection (YOLOv8)
   ↓
Tracking (SORT)
   ↓
License Plate Detection
   ↓
OCR (Text Extraction)
   ↓
CSV Output
   ↓
Interpolation (Missing Data Handling)
   ↓
Visualization
   ↓
Final Output Video
```

---

## 🛠️ Tech Stack

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* EasyOCR
* SORT Tracking Algorithm
* NumPy, Pandas
* SciPy

---

## 📁 Project Structure

```
├── main.py                  # Core pipeline (detection + tracking + OCR)
├── util.py                  # Helper functions (OCR, formatting, CSV writing)
├── add_missing_data.py      # Interpolation for missing frames
├── visualize.py             # Final video rendering
├── sample1.mp4              # Input video
├── yolov8n.pt               # Pretrained YOLO model
├── license_plate_detector.pt # Custom plate detection model
├── test.csv                 # Raw output
├── test_interpolated.csv    # Processed output
├── out.mp4                  # Final output video
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/alpr-project.git
cd alpr-project
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Download models

* Download `yolov8n.pt` from Ultralytics
* Place `license_plate_detector.pt` in the root directory

---

## ▶️ Usage

### Step 1: Run detection + OCR pipeline

```
python main.py
```

👉 Generates: `test.csv`

---

### Step 2: Handle missing frames

```
python add_missing_data.py
```

👉 Generates: `test_interpolated.csv`

---

### Step 3: Generate final video

```
python visualize.py
```

👉 Generates: `out.mp4`

---

## 📊 Output

* 📄 CSV file with detection + OCR results
* 🎥 Annotated video with:

  * Vehicle bounding boxes
  * License plate bounding boxes
  * Extracted plate numbers

---

## 🔍 Key Concepts

* **Bounding Box (bbox):** Rectangle enclosing detected objects
* **SORT:** Tracking algorithm for maintaining object identity
* **Kalman Filter:** Predicts object movement across frames
* **OCR:** Converts image text → machine-readable text

---

## ⚠️ Limitations

* OCR may fail on low-resolution plates
* Performance drops in low-light conditions
* Depends on model accuracy
* Occlusions can affect detection

---

## 🚀 Future Improvements

* Replace OCR with deep learning-based models (CRNN, Transformers)
* Apply super-resolution for better plate clarity
* Use temporal OCR across frames
* Train models specifically for Indian license plates
* Deploy in real-time systems

---

## 📸 Demo

*Add screenshots or GIFs here*

---

## 🙌 Acknowledgements

* YOLOv8 by Ultralytics

* EasyOCR

* SORT Tracking Algorithm

* Special thanks to **Muhammad Zeerak Khan** for the original implementation and inspiration from the project:
  **"Automatic-License-Plate-Recognition-using-YOLOv8"**

---

## 📜 Credit Note

This project is based on and inspired by the work of Muhammad Zeerak Khan.
Modifications, enhancements, and additional features have been implemented for learning and project purposes.

---

## 📜 License

This project is for educational purposes.

---

## 👨‍💻 Author

**Tirthankar Ghosh**
BTech, NIT Sikkim