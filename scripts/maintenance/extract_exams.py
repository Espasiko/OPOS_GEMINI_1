import os
import sys
import glob
import json
import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    print(f"Reading {pdf_path}...")
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def analyze_difficulty(question_text):
    difficulty_score = 0
    if len(question_text) > 300: difficulty_score += 2
    if "EXCEPTO" in question_text or "SALVO" in question_text: difficulty_score += 2
    if "NO" in question_text and "CORRECTA" in question_text: difficulty_score += 1
    if "PLAZO" in question_text or "DÍAS" in question_text: difficulty_score += 1
    if "SILENCIO ADMINISTRATIVO" in question_text: difficulty_score += 2
    
    if difficulty_score >= 4: return "VERY HARD"
    if difficulty_score >= 2: return "HARD"
    return "MEDIUM"

def main():
    # Use WSL path as we are running in WSL python
    base_dir = "/mnt/e/1/OPOS_GEMINI_1/elemplos_leyes_info/de_mi_hija/bajados_academia"
    pdf_files = glob.glob(os.path.join(base_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {base_dir}")
        return

    print(f"Found {len(pdf_files)} PDFs. Analyzing difficulty across all files...")
    
    total_questions = 0
    hard_questions = 0
    readable_files = 0
    
    # Regex to find questions (starts with number and dot/dash, e.g., "1." or "1-")
    question_pattern = re.compile(r'^\d+[\.\-]\s+(.+?)(?=\n\d+[\.\-]\s+|\Z)', re.DOTALL | re.MULTILINE)
    
    for pdf_file in pdf_files:
        # Skip answer files for difficulty analysis of *questions* (though useful for context)
        if "respuestas" in os.path.basename(pdf_file).lower():
            continue
            
        text = extract_text_from_pdf(pdf_file)
        if not text.strip():
            continue # Skip unreadable files
            
        readable_files += 1
        matches = question_pattern.findall(text)
        
        file_hard_count = 0
        for match in matches:
            total_questions += 1
            difficulty = analyze_difficulty(match)
            if difficulty in ["HARD", "VERY HARD"]:
                hard_questions += 1
                file_hard_count += 1
        
        if matches:
            print(f"File: {os.path.basename(pdf_file)} - Questions: {len(matches)} - Hard: {file_hard_count} ({file_hard_count/len(matches):.1%})")

    if total_questions > 0:
        print(f"\n--- SUMMARY ---")
        print(f"Readable Exam Files: {readable_files}")
        print(f"Total Questions Analyzed: {total_questions}")
        print(f"Hard/Very Hard Questions: {hard_questions}")
        print(f"Difficulty Percentage: {hard_questions/total_questions:.1%}")
    else:
        print("\nNo questions extracted. Files might be scans or format not recognized.")

if __name__ == "__main__":
    main()
