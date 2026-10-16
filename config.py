"""Configuration constants for hand gesture control."""
import os
import ctypes

# System metrics
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
SYS_W, SYS_H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Camera settings
CAM_INDEX = 0

# Model path for MediaPipe hand landmarker
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

# Active zone size (as fraction of frame dimensions)
ACTIVE_W = 0.50
ACTIVE_H = 0.40

# Gesture thresholds (normalized distance / palm size)
PINCH_CLICK = 0.20
PINCH_RELEASE = 0.28
STABILIZER_TRIGGER = 0.40

# Cursor smoothing factors (0.0 = instant, 1.0 = no movement)
SMOOTH_FAST = 0.15
SMOOTH_SLOW = 0.92

# Scroll gesture parameters
SCROLL_SENSITIVITY = 3.0
SCROLL_DEADZONE = 4.0

# Video capture settings
CAP_WIDTH = 1280
CAP_HEIGHT = 720
CAP_FPS = 60

# UI display settings
DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540
