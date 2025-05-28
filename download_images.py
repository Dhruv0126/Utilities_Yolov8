import os
import requests

# ── Configuration ────────────────────────────────────────────────────────────────
API_KEY    = "50538385-c64398080f5f9db7cca7c84ed"  # ← your Pixabay API key
CLASSES    = ["spoon", "cup", "plate"]
PER_PAGE   = 200                     # Pixabay’s max per request
MAX_IMAGES = 300                     # images to download per class
BASE_DIR   = "dataset"               # root folder for your data

# ── Download loop ───────────────────────────────────────────────────────────────
for cls in CLASSES:
    out_dir = os.path.join(BASE_DIR, "images", cls)
    os.makedirs(out_dir, exist_ok=True)

    downloaded = 0
    page = 1

    print(f"\nDownloading {MAX_IMAGES} images of '{cls}' into {out_dir} ...")
    while downloaded < MAX_IMAGES:
        resp = requests.get(
            "https://pixabay.com/api/",
            params={
                "key": API_KEY,
                "q": cls,
                "image_type": "photo",
                "per_page": PER_PAGE,
                "page": page
            }
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
        if not hits:
            print(" ▶ No more results from API.")
            break

        for hit in hits:
            if downloaded >= MAX_IMAGES:
                break
            # choose largeImageURL for higher resolution
            url = hit["largeImageURL"]
            ext = os.path.splitext(url)[1] or ".jpg"
            filename = f"{cls}_{downloaded+1:03d}{ext}"
            path = os.path.join(out_dir, filename)

            # fetch and save
            img_data = requests.get(url).content
            with open(path, "wb") as f:
                f.write(img_data)

            downloaded += 1
            if downloaded % 50 == 0:
                print(f"  • {downloaded}/{MAX_IMAGES} downloaded")

        page += 1

    print(f"Finished '{cls}': {downloaded} images saved to {out_dir}")
