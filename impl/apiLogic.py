import time

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader
import json

API_URL_CREATE_TASK = "https://api.piapi.ai/api/v1/task"
API_URL = "https://api.piapi.ai/api/v1/task/"
API_KEY = "a9a0e96125d12a2b92f5f514e4d7bd5232ba8a946d557a8424dc30033470fa51"

cloudinary.config(cloud_name='daxepgo72', api_key='623398975615925', api_secret='IQM-yQkCaxSbXzQL-IlqvZJx2pU')


def image_url(file_to_upload):
    upload_result = cloudinary.uploader.upload(file_to_upload)
    url = upload_result["url"]
    if url.endswith(".webp"):
        url = url[:-5] + ".jpg"  # Remove '.webp' and add '.jpg'
    return url


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
            "aspect_ratio": "9:16",
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
        # response.raise_for_status()  # Raise an exception for HTTP errors
        # return jsonify(response.json())  # Forward the response back to the client
        result = response.json()  # Forward the response back to the client
        task_id = result['data']['task_id']
        print(task_id)
        print(result)
        url = f"{API_URL}{task_id}"
        # Define headers with the API key
        headers = {
            'x-api-key': API_KEY
        }

        # Make the GET request to the external API
        try:
            while True:
                # Make the GET request to the external API
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise exception for HTTP errors

                # Parse the response JSON
                response_data = response.json()
                print(response_data)
                # Check the status
                if response_data['data']['status'] == 'completed':
                    # Return the final output once the task is completed
                    return jsonify(response_data['data']['output']['video_url'])

                # Wait before sending the next request
                time.sleep(2)  # Adjust sleep time as per API rate limits
        except requests.exceptions.RequestException as e:
            # Handle errors and return a meaningful message
            return jsonify({"error": str(e)}), 500
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


def download_and_upload_image(product_code, image_url, api_endpoint):
    """
    Downloads an image from a given URL and uploads it to the specified API endpoint.

    Args:
        product_code (str): The product code.
        image_url (str): The URL of the image to be downloaded.
        api_endpoint (str): The URL of the API endpoint to upload the image.

    Returns:
        Response: The response from the API call.
    """
    try:
        # Download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses (e.g., 404, 500)

        # Save the image temporarily in memory
        image_file_name = f"{product_code}.jpg"  # You can adjust the file extension based on the image type
        image_file = (image_file_name, response.content, response.headers.get('Content-Type', 'image/jpeg'))

        # Prepare the data for the API request
        data = {
            "productCode": product_code,
            "imageFileName": image_file_name,
            "active": "true",  # Adjust this value based on your requirements
        }

        # Upload the image
        files = {"image": image_file}
        api_response = requests.post(api_endpoint, data=data, files=files)
        api_response.raise_for_status()  # Raise an error for bad responses

        return api_response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None