import cv2
from PIL import Image
import pytesseract
from fpdf import FPDF

# --- CONFIG ---
video_path = "triangle_v.mp4"
pdf_output = "ocr_unique_frames.pdf"

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Open video
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Total frames: {total_frames}, FPS: {fps}")

# Prepare PDF
pdf = FPDF()
pdf.add_page()

# Unicode font
font_path = r"C:\Windows\Fonts\ARIAL.TTF"  # make sure this exists
pdf.add_font('ArialUni', '', font_path, uni=True)
pdf.set_font("ArialUni", size=12)

# Extract keyframes (I-frames) directly using OpenCV
last_text = ""
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Check if frame is a keyframe using OpenCV property
    is_keyframe = cap.get(cv2.CAP_PROP_POS_FRAMES) % int(fps) == 0  # simple approx for demo
    if not is_keyframe:
        frame_idx += 1
        continue

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(gray)

    # OCR
    text = pytesseract.image_to_string(pil_img).strip()
    timestamp = frame_idx / fps

    if text and text != last_text:
        pdf.multi_cell(0, 8, f"[Time: {timestamp:.1f}s]\n{text}\n{'-'*50}\n")
        last_text = text

    frame_idx += 1

cap.release()

# Save PDF
pdf.output(pdf_output)
print(f"✅ OCR PDF generated: {pdf_output}")