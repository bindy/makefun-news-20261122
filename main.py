"""make.fun bounty: Sum up 22 November's world news in one image.

Entry program. No network, no randomness: it copies the pre-made
image bundled in this repository (entry.png, 1024x1024 PNG) to
/output/entry.png. Running it twice writes the same bytes.
"""
import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"Wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
