# Football Analysis - Computer Vision Pipeline

An end-to-end computer vision system that analyzes football (soccer) match footage to detect and track players, referees, and the ball in real time. The pipeline classifies players into teams using jersey color clustering, estimates real-world player speed and distance covered, determines ball possession, and compensates for camera movement — all from a single broadcast video input.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![YOLO](https://img.shields.io/badge/YOLO-v11m-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)
![scikit--learn](https://img.shields.io/badge/scikit--learn-KMeans-orange)

## Sample Output

<!-- TODO: Replace these placeholders with actual screenshots/GIFs from your output video -->

| Input Frame | Output Frame |
|:-----------:|:------------:|
| ![Input](assets/sample_input.png) | ![Output](assets/sample_output.png) |

> **To add your own samples:** Take a screenshot from `input_videos/08fd33_4.mp4` and `output_videos/output_video.avi`, save them to an `assets/` folder, and update the paths above. A GIF works even better — you can use [ffmpeg](https://ffmpeg.org/) to convert a short clip:
> ```bash
> ffmpeg -i output_videos/output_video.avi -vf "fps=10,scale=800:-1" -t 5 assets/demo.gif
> ```

## Features

- **Object Detection & Tracking** — Fine-tuned YOLO11m with ByteTrack for robust multi-object tracking of players, referees, and the ball across frames
- **Team Classification** — Unsupervised K-Means clustering on jersey colors to automatically assign players to teams (no manual labeling needed)
- **Ball Possession Analysis** — Real-time assignment of ball to the nearest player, with cumulative team ball control percentages
- **Speed & Distance Estimation** — Perspective transformation from pixel coordinates to real-world pitch coordinates (meters), enabling accurate speed (km/h) and distance (m) calculations
- **Camera Movement Compensation** — Lucas-Kanade optical flow to estimate camera pan/tilt and adjust all position measurements accordingly
- **View Transformation** — Homography-based perspective transform mapping 2D image points to a 68m x 23.32m pitch coordinate system

## Architecture

```
Input Video
    │
    ▼
┌─────────────────────┐
│  YOLO11m Detection   │──── Detect players, referees, ball
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  ByteTrack Tracker   │──── Assign persistent IDs across frames
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Camera Movement     │──── Optical flow on frame edges
│  Estimator           │──── Adjust positions for camera pan/tilt
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  View Transformer    │──── Perspective transform: pixels → meters
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Ball Interpolation  │──── Fill missing ball detections (pandas)
└─────────┬───────────┘
          ▼
┌──────────────────────────────────────────────┐
│  Speed & Distance  │  Team Assigner  │  Ball │
│  Estimator         │  (K-Means)      │  Poss.│
└─────────┬──────────┴────────┬────────┴───┬───┘
          └───────────┬───────┘            │
                      ▼                    │
              ┌───────────────┐            │
              │  Annotated    │◄───────────┘
              │  Output Video │
              └───────────────┘
```

## Project Structure

```
football_analysis/
├── main.py                          # Pipeline orchestration
├── trackers/
│   └── tracker.py                   # YOLO + ByteTrack detection & tracking
├── team_assigner/
│   └── team_assigner.py             # K-Means jersey color clustering
├── player_ball_assigner/
│   └── player_ball_assigner.py      # Ball-to-player proximity assignment
├── camera_movement_estimator/
│   └── camera_movement_estimator.py # Optical flow camera tracking
├── view_transformer/
│   └── view_transformer.py          # Perspective transform (2D → 3D)
├── speed_and_distance_estimator/
│   └── speed_and_distance_estimator.py
├── utils/
│   ├── video_utils.py               # Video I/O (OpenCV)
│   └── bbox_utils.py                # Bounding box helpers
├── models/                          # Fine-tuned YOLO weights (.gitignored)
├── training/
│   └── football_training_yolo_v5.ipynb  # Model fine-tuning notebook
├── input_videos/                    # Source match footage (.gitignored)
├── output_videos/                   # Annotated results (.gitignored)
└── stubs/                           # Cached detection results (.gitignored)
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Object Detection | **YOLO11m** (Ultralytics) | Detect players, referees, ball |
| Multi-Object Tracking | **ByteTrack** (supervision) | Persistent ID assignment across frames |
| Team Classification | **K-Means** (scikit-learn) | Unsupervised jersey color clustering |
| Camera Tracking | **Lucas-Kanade Optical Flow** (OpenCV) | Camera movement estimation |
| Perspective Transform | **cv2.perspectiveTransform** | Pixel-to-meter coordinate mapping |
| Ball Interpolation | **pandas** | Fill missing detections via interpolation |
| Video Processing | **OpenCV** | Frame I/O, drawing, annotations |
| Numerical Computing | **NumPy** | Array operations, coordinate math |

## Model Training

The YOLO11m model was fine-tuned on a custom football player detection dataset:

- **Dataset**: 663 images from [Roboflow](https://roboflow.com/) annotated in YOLO format
- **Classes**: Player, Goalkeeper, Referee, Ball
- **Augmentations**: Horizontal flip (50%), brightness adjustment (±20%)
- **Training notebook**: `training/football_training_yolo_v5.ipynb`

The fine-tuned model detects football-specific objects with higher accuracy than the base YOLO model, particularly for small objects like the ball and distinguishing referees from players.

## Getting Started

### Prerequisites

- Python 3.8+
- A football match video clip (place in `input_videos/`)
- Fine-tuned YOLO weights (place `best.pt` in `models/`)

### Installation

```bash
git clone https://github.com/<your-username>/football_analysis.git
cd football_analysis
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

The annotated output video will be saved to `output_videos/output_video.avi`.

### Output Annotations

The output video includes:
- **Colored ellipses** under each player (team colors) with track IDs
- **Triangle marker** above the ball
- **Ball possession indicator** (yellow triangle on the player with the ball)
- **Team ball control %** overlay (cumulative possession stats)
- **Speed** (km/h) and **distance** (m) labels under each player
- **Camera movement** X/Y values

## How It Works

### 1. Detection & Tracking
YOLO11m detects all objects per frame. Goalkeeper detections are merged into the player class. ByteTrack assigns consistent IDs across frames so each player maintains their identity throughout the video.

### 2. Camera Movement Compensation
Optical flow is computed on the edges of each frame (where the pitch lines are most visible) to estimate camera pan and tilt. All player positions are adjusted by this offset so that movement measurements reflect actual player motion, not camera motion.

### 3. Perspective Transformation
A homography matrix maps four known pixel coordinates to their corresponding real-world pitch positions (in meters). This transforms all tracked positions from image space to a 68m x 23.32m pitch coordinate system.

### 4. Speed & Distance
Using the transformed coordinates, player displacement is measured over 5-frame windows (~0.2s at 24fps). Distance is accumulated per player, and speed is reported in km/h.

### 5. Team Classification
The top half of each player's bounding box (jersey region) is extracted and clustered using K-Means (k=2). A second round of K-Means across all players separates them into two teams based on dominant jersey color.

### 6. Ball Possession
The ball is assigned to the closest player within a 70-pixel radius. When no player is close enough, possession carries forward from the last known assignment.
