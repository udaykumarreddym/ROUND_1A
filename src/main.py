import os
from extract_spans_from_pdf import extract_spans_from_pdf
from heading_detector import predict_headings
from output_formatter import save_output_json

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def process_pdf(pdf_path, output_path):
    spans = extract_spans_from_pdf(pdf_path)
    title, outline = predict_headings(spans)
    save_output_json(title, outline, output_path)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".pdf"):
            in_path = os.path.join(INPUT_DIR, file)
            out_path = os.path.join(OUTPUT_DIR, file.replace(".pdf", ".json"))
            process_pdf(in_path, out_path)

if __name__ == "__main__":
    main()
