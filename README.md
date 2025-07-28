# 📄 Round 1A — Understand Your Document

> **Track**: Document Structure Extraction  
> **Participant**: Uday Kumar Reddy , Rukmangar
> **Language**: Python 3.10  
> **Runtime**: Docker (CPU-only, Offline)  
> **Model Size**: None (Rule-based approach)

---

## 🧠 Approach

This solution extracts a structured outline from any PDF document — including the **Title**, and all major headings like **H1**, **H2**, and **H3**, along with their **page numbers**.

We followed a fully **rule-based approach**, optimized for offline execution, speed, and generalization across unknown documents.

### The pipeline consists of 3 stages:

1. **Text Span Extraction** (`extract_spans_from_pdf.py`)
   - Uses `PyMuPDF` to extract text along with layout features.
   - Computes normalized font size, bold/italic flags, indentation, and position within the page.
   - Skips tables, footers, page numbers, and invalid spans.

2. **Heading Detection** (`heading_detector.py`)
   - Applies heuristics to classify spans as Title, H1, H2, or H3.
   - Leverages:
     - Font ranking and tolerance
     - Numbering (e.g., `1.`, `2.3.1`)
     - Formatting cues: Bold, Centered, Title Case
     - Indentation and top margin
   - Supports unnumbered headings like “Background”, “Summary”.

3. **JSON Output Formatter** (`output_formatter.py`)
   - Removes duplicates.
   - Sorts output by page number and visual order.
   - Saves final output in the required structured JSON format.

---

## 📦 Models or Libraries Used

### ✅ No machine learning models were used.

Instead, the system relies entirely on visual-textual cues and hand-crafted logic.

### 🛠️ Python Libraries:

- [`PyMuPDF`](https://pymupdf.readthedocs.io/) — PDF parsing and layout extraction
- `numpy` — Feature aggregation
- `pandas` — Span processing and alignment
- `re`, `statistics`, `json` — Core Python libraries for text filtering, mode calculation, and output formatting

---

## 🐳 How to Build and Run (Documentation Only)

> ⚠️ While your solution will be run using the **"Expected Execution"** command by the judges, the steps below are provided for clarity.

### ✅ Step 1: Build Docker Image

```bash
docker build --platform linux/amd64 -t mysolution:round1a .
```

### ▶️ Step 2: Run the Container

```
docker run --rm \
-v $(pwd)/input:/app/input \
-v $(pwd)/output:/app/output \
--network none \
mysolution:round1a
```
This will:

Process all .pdf files in /input

Generate a matching .json file for each in /output using the required format

📌 Notes
No internet or external API calls used

Executes under 10 seconds for ≤ 50-page PDFs

Fully compatible with amd64, CPU-only systems

Easily extensible for multilingual or ML-based enhancement in Round 1B

🙌 Author

Uday Kumar Reddy

Rukmangar

B.Tech 3rd Year, CSE (Data Science)
