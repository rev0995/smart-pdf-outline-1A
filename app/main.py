import fitz  # PyMuPDF
import os
import json

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = doc.metadata.get("title") or os.path.basename(pdf_path)
    raw_outline = []
    
    for page_index, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        # Track the block index on each page
        for block_index, block in enumerate(blocks):
            for line in block.get("lines", []):
                if not line.get("spans"):
                    continue

                # Combine all spans of a line
                merged_text = ""
                font_sizes = []
                is_bold = False
                is_caps = True
                for span in line["spans"]:
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    merged_text += " " + text
                    font_sizes.append(span.get("size", 0))
                    if not text.isupper():
                        is_caps = False
                    if "Bold" in span.get("font", "") or "Black" in span.get("font", ""):
                        is_bold = True
                merged_text = merged_text.strip()
                if len(merged_text) < 3:
                    continue

                # Determine heading level by font size, boldness, all-caps
                avg_font = sum(font_sizes) / len(font_sizes) if font_sizes else 0
                score = 0
                if avg_font >= 16:
                    score += 3
                elif avg_font >= 13:
                    score += 2
                elif avg_font >= 11:
                    score += 1
                if is_bold:
                    score += 1
                if is_caps:
                    score += 1

                if score >= 5:
                    level = "H1"
                elif score >= 3:
                    level = "H2"
                elif score >= 2:
                    level = "H3"
                else:
                    continue

                # Store page, level, text, and block index
                raw_outline.append({
                    "page": page_index + 1,
                    "level": level,
                    "text": merged_text,
                    "block": block_index
                })

    # Merge consecutive headings in the same page and block
    merged_outline = []
    buffer = None
    level_order = {"H1": 1, "H2": 2, "H3": 3}
    for item in raw_outline:
        if (buffer 
            and buffer["page"] == item["page"] 
            and buffer["block"] == item["block"]):
            # Combine texts of the same heading
            buffer["text"] += " " + item["text"]
            # Keep the higher-level heading (H1 > H2 > H3)
            if level_order[item["level"]] < level_order[buffer["level"]]:
                buffer["level"] = item["level"]
        else:
            if buffer:
                merged_outline.append(buffer)
            # Use a copy to avoid mutating original raw_outline entries
            buffer = item.copy()
    if buffer:
        merged_outline.append(buffer)

    # Remove the 'block' field for output
    final_outline = []
    for entry in merged_outline:
        final_outline.append({
            "level": entry["level"],
            "text": entry["text"],
            "page": entry["page"]
        })

    return {"title": title, "outline": final_outline}

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, output_filename)

            result = extract_outline(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
