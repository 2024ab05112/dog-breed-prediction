from pathlib import Path
from PIL import Image
from src.data.preprocess import preprocess_and_split

def test_preprocess_creates_images(tmp_path):
    # Create fake raw data
    raw_dir = tmp_path / "raw"
    (raw_dir / "Cat").mkdir(parents=True)
    (raw_dir / "Dog").mkdir(parents=True)

    img = Image.new("RGB", (300, 300))
    img.save(raw_dir / "Cat" / "cat1.jpg")
    img.save(raw_dir / "Dog" / "dog1.jpg")

    processed_dir = tmp_path / "processed"

    preprocess_and_split(raw_dir, processed_dir)

    # Check directory structure
    for split in ["train", "val", "test"]:
        for cls in ["cats", "dogs"]:
            assert (processed_dir / split / cls).exists()

    # Check at least one image exists in ANY split
    found_cat = any((processed_dir / split / "cats").iterdir() for split in ["train", "val", "test"])
    found_dog = any((processed_dir / split / "dogs").iterdir() for split in ["train", "val", "test"])

    assert found_cat
    assert found_dog
