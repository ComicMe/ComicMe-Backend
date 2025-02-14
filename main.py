from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

STABILITY_AI_KEY = os.getenv("STABILITY_AI_KEY")

# AI Image Generation Route
@app.route("/generate-image", methods=["POST"])
def generate_image():
    # Ensure the request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 415

    data = request.get_json()
    prompt = data.get("prompt", "Default comic scene")
    width = data.get("width", 1024)
    height = data.get("height", 1024)

    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    
    headers = {
        "Authorization": f"Bearer {STABILITY_AI_KEY}",
        "Accept": "application/json"  # Set the Accept header to application/json
    }

    # Prepare the form-data payload
    files = {
        'prompt': (None, prompt),
        'width': (None, str(width)),
        'height': (None, str(height))
    }

    # Send the request as multipart/form-data
    response = requests.post(url, headers=headers, files=files)

    print("API Response:", response.json())
    
    if response.status_code == 200:
        return jsonify({"image_url": response.json().get("image_url")})
    
    return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)