import cv2
from PIL import Image
import pytesseract
from fpdf import FPDF
import os

# 1️⃣ Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 2️⃣ Path to your video
video_path = "triangle_v.mp4"  # replace with your video file

# 3️⃣ Open video
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 4️⃣ Frame interval
interval_sec = 2
frame_step = int(fps * interval_sec)

print(f"Total frames: {total_frames}, FPS: {fps}, Testing every {interval_sec}s")

# 5️⃣ Prepare PDF
pdf = FPDF()
pdf.add_page()

# Use Arial Unicode font
font_path = r"C:\Windows\Fonts\ARIAL.TTF"  # make sure this file exists
pdf.add_font('ArialUni', '', font_path, uni=True)
pdf.set_font("ArialUni", size=12)

# 6️⃣ Extract OCR and add to PDF
last_text = ""
for frame_idx in range(0, total_frames, frame_step):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret:
        break

    # Grayscale for OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(gray)

    # OCR
    text = pytesseract.image_to_string(pil_img).strip()
    timestamp = frame_idx / fps

    # Only add non-empty, unique text
    if text and text != last_text:
        pdf.multi_cell(0, 8, f"[Time: {timestamp:.1f}s]\n{text}\n{'-'*50}\n")
        last_text = text

cap.release()

# 7️⃣ Save PDF
pdf_output = "ocr_unique_frames.pdf"
pdf.output(pdf_output)
print(f"✅ OCR PDF generated: {pdf_output}")