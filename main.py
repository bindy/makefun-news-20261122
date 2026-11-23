"""make.fun bounty: Sum up 22 November's world news in one image.

The entry program. It does no network calls and uses no randomness: it
copies the finished image shipped in this repository (entry.png, a
1024x1024 PNG) to /output/entry.png. Running it twice writes identical bytes.
"""
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    source = root / "entry.png"
    target_dir = Path("/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    target.write_bytes(source.read_bytes())
    print(f"Wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
