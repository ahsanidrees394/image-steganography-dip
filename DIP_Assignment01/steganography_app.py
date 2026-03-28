import numpy as np
from PIL import Image
import argparse, os

def hide_image(cover_path, secret_path, output_path="stego_output.png"):
    if not os.path.exists(cover_path): raise FileNotFoundError(cover_path)
    if not os.path.exists(secret_path): raise FileNotFoundError(secret_path)
    cover  = Image.open(cover_path).convert("RGB")
    secret = Image.open(secret_path).convert("RGB")
    secret = secret.resize(cover.size, Image.LANCZOS)
    ca = np.array(cover, dtype=np.uint8)
    sa = np.array(secret, dtype=np.uint8)
    Image.fromarray((ca & 0xF0) | (sa >> 4)).save(output_path)
    print("[SUCCESS] Secret hidden. Output: " + output_path)

def reveal_image(stego_path, output_path="revealed_secret.png"):
    if not os.path.exists(stego_path): raise FileNotFoundError(stego_path)
    stego = Image.open(stego_path).convert("RGB")
    sa = np.array(stego, dtype=np.uint8)
    Image.fromarray((sa & 0x0F) << 4).save(output_path)
    print("[SUCCESS] Hidden image revealed. Output: " + output_path)

def main():
    parser = argparse.ArgumentParser(description="Image Steganography | Ahsan 235139")
    parser.add_argument("mode", choices=["hide","reveal"])
    parser.add_argument("--cover",  type=str)
    parser.add_argument("--secret", type=str)
    parser.add_argument("--stego",  type=str)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    if args.mode == "hide":
        hide_image(args.cover, args.secret, args.output or "stego_output.png")
    else:
        reveal_image(args.stego, args.output or "revealed_secret.png")

if __name__ == "__main__":
    main()
