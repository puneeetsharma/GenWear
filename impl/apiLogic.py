import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader
import json

API_URL_CREATE_TASK = "https://api.piapi.ai/api/v1/task"
API_URL = "https://api.piapi.ai/api/v1/task/"
API_KEY = "e2adc30848fb4497f5f496be2ab86f99cbed7e1c9e12c9382193521b692d4fa3"


def image_url(file_to_upload):
    upload_result = cloudinary.uploader.upload(file_to_upload)
    return upload_result["url"]


def generate_video_prompt(image_file, user_data):
    # Prepare payload for the external API

    if image_file:
        image = image_url(image_file)
    else:
        image = user_data.get("image")

    payload = {
        "model": "kling",
        "task_type": "video_generation",
        "input": {
            "prompt": user_data.get("prompt"),
            "negative_prompt": "",
            "cfg_scale": 0.5,
            "duration": 5,
            "aspect_ratio": "1:1",
            "image_url": image,
            "camera_control": {
                "type": "simple",
                "config": {
                    "horizontal": 0,
                    "vertical": 0,
                    "pan": -10,
                    "tilt": 0,
                    "roll": 0,
                    "zoom": 0
                }
            },
            "mode": "std"
        },
        "config": {
            "service_mode": "",
            "webhook_config": {
                "endpoint": "",
                "secret": ""
            }
        }
    }

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    # Call the external API
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return jsonify(response.json())  # Forward the response back to the client
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


def generate_image_with_image_and_return_image(request1, user_data):
    try:
        model_input_file = request1.files.get('model_input')
        upper_input_file = request1.files.get('upper_input')
        lower_input_file = request1.files.get('lower_input')

        if not model_input_file:
            return jsonify({"error": "'model_input' file is required"}), 400

        model_input_url = cloudinary.uploader.upload(model_input_file)['url']

        if 'dress_input' in request1.files:
            dress_input_file = request1.files.get('dress_input')
            dress_input_url = cloudinary.uploader.upload(dress_input_file)['url']
        else:
            if not upper_input_file or not lower_input_file:
                return jsonify({
                    "error": "'upper_input' and 'lower_input' files are required when 'dress_input' is not provided"}), 400
            upper_input_url = cloudinary.uploader.upload(upper_input_file)['url']
            lower_input_url = cloudinary.uploader.upload(lower_input_file)['url']
    except Exception as e:
        return jsonify({"error": f"File upload failed: {str(e)}"}), 500

    # Prepare payload for the external API
    payload = {
        "model_input": model_input_url,
        "batch_size": user_data.get("batch_size"),
    }

    if "dress_input" in user_data:
        payload["upper_input"] = dress_input_url
    else:
        if "upper_input" not in user_data or "lower_input" not in user_data:
            return jsonify(
                {"error": "'upper_input' and 'lower_input' are required when 'dress_input' is not provided"}), 400
        payload["upper_input"] = upper_input_url
        payload["lower_input"] = lower_input_url

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    # Call the external API
    try:
        response = requests.post(API_URL_CREATE_TASK, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()  # Forward the response back to the client
        task_id = result['data']['task_id']

        url = f"{API_URL}{task_id}"
        # Define headers with the API key
        headers = {
            'x-api-key': API_KEY
        }

        # Make the GET request to the external API
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Return the response from the API
            # return jsonify(response.json())
            return jsonify(response['data']['output']['works'][0]['image']['resource_without_watermark'])
        except requests.exceptions.RequestException as e:
            # Handle errors and return a meaningful message
            return jsonify({"error": str(e)}), 500


    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
