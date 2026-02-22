import cv2
from PIL import Image
import pytesseract

# 1️⃣ Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 2️⃣ Path to your sample video
video_path = "triangle_v.mp4"  # replace with your video file

# 3️⃣ Open video
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 4️⃣ Choose frames to test (every 5 seconds)
interval_sec = 2
frame_step = int(fps * interval_sec)

print(f"Total frames: {total_frames}, FPS: {fps}, Testing every {interval_sec}s")

# 5️⃣ Extract OCR from selected frames
for frame_idx in range(0, total_frames, frame_step):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(gray)

    # OCR
    text = pytesseract.image_to_string(pil_img).strip()
    timestamp = frame_idx / fps

    print(f"\n[Frame at {timestamp:.1f}s] Extracted Text:\n{text}\n{'-'*40}")

cap.release()
print("✅ OCR test complete!")