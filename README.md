🎮 Free Fire Outfit Image API

👑 Owner: Rakibul

---

🚀 Overview

This API generates a Free Fire outfit image using a player UID.
It fetches player data, extracts equipped outfit items, downloads their icons, and places them on a custom background.

---

🔗 API Endpoint

http://127.0.0.1:5000/outfit-image?uid=PLAYER_UID&key=KALLU07

---

📥 Parameters

Parameter| Type| Required| Description
"uid"| string| ✅| Free Fire Player UID
"key"| string| ✅| API Key ("KALLU07")

---

✅ Example Request

http://127.0.0.1:5000/outfit-image?uid=7255834728&key=KALLU07

---

📤 Response

- Returns a PNG image
- Outfit icons placed on background

---

⚙️ Installation

1. Clone Repository

git clone https://github.com/your-username/outfit-api.git
cd outfit-api

2. Install Dependencies

pip install -r requirements.txt

Or manually:

pip install flask requests pillow

---

▶️ Run Server

python app.py

Server will start on:

http://127.0.0.1:5000

---

📁 Project Structure

OUTFIT-API/
│── app.py
│── outfit.png
│── requirements.txt
│── vercel.json

---

🧠 How It Works

1. Takes UID from user
2. Fetches player data from API
3. Extracts "equippedSkills" (outfit IDs)
4. Downloads images from icon API
5. Pastes them on background
6. Returns final PNG image

---

🔑 API Key

Default:

KALLU07

You can change it in "app.py":

API_KEY = "YOUR_KEY"

---

🌐 Make Public API (Ngrok)

./ngrok http 5000

Example:

https://abcd1234.ngrok-free.app/outfit-image?uid=7255834728&key=KALLU07

---

⚠️ Notes

- Make sure "outfit.png" exists in same folder
- Works best with stable internet
- For production use Gunicorn or hosting (Render, Railway)

---

💡 Features

- Fast image processing (ThreadPool)
- Dynamic outfit rendering
- API key protection
- Lightweight & efficient

---

📌 Credits

- Developed by: Rakibul
- Inspired by Free Fire community tools

---

❤️ Support

If you like this project, give it a ⭐ on GitHub!

---