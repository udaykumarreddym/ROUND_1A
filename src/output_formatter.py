import json

def save_output_json(title, outline, output_path):
    seen = set()
    final_outline = []
    for item in outline:
        key = (item["text"],item["level"],  item["page"])
        if key not in seen:
            seen.add(key)
            final_outline.append(item)

    output = {
        "title": title,
        "outline": final_outline
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
