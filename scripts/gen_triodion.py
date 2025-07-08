#!/usr/bin/env python3
import json
import argparse
import os
from pathlib import Path

def load_json_file(filepath):
    """Load and return JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}")
        return None

def load_translations(cal_file):
    """Load translations from cal.json file"""
    translations = load_json_file(cal_file)
    return translations if translations else {}

def create_md_file(output_dir, saint, feast_name_translated, num, lang, reading):
    """Create MD file with the specified format"""
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Create filename based on saint name (sanitized for filesystem)
    filename = f"{saint.replace(' ', '_').replace('/', '_')}.md"
    filepath = os.path.join(output_dir, filename)

    # MD file content
    content = f"""+++
draft = false
hidden = true
linkTitle = '{saint}'
description = '{feast_name_translated}'
weight = {num}
+++

{{{{% include file="content/{lang}/lives/{reading}.md" %}}}}
"""

    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created: {filepath}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate MD files from JSON data')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('lang', choices=['en', 'ru'], help='Language (en or ru)')
    parser.add_argument('--cal-file', default='cal.json', help='Translation file (default: cal.json)')
    parser.add_argument('--output-dir', default='output', help='Output directory (default: output)')

    args = parser.parse_args()

    # Load input JSON file
    input_data = load_json_file(args.input_file)
    if input_data is None:
        return 1

    # Load translations
    translations = load_translations(args.cal_file)

    # Process each structure in the JSON array
    num = 1
    processed_count = 0

    for item in input_data:
        # Check if date is empty and feastName is not None
        if item.get('date') == '' and item.get('feastName') is not None:
            saint = item.get('saint', '')
            feast_name = item.get('feastName', '')
            reading = item.get('reading', '')

            # Get translation for feastName, use original if not found
            feast_name_translated = translations.get(feast_name, feast_name)

            # Create MD file
            create_md_file(
                args.output_dir,
                saint,
                feast_name_translated,
                num,
                args.lang,
                reading
            )

            processed_count += 1
            num += 1

    print(f"\nProcessed {processed_count} items successfully.")
    return 0

if __name__ == '__main__':
    exit(main())
