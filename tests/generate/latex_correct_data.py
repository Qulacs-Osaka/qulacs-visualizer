import os
import sys

from PIL import Image

from qulacsvis import circuit_drawer

sys.path.append(os.path.join("tests"))

from circuit_test_data import load_circuit_data  # noqa

OUTPUT_DIR = os.path.join("tests", "images", "latex")

if __name__ == "__main__":
    test_data = load_circuit_data()

    for name, circuit in test_data.items():
        img = circuit_drawer(circuit, "latex")
        if isinstance(img, Image.Image):
            img.save(os.path.join(OUTPUT_DIR, f"{name}.png"))
            print(f'Saved image to {os.path.join(OUTPUT_DIR, name + ".png")}')
        else:
            print("img is not an Image.Image", file=sys.stderr)
