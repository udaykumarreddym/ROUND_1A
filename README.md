# 📄 Round 1A — Understand Your Document

> **Hackathon Theme:** *Connecting the Dots Through Docs*  
> **👤 Team:** Solo — Uday Kumar Reddy  
> **🎯 Track:** Document Structure Extraction  
> **🧠 Language:** Python 3.10  
> **🐳 Deployment:** Docker (AMD64, CPU-only, Offline)

---

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen)
![Offline](https://img.shields.io/badge/Network-Offline-lightgrey)
![Model Size](https://img.shields.io/badge/Model-None--Used-green)

---

## 🧠 Objective

This project extracts a clean **hierarchical outline** from PDFs:

- 📌 **Title**
- 📑 **Headings**: `H1`, `H2`, `H3` with **page numbers**

The output enables smarter document experiences like:

- 🔍 Semantic Search  
- 🧠 Insight Generation  
- 📄 Document Summarization

---

## 🧱 Architecture Overview

```bash
📂 round_1A/
├── input/                    # Input PDFs (mounted by Docker)
├── output/                   # Output JSON files (mounted by Docker)
├── src/
│   ├── main.py                     # Entry point — batch processor
│   ├── extract_spans_from_pdf.py  # Layout + span extraction
│   ├── heading_detector.py        # Rule-based heading classifier
│   ├── output_formatter.py        # JSON formatter
├── requirements.txt
└── Dockerfile
```

⚙️ Pipeline Summary
<details> <summary>📥 <strong>Text Span Extraction</strong> (click to expand)</summary>
Uses PyMuPDF to parse text spans.

Captures layout metadata:

Normalized font size

Bold / Italic styling

Center alignment

Indentation

Position on page

Filters out:

Tables

Page numbers

Dates / Footers / Headers

</details> <details> <summary>🔍 <strong>Heading Detection (Rule-Based)</strong> (click to expand)</summary>
Classifies spans into: Title, H1, H2, H3

Key signals used:

Font rank and size tolerance

Heading numbering (e.g., 1., 2.1.3)

Formatting cues: Bold, Centered, Title Case

Indentation and top margin heuristics

Handles edge cases:

Short unnumbered headings (Summary, Background)

Mixed layout formatting (e.g., left-aligned + bold)

</details> <details> <summary>📦 <strong>JSON Structuring</strong> (click to expand)</summary>
Deduplicates entries

Sorts by page and text order

Outputs valid JSON in the format
</details>

🐳 Docker Usage
✅ Build the Docker Image
```bash
docker build --platform linux/amd64 -t mysolution:round1a .
```
▶️ Run the Container
```bash
docker run --rm \
-v $(pwd)/input:/app/input \
-v $(pwd)/output:/app/output \
--network none \
mysolution:round1a
```
✅ All PDFs in /input will be processed and corresponding .json files will be saved in /output.

✅ Constraint Compliance
Constraint	Status
📦 Model size ≤ 200MB	✅ No ML model used
⏱️ Runtime ≤ 10s for 50-page PDF	✅ Fast performance
🌐 No internet calls	✅ Fully offline
🖥️ Platform: AMD64, CPU-only	✅ Docker compliant
📁 Volumes: /input, /output	✅ Correctly mounted

📚 Dependencies
requirements.txt
```
pymupdf
numpy
pandas
```

🧠 Design Rationale
✅ Rule-based, deterministic logic — reliable, lightweight, and interpretable

🧠 Uses visual layout + text formatting cues for robust classification

💡 Carefully handles real-world edge cases:

Short standalone headings

Multi-line titles

Inconsistent font usage

🔧 Modular design — easy to plug in a model later (e.g., for Round 1B)

🧪 Testing
Tested against:

✅ Simple academic papers

✅ Deeply nested technical PDFs

✅ PDFs with nonstandard layout or font usage

➡️ Accuracy verified against the sample ground truth output.

🙌 Author

Uday Kumar Reddy

Rukmangar

B.Tech, 3rd Year — Computer Science (Data Science)

