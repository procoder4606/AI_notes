import sys
import os
from transcriber import transcribe_audio
from notes_generator import generate_notes
from ocr import extract_ocr_text  # Import your OCR function

def main(video_or_audio_path):
    # 1. Check if the file is a video (for OCR) or just audio
    is_video = video_or_audio_path.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))

    print("[1/4] Processing input source...")
    
    # 2. Get OCR Text (if video)
    ocr_content = ""
    if is_video:
        print("🎥 Video detected. Extracting on-screen text...")
        ocr_content = extract_ocr_text(video_or_audio_path, interval_sec=10)
    
    # 3. Get Audio Transcript
    # (Note: If your transcriber requires mp3, you'll need an audio_extractor step)
    print("[2/4] Transcribing audio...")
    transcript = transcribe_audio(video_or_audio_path)

    # 4. Merge Content for the AI
    print("[3/4] Merging content and generating notes...")
    combined_data = f"""
    --- TRANSCRIPT ---
    {transcript}
    
    --- ON-SCREEN TEXT (OCR) ---
    {ocr_content}
    """

    # 5. Generate Notes using your OpenRouter/Gemini logic
    notes = generate_notes(combined_data)

    with open("notes.txt", "w", encoding="utf-8") as f:
        f.write(notes)

    print(f"✅ Process complete! Notes saved to notes.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_video_or_audio>")
    else:
        main(sys.argv[1])