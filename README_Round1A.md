# Round 1A – PDF Outline Extractor

This project extracts a structured outline (headings hierarchy) from PDF documents using PyMuPDF. It detects headings based on font size, boldness, and capitalization, then outputs the result in JSON format.

## 📂 Project Structure

```
Round1A/
├── app/
│   └── main.py              # Main script to extract PDF outlines
├── input/                   # Place your input PDF files here
├── output/                  # JSON output will be saved here
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker setup to run the script
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

## 🚀 How to Run

### Option 1: With Python (No Docker)

1. **Create virtual environment (optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script**:
   - Place PDF files inside the `input/` folder
   - Run:
     ```bash
     python app/main.py
     ```
   - Output will be saved as JSON in the `output/` folder

---

### Option 2: Using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t adobe-outline:latest .
   ```

2. **Run the container**:
   ```bash
   docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" adobe-outline:latest
   ```

> On Windows PowerShell use:
> ```powershell
> docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" adobe-outline:latest
> ```

---

## 📄 Output Format

Each PDF is converted to a JSON file with this structure:

```json
{
  "title": "sample.pdf",
  "outline": [
    {
      "level": "H1",
      "text": "INTRODUCTION TO AI",
      "page": 1
    }
  ]
}
```

## 🧠 Heading Detection Logic

- **Font Size**: Larger text is more likely to be a heading
- **Bold Font**: Adds to heading score
- **ALL CAPS**: Treated as a strong indicator
- **Scoring**: Combines the above to classify as H1, H2, or H3

---

## 📦 Dependencies

- Python 3.8+
- PyMuPDF (`pip install pymupdf`)

---

## 👤 Author

- Name: *Your Name Here*
- Institute: *Your College*
- Round: 1A – Adobe Challenge