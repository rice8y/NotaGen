import sys
import os
import datetime
import subprocess
import argparse
from inference import inference_patch

def parse_args():
    parser = argparse.ArgumentParser(
        description="Genperiodte music using CLI options for period, composer, and instrumentation."
    )
    parser.add_argument(
        '--period', required=True,
        help="period (Ex: Baroque, Classical, Romantic)"
    )
    parser.add_argument(
        '--composer', required=True,
        help="Composer name (Ex: Bach, Johann Sebastian)"
    )
    parser.add_argument(
        '--instrumentation', required=True,
        help="Instrumentation (Ex: Chamber, Orchestral, Keyboard, etc.)"
    )
    args = parser.parse_args()
    return args.period, args.composer, args.instrumentation

def genperiodte_music(period, composer, instrumentation):
    abc_content = inference_patch(period, composer, instrumentation)
    return abc_content

def save_and_convert(abc_content, period, composer, instrumentation):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_str = f"{period}_{composer}_{instrumentation}"
    filename_base = f"{timestamp}_{prompt_str}"

    abc_filename = f"{filename_base}.abc"
    with open(abc_filename, "w", encoding="utf-8") as f:
        f.write(abc_content)

    xml_filename = f"{filename_base}.xml"
    try:
        subprocess.run(
            ["python", "abc2xml.py", "-o", ".", abc_filename],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Successfully saved: {abc_filename} -> {xml_filename}")
    except subprocess.CalledProcessError as e:
        error_msg = f"Conversion failed: {e.stderr}" if e.stderr else "Unknown error"
        print(error_msg)

if __name__ == "__main__":
    period, composer, instrumentation = parse_args()
    abc_content = genperiodte_music(period, composer, instrumentation)
    save_and_convert(abc_content, period, composer, instrumentation)
