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

