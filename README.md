📄 Round 1A — Understand Your Document
Hackathon Theme: Connecting the Dots Through Docs
Team: Solo — Uday Kumar Reddy
Track: Document Structure Extraction
Language: Python 3.10
Deployment: Docker (AMD64, CPU-only, Offline)

🧠 Objective
This project extracts a clean hierarchical outline from PDFs, comprising:
📌 Title
📑 Headings: H1, H2, H3 with associated page numbers
The output enables downstream tasks like semantic search, information retrieval, and document summarization — forming the foundation for later rounds.

🧱 Architecture Overview
📂 round_1A/
├── input/                  # Input PDFs (mounted by Docker)
├── output/                 # Output JSON files (mounted by Docker)
├── src/
│   ├── main.py             # Entry point — batch processor
│   ├── extract_spans_from_pdf.py   # Layout + span extraction
│   ├── heading_detector.py         # Rule-based heading classifier
│   ├── output_formatter.py         # JSON formatter
├── requirements.txt
└── Dockerfile

⚙️ Pipeline Summary
1. Text Span Extraction
  Uses PyMuPDF to parse text spans
  Captures layout metadata:
  Font size (normalized), bold, italic
  Indentation, center alignment
  Position on page
  Filtering: tables, page numbers, dates, noise
2. Heading Detection (Rule-Based)
  Classifies spans into: Title, H1, H2, H3
  Logic combines:
  Font rank and size tolerance
  Numbering hierarchy (e.g., 1., 2.1.3)
  Formatting clues (bold, centered, title case)
  Indentation and top-margin heuristics
  Handles unnumbered headings (Summary, Conclusion, etc.)
3. JSON Structuring
  Deduplicates headings
  Sorts by page and order of appearance
  Outputs clean JSON as per required format

🐳 Docker Usage
✅ Build
docker build --platform linux/amd64 -t mysolution:round1a .
▶️ Run
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolution:round1a

All .pdf files in /input are automatically processed.
Outputs saved as .json in /output with the same filename.

✅ Constraint Compliance
Requirement	Status
📦 Model size ≤ 200MB	✅ No models used (fully rule-based)
⏱️ Runtime ≤ 10s for 50-page PDF	✅ Yes (tested with margin)
🌐 Network-free operation	✅ Fully offline
🖥️ Platform: linux/amd64, CPU-only	✅ Yes (via --platform flag)
📁 Input/output volume mounts	✅ Compliant

📚 Dependencies
requirements.txt
pymupdf
numpy
pandas

🧠 Design Rationale
✅ Rule-based approach ensures portability, speed, and small size
🧠 Combines visual layout, font hierarchy, and text semantics
💡 Handles real-world edge cases:
Short headings without numbers
Overlapping font sizes
Mixed formatting (e.g., centered + bold)

🧪 Testing
Tested on:
✍️ Simple academic documents
📊 Technical PDFs with nested headings
⚠️ PDFs with missing or unordered font hierarchies
Passed accuracy checks using provided sample outputs.

📌 Notes
No AI model or training used — fully deterministic
Easy to extend for multilingual or semantic enhancements (for Round 1B)
Written for high interpretability and modularity

🙌 Author
Uday Kumar Reddy
Rukmangar
B.Tech, 3rd Year (CSE - Data Science)
