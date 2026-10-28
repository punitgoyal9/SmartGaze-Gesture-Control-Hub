# GestureX — AI-Powered Gesture & Face Analysis System

> **This is an early-stage demo and a teaser of a much larger project.** The current version demonstrates a few basic gesture-based computer interactions. More intelligent, accessible, and advanced features are planned for future releases.

## Overview

**GestureX** is a Python-based computer vision project that explores how hand gestures and facial landmarks can be used to interact with a computer through a webcam.

The project combines OpenCV and MediaPipe to detect hand and face landmarks in real time. It demonstrates gesture-based screen brightness adjustment, motion-triggered screenshots, basic predefined gesture recognition, and facial geometry analysis.

The goal is to explore more natural and accessible ways of interacting with computers, with an emphasis on hands-free interaction and future assistive technology.

**This release is a demo, not the final product.** It intentionally focuses on a small set of basic features while laying the foundation for a more capable gesture-interaction system.

## Current Demo Features

### 1. Gesture-Based Brightness Control

- Uses the hand positioned on the right half of the webcam view.
- Tracks the thumb tip and index fingertip.
- Calculates the distance between the two fingertips.
- Maps that distance to a brightness level from 0% to 100%.
- Attempts to adjust system display brightness using `screen-brightness-control`.

### 2. Basic Gesture Recognition

The demo uses hand landmarks and simple geometric rules to identify selected hand configurations.

Examples of intended gesture meanings include:

- **Thumbs Up:** A positive or confirmation-style gesture.
- **Open Palm:** A greeting or stop-style gesture.
- **Closed Fist:** A predefined status gesture.
- **Index and Middle Fingers:** A peace or victory-style gesture.
- **Index Finger:** An attention-style gesture.

Recognition is based on basic rules rather than a trained sign-language classification model. Accuracy can vary with hand orientation, lighting, camera position, and individual movement.

### 3. Motion-Triggered Screenshot Capture

- Uses a hand positioned on the left half of the webcam view.
- Detects a hand with multiple extended fingers.
- Tracks downward wrist movement between consecutive frames.
- Captures a screenshot when the movement threshold is crossed.
- Applies a cooldown to reduce repeated screenshots.
- Saves screenshots as timestamped PNG files in the current working directory.

**Demo interaction:** Open your hand, then move it slowly from top to bottom in the left half of the camera view.

### 4. Facial Landmark Analysis

- Uses MediaPipe Face Landmarker to identify facial landmarks.
- Estimates face width and height from selected landmark points.
- Calculates a facial width-to-height ratio.
- Displays a heuristic male/female label based on a manually selected threshold.

**Important limitation:** This is only an experimental geometric heuristic. It does not reliably detect a person's gender, and facial proportions cannot establish a person's gender identity. The displayed label may be inaccurate and should not be used for identity, eligibility, or other consequential decisions.

### 5. Live Webcam Interface

The OpenCV window displays:

- Hand tracking and fingertip indicators.
- A visual brightness bar and percentage.
- The current predefined gesture label.
- The experimental facial-analysis label.
- A notification when a screenshot is captured.

Press **Q** to close the webcam window.

## How the Demo Works

1. The application checks for the required MediaPipe hand and face model files and downloads them if they are missing.
2. OpenCV initializes the webcam and captures frames.
3. Each frame is flipped horizontally to provide a mirror-style view.
4. MediaPipe detects hand and face landmarks.
5. Hand position determines which interaction logic is evaluated.
6. Finger configurations are matched against predefined rules.
7. Selected actions are triggered, and the results are displayed in the webcam interface.

## Technology Stack

- **Python** — Core application logic
- **OpenCV** — Webcam access, image processing, and interface rendering
- **MediaPipe Tasks** — Hand and face landmark detection
- **NumPy** — Numeric calculations and brightness mapping
- **Math** — Distance and geometry calculations
- **Screen Brightness Control** — System brightness adjustment
- **PyAutoGUI** — Screenshot capture
- **OS and Time modules** — File checks, timestamps, and cooldown timing

## Requirements

- A computer running Windows, macOS, or Linux, subject to library and hardware compatibility
- Python version compatible with the installed MediaPipe release; Python 3.10–3.12 is a reasonable starting point
- A working webcam
- Internet access for installing dependencies and downloading the model files
- A supported display and operating system for brightness adjustment

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/GestureX-AI-Gesture-Control.git
cd GestureX-AI-Gesture-Control
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Python 3.11 is not installed, use another Python version supported by your installed MediaPipe release.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

If the main Python file is named `main.py`:

```bash
python main.py
```

The application will attempt to download the hand and face model files automatically if they are not already present.

## Gesture Interaction Guide

| Hand position | Demo action |
|---|---|
| Right half of the webcam view | Brightness adjustment and basic gesture recognition |
| Thumb and index fingertips at different distances | Adjusts the target brightness |
| Open palm on the right | Displays a greeting/stop-style label |
| Closed fist on the right | Displays a predefined gesture label |
| Index and middle fingers on the right | Displays a peace/victory-style label |
| Index finger on the right | Displays an attention-style label |
| Left half, open hand with multiple extended fingers | Prepares the motion-based screenshot gesture |
| Left half, slow top-to-bottom hand movement | May trigger screenshot capture |

Gesture labels are approximate and depend on the current rule-based implementation. The application does not yet provide complete sign-language understanding.

## Project Structure

```text
GestureX-AI-Gesture-Control/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    └── (optional demo images)
```

The MediaPipe `.task` model files are downloaded automatically when needed and should generally remain outside version control.

## Limitations of This Demo

- Gesture recognition uses simple geometric rules, not a trained sign-language model.
- The current implementation supports only a small selection of predefined gestures.
- Hand orientation and mirror-view assumptions can affect recognition.
- Screenshot triggering depends on the hand movement threshold and cooldown.
- Brightness adjustment depends on hardware and operating-system support.
- Facial analysis is experimental and does not reliably identify gender.
- The demo has not yet been optimized for all lighting conditions, camera setups, or accessibility requirements.
- Some features may behave differently across computers.

## Future Roadmap — More Features Are Planned

**This demo is only the beginning.** GestureX is intended to evolve into a more advanced, intelligent, and accessibility-focused interaction platform.

Potential future developments include:

- **Expanded gesture vocabulary:** More hand signs and customizable gesture mappings.
- **Sign-language assistance:** Research and development toward recognizing supported sign-language gestures and sequences.
- **Communication assistance:** Exploring ways for people who cannot speak, or who have difficulty communicating verbally, to express selected messages through gestures and visual or text-based output.
- **Smarter hand tracking:** Improved gesture recognition across different orientations and lighting conditions.
- **More computer controls:** Gesture-based media playback, navigation, volume control, and other configurable actions.
- **Customizable actions:** Allow users to map supported gestures to their preferred commands.
- **Improved screenshot controls:** More reliable movement detection and configurable triggers.
- **Accessibility-focused interface:** Clearer visual feedback and customizable interaction options.
- **Better testing and performance:** Reduced false triggers, improved stability, and broader device compatibility.

These are planned directions, not features promised or fully implemented in the current release. Sign-language recognition and assistive communication would require dedicated design, validation, and testing with intended users.

## Responsible Use and Privacy

- Webcam frames are processed by the local application using the installed computer vision libraries.
- Screenshot capture saves an image of the computer screen, which may contain private information.
- Review the screenshot destination and protect any captured files before sharing them.
- The current demo should not be used as a reliable gender classifier or as a replacement for professional accessibility tools.

## Contributing

Suggestions, bug reports, and contributions are welcome. If you would like to contribute, open an issue describing the proposed improvement or submit a pull request with a clear explanation of the changes.

## Project Status

**Status: Demo / Early Prototype**

GestureX demonstrates the initial concept of controlling selected computer functions using hand gestures. The current implementation is intentionally limited, and future releases may introduce more advanced recognition, interaction, and accessibility features.

## Author

**Punit Goyal**

MCA Student | Python | Computer Vision | AI Projects

---

*GestureX is an experimental learning project. Its long-term vision is to explore more natural computer interaction and accessible communication through gesture-based technology.*