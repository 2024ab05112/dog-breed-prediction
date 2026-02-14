import os
import random
from pathlib import Path
from PIL import Image
from tqdm import tqdm

IMG_SIZE = (224, 224)
SPLITS = {"train": 0.8, "val": 0.1, "test": 0.1}

RAW_CLASS_MAP = {
    "Cat": "cats",
    "Dog": "dogs"
}

def preprocess_and_split(raw_dir, processed_dir):
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)

    for split in SPLITS:
        for cls in ["cats", "dogs"]:
            os.makedirs(processed_dir / split / cls, exist_ok=True)

    for raw_cls, out_cls in RAW_CLASS_MAP.items():
        images = list((raw_dir / raw_cls).glob("*.jpg"))
        random.shuffle(images)

        n_total = len(images)
        n_train = int(n_total * SPLITS["train"])
        n_val = int(n_total * SPLITS["val"])

        split_map = {
            "train": images[:n_train],
            "val": images[n_train:n_train + n_val],
            "test": images[n_train + n_val:]
        }

        for split, split_imgs in split_map.items():
            for img_path in tqdm(split_imgs, desc=f"{raw_cls} → {split}"):
                try:
                    img = Image.open(img_path).convert("RGB")
                    img = img.resize(IMG_SIZE)
                    img.save(processed_dir / split / out_cls / img_path.name)
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")

if __name__ == "__main__":
    preprocess_and_split(
        raw_dir="data/raw",
        processed_dir="data/processed"
    )
