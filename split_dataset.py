import os
import shutil
import random

# ── Configuration ────────────────────────────────────────────────────────────────
RAW_DIR     = "dataset/images"    # raw images downloaded per class
DEST_DIR    = "dataset"           # will create train/ and val/ under here
CLASSES     = ["spoon", "cup", "plate"]
TRAIN_SPLIT = 0.8                 # 80% train, 20% val
SEED        = 42                  # for reproducible shuffling

random.seed(SEED)

# ── Create target folders ────────────────────────────────────────────────────────
for subset in ["train", "val"]:
    for folder in ["images", "labels"]:
        for cls in CLASSES:
            dirpath = os.path.join(DEST_DIR, subset, folder, cls)
            os.makedirs(dirpath, exist_ok=True)

# ── Split files ──────────────────────────────────────────────────────────────────
for cls in CLASSES:
    src_cls_dir = os.path.join(RAW_DIR, cls)
    all_files = [
        f for f in os.listdir(src_cls_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    random.shuffle(all_files)

    split_idx = int(len(all_files) * TRAIN_SPLIT)
    train_files = all_files[:split_idx]
    val_files   = all_files[split_idx:]

    # Copy images
    for fname in train_files:
        shutil.copy2(
            os.path.join(src_cls_dir, fname),
            os.path.join(DEST_DIR, "train", "images", cls, fname)
        )
    for fname in val_files:
        shutil.copy2(
            os.path.join(src_cls_dir, fname),
            os.path.join(DEST_DIR, "val", "images", cls, fname)
        )

    # (Labels will be created by LabelImg into the matching labels/ folders)
    print(f"{cls}: {len(train_files)} train, {len(val_files)} val")

print("\nDataset split complete!")
