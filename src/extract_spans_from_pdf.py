import fitz  # PyMuPDF
import numpy as np
import re
from statistics import mode, StatisticsError

# --- Helpers ---
def is_title_case(text):
    words = text.split()
    return all(w[0].isupper() for w in words if w and w[0].isalpha())

def starts_with_number(text):
    return bool(re.match(r"^[1-9]\d{0,1}[\.\)]?\s", text.strip()))

def has_colon(text):
    return ":" in text

def count_dots(text):
    return text.count(".")

def is_centered(bbox, page_width):
    left, _, right, _ = bbox
    span_center = (left + right) / 2
    return abs(span_center - page_width / 2) < page_width * 0.05

def is_date_like(text):
    return re.search(
        r"\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b",
        text, re.IGNORECASE)

def is_page_number(text):
    return re.fullmatch(r"page\s*\d+", text.lower()) or re.fullmatch(r"\d{1,3}", text.strip())

# --- Main extractor ---
def extract_spans_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_font_sizes = []
    paragraph_units = []

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        
        # --- Start: Table Detection ---
        tables = page.find_tables()
        table_bboxes = [table.bbox for table in tables]
        # --- End: Table Detection ---

        blocks = page.get_text("dict")["blocks"]
        page_width = page.rect.width
        page_height = page.rect.height

        line_objects = []
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                # --- Start: Check if line is within any table bounding box ---
                line_bbox = fitz.Rect(line["bbox"])
                in_table = False
                for table_bbox in table_bboxes:
                    if line_bbox.intersects(table_bbox):
                        in_table = True
                        break
                if in_table:
                    continue
                # --- End: Check if line is within any table bounding box ---
                
                spans = line["spans"]
                line_text = " ".join(span["text"].strip() for span in spans if span["text"].strip())
                if not line_text:
                    continue
                if any(len(word) >= 15 for word in line_text.split()):
                    continue
                if is_date_like(line_text) or is_page_number(line_text):
                    continue
                line_y = line["bbox"][1]
                line_objects.append({
                    "text": line_text,
                    "spans": spans,
                    "y": line_y,
                    "page": page_index,
                    "page_width": page_width,
                    "page_height": page_height
                })
                for span in spans:
                    all_font_sizes.append(round(span["size"], 2))

        # --- Paragraph grouping ---
        line_objects.sort(key=lambda x: x["y"])
        last_y = None
        paragraph = []
        for line in line_objects:
            if last_y is not None and abs(line["y"] - last_y) > 15:
                if paragraph:
                    paragraph_units.append(paragraph)
                    paragraph = []
            paragraph.append(line)
            last_y = line["y"]
        if paragraph:
            paragraph_units.append(paragraph)

    if not all_font_sizes:
        raise ValueError("❌ No valid spans found in document")

    try:
        mode_font_size = mode(all_font_sizes)
    except StatisticsError:
        mode_font_size = np.mean(all_font_sizes)
    mean_font_size = np.mean(all_font_sizes)

    # --- Feature extraction per paragraph ---
    enriched_units = []
    for paragraph in paragraph_units:
        all_spans = [span for line in paragraph for span in line["spans"]]
        full_text = " ".join(line["text"] for line in paragraph).strip()
        if not full_text or len(full_text.replace(" ", "")) < 4:
            continue

        font_sizes = [round(span["size"], 2) for span in all_spans]
        font_names = [span.get("font", "") for span in all_spans]
        bboxes = [span["bbox"] for span in all_spans]

        avg_font_size = np.mean(font_sizes)
        font_name = max(set(font_names), key=font_names.count)
        bbox = bboxes[0]
        page = paragraph[0]["page"]
        page_width = paragraph[0]["page_width"]
        page_height = paragraph[0]["page_height"]

        enriched_units.append({
            "text": full_text,
            "normalized_font_size": round(avg_font_size / mode_font_size, 2),
            "is_bold": int(any("Bold" in name for name in font_names)),
            "is_italic": int(any("Italic" in name or "Oblique" in name for name in font_names)),
            "is_centered": int(is_centered(bbox, page_width)),
            "is_upper": int(full_text.isupper()),
            "is_title_case": int(is_title_case(full_text)),
            "starts_number": int(starts_with_number(full_text)),
            "char_count": len(full_text),
            "indentation": round(bbox[0] / page_width, 3),
            "has_dots": count_dots(full_text),
            "num_words": len(full_text.split()),
            "text_len": len(full_text),
            "position_in_page": round(bbox[1] / page_height, 3),
            "top_margin": round(bbox[1], 2),
            "line_height_ratio": round(avg_font_size / mean_font_size, 2),
            "font_name_len": len(font_name),
            "has_colon": int(has_colon(full_text)),
            "page": page
        })

    return enriched_units