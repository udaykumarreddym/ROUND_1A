import re
from collections import Counter
from statistics import mode

def predict_headings(spans):

    def is_title_case(text):
        words = text.split()
        return all(w[0].isupper() for w in words if w and w[0].isalpha())

    def get_numbered_level(text):
        match = re.match(r"^\s*(\d+(\.\d+)*)(\.|\))?\s+", text)
        if not match:
            return None
        level = match.group(1).count('.') + 1
        return min(level, 3)

    def is_valid_heading(text):
        if not text or len(text.strip()) < 3:
            return False
        text = text.strip().rstrip(":")
        if re.match(r"^(Table|Figure|Appendix|Page)\s", text, re.I):
            return False
        if not any(c.isalpha() for c in text):  # skip numeric-only
            return False
        return True

    def get_font_ranks(spans):
        fonts = [s["normalized_font_size"] for s in spans]
        ranked = sorted(set(fonts), reverse=True)
        return ranked

    title = ""
    outline = []
    used_texts = set()
    max_font = max(s["normalized_font_size"] for s in spans)
    font_ranks = get_font_ranks(spans)

    # --- Title detection on first page ---
    page0_spans = [s for s in spans if s["page"] == 0]
    page0_spans = sorted(page0_spans, key=lambda x: x["top_margin"])

    merged_title_lines = []
    for s in page0_spans[:3]:
        text = s["text"].strip()
        if (
            s["normalized_font_size"] >= 0.95 * max_font and
            not text.isupper() and
            ":" not in text and
            len(text) <= 100 and
            (s["is_centered"] or s["is_bold"] or is_title_case(text))
        ):
            merged_title_lines.append(text)

    if merged_title_lines:
        title = " ".join(merged_title_lines)
        used_texts.update(merged_title_lines)

    h1_spans, h2_spans, h3_spans = [], [], []

    # Font size thresholds
    h1_font = font_ranks[1] if len(font_ranks) > 1 else font_ranks[0]
    h2_font = font_ranks[2] if len(font_ranks) > 2 else h1_font - 0.1
    h3_font_candidates = [f for f in font_ranks if f < h2_font]
    h3_font = h3_font_candidates[0] if h3_font_candidates else h2_font - 0.1

    FONT_TOL = 0.03  # Font tolerance (instead of ==)

    for s in spans:
        text = s["text"].strip()
        if text in used_texts or not text or len(text) > 120:
            continue

        num_level = get_numbered_level(text)
        indent = s.get("indentation", 0.0)
        font = s.get("normalized_font_size", 0.0)
        is_bold = s.get("is_bold", False)
        is_centered = s.get("is_centered", False)
        is_title = is_title_case(text)
        word_count = len(text.split())

    # --- H1 detection ---
        if (
            (num_level == 1 and is_valid_heading(text)) or
            (
            abs(font - h1_font) < FONT_TOL and
            is_valid_heading(text) and
            (
                (is_bold and is_centered) or
                (is_bold and indent < 0.2)
            )
            )
        ):
            h1_spans.append({"level": "H1", "text": text, "page": s["page"]})
            used_texts.add(text)
            continue

    # --- H2 detection ---
        if (
        (num_level == 2 and is_valid_heading(text)) or
        (
            abs(font - h2_font) < FONT_TOL and
            is_valid_heading(text) and
            (
                (is_bold and indent < 0.3) or
                (word_count <= 4 and is_title and font > 0.7)
            )
        )
        ):
            h2_spans.append({"level": "H2", "text": text, "page": s["page"]})
            used_texts.add(text)
            continue

    # --- H3 detection ---
        if (
            (num_level == 3 and word_count <= 10 and is_valid_heading(text)) or
            (
            abs(font - h3_font) < FONT_TOL and
            word_count <= 10 and
            is_valid_heading(text) and
            (
                indent > 0.15 or
                re.match(r"^\s*\d+\.\d+\.\d+(\.|:|\))?\s+", text)
            ) and
            (is_bold or is_title)
        )
        ):
            h3_spans.append({"level": "H3", "text": text, "page": s["page"]})
            used_texts.add(text)
            continue

    # --- UNNUMBERED SINGLE-WORD HEADING as H2 ---
        if (
        word_count <= 3 and
        is_valid_heading(text) and
        is_bold and font >= 0.7 and indent < 0.2 and
        text.lower() not in used_texts
        ):
            h2_spans.append({"level": "H2", "text": text, "page": s["page"]})
            used_texts.add(text)

            
    outline = h1_spans + h2_spans + h3_spans
    outline.sort(key=lambda x: (x["page"], x["text"]))

    return title.strip(), outline
