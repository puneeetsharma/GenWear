import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Endpoint and Headers for Kling API
GENERATE_API_URL = "https://api.klingai.com/v1/images/generations"
FETCH_API_URL = "https://api.klingai.com/v1/images/generations/{task_id}"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY_HERE"  # Replace with your actual API key
}


@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Endpoint to generate images based on user input."""
    try:
        # Extract prompt, negative_prompt, and image from UI request
        user_input = request.json
        prompt = user_input.get("prompt")
        negative_prompt = user_input.get("negative_prompt")
        image = user_input.get("image")

        # Validate required fields
        if not prompt:
            return jsonify({"message": "Prompt is required"}), 400

        # Construct the full request body for Kling API
        request_body = {
            "model": "kling-v1",  # Optional, default is kling-v1
            "prompt": prompt,
            "negative_prompt": negative_prompt,  # Optional
            "image": image,  # Optional Base64 encoded image or image URL
            "image_fidelity": 0.7,  # Example value for image influence
            "n": 1,  # Number of images to generate
            "aspect_ratio": "16:9"  # Default aspect ratio
        }

        # Make the POST request to the Kling API
        response = requests.post(GENERATE_API_URL, headers=HEADERS, json=request_body)

        if response.status_code == 200:
            return jsonify({"message": "Image generation request successful!", "data": response.json()}), 200
        else:
            return jsonify({"message": "Request failed", "status_code": response.status_code,
                            "error": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@app.route('/fetch-image-status/<task_id>', methods=['GET'])
def fetch_image_status(task_id):
    """Endpoint to fetch the status of a single image generation task."""
    try:
        # Format the API URL with the task ID
        url = FETCH_API_URL.replace("{task_id}", task_id)

        # Make the GET request to the Kling API
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            return jsonify({"message": "Image generation task fetched successfully!", "data": response.json()}), 200
        else:
            return jsonify({"message": "Request failed", "status_code": response.status_code,
                            "error": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
