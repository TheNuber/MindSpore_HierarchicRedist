#!/usr/bin/env python3

import argparse
from pathlib import Path

# Keep the chunk strictly below 99 MB.
CHUNK_SIZE = 99 * 1024 * 1024 - 1


def split_file(input_file: Path, output_dir: Path):
    if not input_file.is_file():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with input_file.open("rb") as source:
        chunk_number = 1

        while True:
            data = source.read(CHUNK_SIZE)

            if not data:
                break

            chunk_name = f"{input_file.name}.part{chunk_number:06d}"
            chunk_path = output_dir / chunk_name

            with chunk_path.open("wb") as chunk:
                chunk.write(data)

            print(f"Created: {chunk_path} ({len(data):,} bytes)")
            chunk_number += 1

    print(f"\nDone. Created {chunk_number - 1} chunk(s).")


def main():
    parser = argparse.ArgumentParser(
        description="Split a file into chunks smaller than 99 MB."
    )

    parser.add_argument("input_file", type=Path)
    parser.add_argument("output_dir", type=Path)

    args = parser.parse_args()

    split_file(args.input_file, args.output_dir)


if __name__ == "__main__":
    main()
