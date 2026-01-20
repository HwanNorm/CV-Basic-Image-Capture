import threading
import cv2
import time
# --- Video camera handler per camera ---
class VideoCamera:
    def __init__(self):
        self.source = None
        self.cap = None
        self.frame = None         # BGR numpy array
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def start(self, source):
        # nếu cùng source thì giữ nguyên
        if self.running and self.source == source:
            return
        # stop existing
        self.stop()
        self.source = source
        self.running = True
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        if self.cap:
            try:
                self.cap.release()
            except:
                pass
        self.cap = None
        self.thread = None
        self.frame = None

    def _reader(self):
        # try open source
        # Convert to int if it's a digit (for webcam index)
        source = self.source
        if isinstance(source, str) and source.isdigit():
            source = int(source)

        # For webcam (integer source), use default backend instead of FFMPEG
        if isinstance(source, int):
            self.cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)  # DirectShow for Windows
        else:
            try:
                self.cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            except:
                self.cap = cv2.VideoCapture(source)

        print(f"[Camera] Opened source={source}, isOpened={self.cap.isOpened() if self.cap else False}")
        # optional tune: set buffer size or transport
        # read loop
        while self.running:
            if not self.cap or not self.cap.isOpened():
                # try reopen every 2s
                print(f"[Camera] Not opened, retrying source={source}...")
                time.sleep(2)
                if isinstance(source, int):
                    self.cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
                else:
                    try:
                        self.cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
                    except:
                        self.cap = cv2.VideoCapture(source)
                continue
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print(f"[Camera] Failed to read frame, ret={ret}")
                time.sleep(0.05)
                continue
            print(f"[Camera] Got frame: {frame.shape}")
            with self.lock:
                self.frame = frame.copy()
            # small sleep to relinquish CPU
            time.sleep(0.02)
        # cleanup
        try:
            if self.cap:
                self.cap.release()
        except:
            pass
        self.cap = None

    def get_frame_jpeg(self):
        # return JPEG bytes of current frame, or None
        with self.lock:
            f = None if self.frame is None else self.frame.copy()
        if f is None:
            return None
        # encode as JPEG
        ret, jpeg = cv2.imencode('.jpg', f, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ret:
            return None
        return jpeg.tobytes()

    def get_frame_bgr(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def get_frame_bmp(self):
        # return BMP bytes of current frame, or None
        with self.lock:
            f = None if self.frame is None else self.frame.copy()
        if f is None:
            return None
        # encode as BMP
        ret, bmp = cv2.imencode('.bmp', f)
        if not ret:
            return None
        return bmp.tobytes()