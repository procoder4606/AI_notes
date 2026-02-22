import cv2
import pytesseract
from PIL import Image
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor

# Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_single_frame(frame_data):
    """Worker function to process one frame and return text."""
    frame, timestamp = frame_data
    
    # Preprocessing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(gray)
    
    # OCR Extraction
    text = pytesseract.image_to_string(pil_img).strip()
    
    if text:
        return f"[Time: {timestamp:.1f}s]\n{text}"
    return None

def extract_ocr_text(video_path, interval_sec=10, max_workers=4):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step = int(fps * interval_sec)
    
    frames_to_process = []
    
    print(f"🎞️ Extracting frames from: {os.path.basename(video_path)}")
    # First, quickly grab the frames we need
    for frame_idx in range(0, total_frames, frame_step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        # Store frame and its timestamp
        frames_to_process.append((frame, frame_idx / fps))
    
    cap.release()

    print(f"🧠 Processing {len(frames_to_process)} frames with {max_workers} threads...")
    
    # Run the OCR in parallel
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # list() forces the tqdm bar to track the map progress
        results = list(tqdm(executor.map(process_single_frame, frames_to_process), 
                           total=len(frames_to_process), 
                           desc="OCR Scanning"))

    # Clean up None results and remove duplicates
    final_texts = []
    last_text = ""
    for text in results:
        if text and text != last_text:
            final_texts.append(text)
            last_text = text

    return "\n\n---\n\n".join(final_texts)