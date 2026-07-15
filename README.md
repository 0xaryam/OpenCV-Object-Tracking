# 🎯 Smart Object Tracking System Using OpenCV

A real-time object tracking system developed using Python and OpenCV. The application allows users to select an object from a live camera feed and track its movement using the CSRT tracking algorithm

## ✨ Features

- Real-time object tracking using CSRT
- Interactive object selection
- Bounding box visualization
- Object center-point detection
- Motion trail visualization
- Real-time FPS monitoring
- Object position and size display
- Tracking status detection
- Screenshot capture
- Video recording with a REC indicator
- Reset and select a new object without restarting the application

## 🛠️ Technologies Used

- Python
- OpenCV
- CSRT Tracker
- Anaconda
- PyCharm

## 📁 Project Structure

```text
OpenCV-Object-Tracking/
├── object_tracker.py
├── requirements.txt
├── README.md
├── screenshots/
└── recordings/
```

## ⚙️ Installation

### 1. Create a Conda environment

```bash
conda create -n opencv-tracking python=3.11
```

### 2. Activate the environment

```bash
conda activate opencv-tracking
```

### 3. Install the required package

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

Run the following command:

```bash
python object_tracker.py
```

The application will open the default camera

## 🎮 Controls

| Key | Action |
|---|---|
| `R` | Select or reset the object |
| `S` | Save a screenshot |
| `V` | Start or stop video recording |
| `Q` | Quit the application |

## 🧠 How It Works

1. The application captures real-time video using OpenCV
2. The user presses `R` and selects an object using the mouse
3. The CSRT tracking algorithm initializes the selected region
4. The tracker continuously estimates the object's new position
5. A bounding box and center point are drawn around the tracked object
6. Previous center positions are stored to create a motion trail
7. The interface displays tracking status, FPS, position, and object size
8. The user can capture screenshots or record the tracking session

## 📸 Demo

Add a screenshot or GIF of the project here:

```markdown
![Object Tracking Demo](demo.gif)
```

## 🚀 Future Improvements

- Multiple object tracking
- Automatic object detection
- Deep learning integration
- Object classification
- Improved tracking recovery

## 👩‍💻 Author

**Aryam Aseiri**

Developed as part of an OpenCV computer vision task
