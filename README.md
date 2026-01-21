# CV Basic Image Capture

A Flask-based web application for capturing and streaming video from multiple IP cameras simultaneously.

## Result

![Camera Capture Result](pic_2.png)

Successfully connected to 2 IP cameras at the ACLAB Makerspace, streaming both feeds in real-time through a web interface.

## Requirements

- Python 3.8+
- OpenCV
- Flask

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HwanNorm/CV-Basic-Image-Capture.git
cd CV-Basic-Image-Capture
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open browser and go to: http://127.0.0.1:5000

3. Connect to cameras:
   - **For IP cameras (RTSP):** Enter the RTSP URL in the input field
   - **For local webcam:** Enter `0` (or `1` for second webcam)

4. Click **Connect** to start the video stream

5. Click the camera icon to capture and process images

## Connecting to ACLAB Cameras

To replicate the setup at FUV Makerspace:

1. Connect to the **ACLAB** WiFi network

2. Enter the following RTSP URLs:
   - **Camera 1:** `rtsp://admin:ACLAB2023@192.168.8.105:554/Streaming/channels/101`
   - **Camera 2:** `rtsp://admin:ACLAB2023@192.168.8.106:554/Streaming/channels/101`

3. Click **Connect** for each camera

## Camera Source Formats

| Type | Format | Example |
|------|--------|---------|
| RTSP | `rtsp://user:pass@ip:port/path` | `rtsp://admin:password@192.168.1.100:554/Streaming/channels/101` |
| HTTP | `http://ip:port/path` | `http://192.168.1.100:8080/video` |
| Webcam | `0`, `1`, etc. | `0` (default camera) |

## Project Structure

```
CV-Basic-Image-Capture/
├── app.py              # Flask web server & routes
├── camera.py           # Video camera handler (threading)
├── process.py          # Image processing
├── templates/
│   └── index.html      # Web interface
├── static/
│   ├── main.js         # Frontend JavaScript
│   └── style.css       # Styling
├── CapturedImage/      # Saved captures
└── requirements.txt    # Dependencies
```

## Author

HwanNorm - Fulbright University Vietnam, Spring 2026
