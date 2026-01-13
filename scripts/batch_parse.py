#!/usr/bin/env python3

import os
import sys
import glob
from pathlib import Path

# Add the script directory to the path to import parse_lead
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

from parse_lead import generate_lead_report

def batch_process_inquiries(input_directory, output_directory=None):
    """Process multiple inquiry files in batch."""
    input_path = Path(input_directory)

    if output_directory is None:
        output_directory = input_path / "reports"

    output_path = Path(output_directory)
    output_path.mkdir(exist_ok=True)

    # Supported file extensions
    extensions = ['*.txt', '*.eml', '*.md']
    inquiry_files = []

    for ext in extensions:
        inquiry_files.extend(input_path.glob(ext))

    if not inquiry_files:
        print(f"No inquiry files found in {input_directory}")
        return

    print(f"Processing {len(inquiry_files)} inquiry files...")

    for i, inquiry_file in enumerate(inquiry_files, 1):
        print(f"Processing {i}/{len(inquiry_files)}: {inquiry_file.name}")

        # Read inquiry text
        with open(inquiry_file, 'r', encoding='utf-8') as f:
            inquiry_text = f.read()

        # Generate report filename
        report_name = f"Lead_Report_{inquiry_file.stem}_{i}.md"
        report_path = output_path / report_name

        # Generate lead report
        generate_lead_report(inquiry_text, str(report_path))

        print(f"  -> Report saved: {report_path.name}")

    print(f"\nBatch processing completed! Reports saved in: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: batch_parse.py <input_directory> [output_directory]")
        print("Processes all .txt, .eml, and .md files in the input directory")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist")
        sys.exit(1)

    batch_process_inquiries(input_dir, output_dir)

if __name__ == "__main__":
    main()