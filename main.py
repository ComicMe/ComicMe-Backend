from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STABILITY_AI_KEY = os.getenv("STABILITY_AI_KEY")

# Initialize Flask app
app = Flask(__name__)

# AI Image Generation Route
@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "Default comic scene")
    width, height = 1024, 1024

    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    headers = {
        "Authorization": f"Bearer {STABILITY_AI_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt, "width": width, "height": height}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify({"image_url": response.json().get("image_url")})
    return jsonify({"error": response.text}), 400

if __name__ == "__main__":
    app.run(debug=True)
