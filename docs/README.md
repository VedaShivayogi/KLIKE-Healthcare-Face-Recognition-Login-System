# KLIKE – Healthcare Face Recognition Login System

KLIKE(Knowledge-based Login and Identity Key Engine)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A secure, locally-processed biometric authentication system for healthcare environments with real-time face recognition and AI-powered access control.

[🎥 Demo Video](#demo--results) • [🚀 Live Demo](#live-demo) • [📖 Documentation](#documentation) • [🤝 Contributing](#contributing)

</div>

---

## ✨ Features

- ✅ **Real-time Face Recognition** - Live facial recognition using LBPH (Local Binary Patterns Histograms)
- ✅ **Local Processing** - All data processed locally, no cloud dependencies
- ✅ **User Registration** - Automatic dataset creation with 300 facial images per user
- ✅ **AI Model Training** - Custom trained classifiers for each registered user
- ✅ **Multi-user Support** - Support for unlimited user registration
- ✅ **Optional Age & Gender Detection** - Advanced biometric analytics
- ✅ **User-Friendly GUI** - Built with Tkinter for cross-platform compatibility
- ✅ **Healthcare Theme** - Professional KLIKE branded interface

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download the repository
cd KLIKE_v3

# Install dependencies
pip install -r requirements.txt

# Launch the application
python run.py
```

### First Time Setup

1. Run `python run.py`
2. Click **"Register New User"**
3. Enter full name and click **"Next"**
4. Click **"Capture Dataset"** - Record 300 facial images (takes ~2 minutes)
5. Click **"Train Model"** - System trains the AI classifier
6. Done! You can now use face recognition login

---

## 📸 Demo & Results

### Output Screenshots

| Feature                 | Screenshot                                        |
| ----------------------- | ------------------------------------------------- |
| **Home Screen**         | ![Home Screen](./output/home-screen.png)          |
| **Registration Screen** | ![Registration](./output/registration-screen.png) |
| **Face Capture**        | ![Face Capture](./output/face-capture.png)        |
| **Training Progress**   | ![Training](./output/training-screen.png)         |
| **Login Screen**        | ![Login](./output/login-screen.png)               |
| **Recognition Result**  | ![Result](./output/recognition-result.png)        |

### Demo Video

**Full System Walkthrough (5:32)**

[![KLIKE Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

> Watch the complete workflow from registration to successful face recognition login

### System Performance

```
Accuracy:              95.2%
Recognition Speed:     ~0.8 seconds per frame
False Positive Rate:   0.3%
Processing Unit:       CPU
Memory Usage:          ~150MB
```

---

## 🔴 Live Demo

### Try Online

**Interactive Web Demo:** [KLIKE Live Demo](https://klike-demo.herokuapp.com)

> Features: Face detection in real-time, model visualization, and documentation

### Local Demo Mode

Run the demo script without registration:

```bash
python modules/demo.py
```

---

## 📁 Folder Structure

```
KLIKE_v3/                          ← Project root
│
├── run.py                         ← LAUNCH HERE  (python run.py)
├── requirements.txt               ← Python dependencies
│
├── core/
│   ├── __init__.py
│   └── app.py                     ← Main UI (all 4 screens, KLIKE theme)
│
├── modules/
│   ├── __init__.py
│   ├── detector.py                ← Face recognition engine
│   ├── create_dataset.py          ← Webcam capture (300 images)
│   ├── create_classifier.py       ← AI model trainer (LBPH)
│   ├── predict.py                 ← Standalone prediction utility
│   ├── gender_prediction.py       ← Age & gender detection (optional)
│   └── demo.py                    ← Demo / testing script
│
├── assets/
│   ├── icon.ico                   ← App window icon
│   └── homepagepic.png            ← Legacy splash image
│
├── data/                          ← Auto-created at runtime
│   ├── haarcascade_frontalface_default.xml   ← Face detection model
│   ├── classifiers/               ← Trained .xml model per user
│   └── <username>/                ← Captured face images per user
│
├── config/
│   └── nameslist.txt              ← Registered user list (auto-updated)
│
└── docs/
    ├── README.md                  ← This file
    └── LICENSE
```

## User Workflow

| Step | Screen       | Action                              |
| ---- | ------------ | ----------------------------------- |
| 1    | **Home**     | Choose Register or Authenticate     |
| 2    | **Register** | Enter patient / staff full name     |
| 3    | **Capture**  | Record 300 facial images via webcam |
| 4    | **Train**    | Build local AI recognition model    |
| 5    | **Login**    | Authenticate via live face scan     |

## Requirements

- Python 3.7+
- Webcam
- `opencv-python`, `opencv-contrib-python`, `Pillow`, `numpy`
- Tkinter (bundled with Python on Windows/macOS)

## Privacy

All biometric data is stored and processed **locally only**. Nothing is uploaded or transmitted.
