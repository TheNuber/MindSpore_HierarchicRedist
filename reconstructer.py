#!/usr/bin/env python3

import argparse
from pathlib import Path


def join_chunks(chunks_dir: Path, output_file: Path):
    chunks = sorted(
        chunks_dir.glob("*.part*"),
        key=lambda path: int(path.name.rsplit(".part", 1)[1])
    )

    if not chunks:
        raise FileNotFoundError(
            f"No chunk files found in: {chunks_dir}"
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("wb") as destination:
        for chunk in chunks:
            print(f"Adding: {chunk}")

            with chunk.open("rb") as source:
                while True:
                    data = source.read(1024 * 1024)  # 1 MB at a time

                    if not data:
                        break

                    destination.write(data)

    print(f"\nDone. Reconstructed file: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Join file chunks back together in order."
    )

    parser.add_argument("chunks_dir", type=Path)
    parser.add_argument("output_file", type=Path)

    args = parser.parse_args()

    join_chunks(args.chunks_dir, args.output_file)


if __name__ == "__main__":
    main()
