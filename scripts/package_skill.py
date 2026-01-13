#!/usr/bin/env python3

import os
import zipfile
import sys
from pathlib import Path

def package_skill(skill_path, output_path):
    """
    Package the skill directory into a .skill file (which is a zip archive)
    """
    skill_path = Path(skill_path)
    output_path = Path(output_path)

    print(f"Packaging Lead-Insight-Parser skill from {skill_path} to {output_path}")

    # Create the zip file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the skill directory
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                # Add file to zip with relative path from skill directory
                arc_path = file_path.relative_to(skill_path)
                zipf.write(file_path, f"lead-insight-parser-skill/{arc_path}")

    print(f"Lead-Insight-Parser skill successfully packaged as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        skill_dir = Path(__file__).parent.parent  # lead-insight-parser-skill directory
        output_file = Path.cwd() / "lead-insight-parser.skill"
    else:
        skill_dir = Path(sys.argv[1])
        output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd() / "lead-insight-parser.skill"

    package_skill(skill_dir, output_file)