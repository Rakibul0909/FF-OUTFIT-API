# SRC UPDATED BY GPT (5 IMAGE VERSION)

from flask import Flask, request, jsonify, send_file
import httpx
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import os

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)

API_KEY = "Dark-OXO"
BACKGROUND_FILENAME = "outfit1.png"
CANVAS_SIZE = (800, 800)
IMAGE_TIMEOUT = 8


# -------------------------------
# 🔹 FETCH PLAYER DATA (NEW API)
# -------------------------------
def fetch_player_info(uid: str):
    url = f"http://127.0.0.1:5001/player-info?uid={uid}"
    try:
        with httpx.Client(timeout=IMAGE_TIMEOUT) as client:
            r = client.get(url)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        print("API ERROR:", e)
        return None


# -------------------------------
# 🔹 FETCH IMAGE
# -------------------------------
def fetch_image(item_id, size=(150, 150)):
    try:
        url = f"https://iconapi.wasmer.app/{item_id}"
        with httpx.Client(timeout=IMAGE_TIMEOUT) as client:
            r = client.get(url)
            r.raise_for_status()

        img = Image.open(BytesIO(r.content)).convert("RGBA")
        return img.resize(size, Image.LANCZOS)

    except Exception as e:
        print("IMG ERROR:", item_id, e)
        return None


# -------------------------------
# 🔹 MAIN ROUTE
# -------------------------------
@app.route('/outfit-image', methods=['GET'])
def outfit_image():
    uid = request.args.get("uid")
    key = request.args.get("key")

    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401

    data = fetch_player_info(uid)
    if not data:
        return jsonify({"error": "Failed to fetch data"}), 500

    # -------------------------------
    # 🔹 EXTRACT DATA
    # -------------------------------
    basic = data.get("basicInfo", {})
    profile = data.get("profileInfo", {})
    pet = data.get("petInfo", {})

    weapon_ids = basic.get("weaponSkinShows", []) or []
    avatar_id = profile.get("avatarId")
    pet_skin = pet.get("skinId")

    # -------------------------------
    # 🔹 BUILD FINAL ID LIST
    # -------------------------------
    final_ids = []

    # 1️⃣ weapon skins
    final_ids.extend(weapon_ids)

    # 2️⃣ pet skin
    if pet_skin:
        final_ids.append(pet_skin)

    # 3️⃣ avatar
    if avatar_id:
        final_ids.append(avatar_id)

    # ✅ LIMIT TO 5 IMAGES
    final_ids = final_ids[:5]

    # -------------------------------
    # 🔹 LOAD BACKGROUND
    # -------------------------------
    bg_path = os.path.join(os.path.dirname(__file__), BACKGROUND_FILENAME)
    background = Image.open(bg_path).convert("RGBA")
    canvas = background.resize(CANVAS_SIZE)

    # -------------------------------
    # 🔹 5 POSITIONS (BALANCED)
    # -------------------------------
    positions = [
        (325, 63),    # top center
        (566, 230),   # right top
        (493, 520),   # right bottom
        (160, 510),   # left bottom
        (80, 200)    # left top
    ]

    size = (150, 150)

    # -------------------------------
    # 🔹 PARALLEL IMAGE FETCH
    # -------------------------------
    futures = []
    for item_id in final_ids:
        futures.append(executor.submit(fetch_image, item_id, size))

    # -------------------------------
    # 🔹 PASTE IMAGES
    # -------------------------------
    for i, future in enumerate(futures):
        if i >= len(positions):
            break

        img = future.result()
        if not img:
            continue

        x, y = positions[i]
        canvas.paste(img, (x, y), img)

    # -------------------------------
    # 🔹 OUTPUT
    # -------------------------------
    output = BytesIO()
    canvas.save(output, format="PNG")
    output.seek(0)

    return send_file(output, mimetype="image/png")


# -------------------------------
# 🔹 RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
