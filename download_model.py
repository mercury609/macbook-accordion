"""Fetch the official Demucs model and verify it against the tested artifact."""
from pathlib import Path
import hashlib
import tempfile
import urllib.request

URL = "https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/955717e8-8726e21a.th"
SHA256 = '8726e21a993978c7ba086d3872e7608d7d5bfca646ca4aca459ffda844faa8b4'

def main():
    target = Path(__file__).resolve().parent / "models" / "955717e8-8726e21a.th"
    target.parent.mkdir(exist_ok=True)
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == SHA256:
        print("Model already verified.")
        return
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".part", delete=False) as stream:
            temp = Path(stream.name)
            with urllib.request.urlopen(URL, timeout=90) as response:
                while chunk := response.read(1024 * 1024):
                    stream.write(chunk)
        if hashlib.sha256(temp.read_bytes()).hexdigest() != SHA256:
            raise RuntimeError("Model checksum mismatch; download was not installed.")
        temp.replace(target)
        print("Model downloaded and verified.")
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
