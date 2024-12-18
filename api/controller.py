import time

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader
import json
from impl import apiLogic

app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=['POST'])
def upload_file():
    app.logger.info('in upload route')
    if request.method == 'POST':
        file_to_upload = request.files['image']
        app.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            app.logger.info(upload_result)
            return jsonify({"Image uploaded Successfully": upload_result["url"]})
        else:
            return jsonify({"Image uploaded Failed"})


cookies = {
    '__bwa_user_id': '723337755.U.1481629537580909.1703572604',
    '_fbp': 'fb.1.1703572603948.650712607',
    '_vwo_ssm': '1',
    '_vwo_uuid': 'D0FECF4DA90DB71E169FD408AF48C2A90',
    '_vwo_ds': '3%3Aa_0%2Ct_0%3A0%241703652856%3A32.60795595%3A%3A%3A%3A0',
    'USER_DATA': '%7B%22attributes%22%3A%5B%5D%2C%22subscribedToOldSdk%22%3Afalse%2C%22deviceUuid%22%3A%22803312bb-723b-4571-9cf2-0c2ce4a2364b%22%2C%22deviceAdded%22%3Afalse%7D',
    'SOFT_ASK_STATUS': '%7B%22actualValue%22%3A%22not%20shown%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D',
    'afUserId': 'b2fd01d5-ee60-4892-826c-4e1f309cbefb-p',
    'IR_PI': '887b3867-a93d-11ee-a8c3-71381190d436%7C1724762414228',
    '_ce.s': 'v~6fdd4d081a00e4acdb1d7ccd667d53720188d505~lcw~1725478809184~lva~1725478809184~vpv~14~lcw~1725478809184',
    'IR_gbd': 'gdn-app.com',
    '_gcl_au': '1.1.219426536.1727169294',
    'IR_19024': '1733396055062%7C4120732%7C1733396055062%7C%7C',
    '_ga_G3ZP2F3MW9': 'GS1.1.1733396055.17.0.1733396062.53.0.1303411168',
    'Partners-Device-Id': '2397160f-0240-49ea-a80d-a0e04daea2e9',
    'Partners-Username': 'searchdev@gdn-commerce.com',
    'Partners-User-Id': 'ed4b81f8-6580-48e6-ad89-46f4edada26e',
    'Partners-Signature': '95F9C422166EFC8B586B71430A932B9931885F11E1B1CFE730FCC88CC33EE4C2',
    'Blibli-Extras-MerchantId': 'DED-70077',
    '__cf_bm': 'GPtjjRJh48YkBY_gl2Ze9UzRQrxJWc6oTM7koyqsZKw-1734427528-1.0.1.1-t4aCPl16OCyo4.fxr5pa7.1wMnXRuv9WlnL8ZRG1nC58ijI90dcHsV_8euXQfO8j4jdCiNayGZLDxw5Pw2mF_g',
    '__bwa_session_id': '1734511390.4d31bb17-9c1a-43c6-ad6f-a827e3f7555b'
}


@app.route('/generate-product-code', methods=['GET'])
def generate_product_code():
    """
        Endpoint to call the external API to generate a product code.
        """
    url = "https://seller-qa2-gcp.gdn-app.com/backend/product-external/api/generators/generateProductCode"

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,en-GB;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://seller-qa2-gcp.gdn-app.com/external/CreateNewProduct',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    try:
        params = request.args.to_dict()
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500


TARGET_URL = 'https://seller-qa2-gcp.gdn-app.com/backend/product-external/api/images/upload'


@app.route('/upload-image', methods=['POST'])
def upload_image():
    try:
        # Extract fields from the incoming request
        image_file = request.files.get('image')
        image_file_name = request.form.get('imageFileName')
        product_code = request.form.get('productCode')
        active = request.form.get('active')

        if not image_file or not image_file_name or not product_code or active is None:
            return jsonify({"error": "Missing required fields"}), 400

        # URL for the external API
        url = 'https://seller-qa2-gcp.gdn-app.com/backend/product-external/api/images/upload'

        # General headers
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en,en-GB;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://seller-qa2-gcp.gdn-app.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://seller-qa2-gcp.gdn-app.com/external/CreateNewProduct',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        # Files and data payload
        files = {
            'image': (image_file.filename, image_file.stream, image_file.mimetype),
        }
        data = {
            'imageFileName': image_file_name,
            'productCode': product_code,
            'active': active,
        }

        # Make the request to the external API
        response = requests.post(url, headers=headers, cookies=cookies, files=files, data=data)
        print(response)
        # Return the response from the external API
        return jsonify({
            "status_code": response.status_code,
            "response": response.json() if response.headers.get(
                'Content-Type') == 'application/json' else response.text,
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_product', methods=['POST'])
def add_product():
    # Target URL
    url = "https://seller-qa2-gcp.gdn-app.com/backend/product-external/api/products/add?flowType=flow1"

    # Headers required for the cURL
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en,en-GB;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://seller-qa2-gcp.gdn-app.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://seller-qa2-gcp.gdn-app.com/external/CreateNewProduct",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    # cookies = {
    #     "__bwa_user_id": "723337755.U.1481629537580909.1703572604",
    #     "_fbp": "fb.1.1703572603948.650712607",
    #     "_vwo_ssm": "1",
    #     "_vwo_uuid": "D0FECF4DA90DB71E169FD408AF48C2A90",
    #     "__bwa_session_id": "1734427529.f2803e92-57c0-4718-ad80-f27d3516118b",
    #     "__bwa_session_action_sequence": "2",
    #     "JSESSIONID": "37EF6BEE093E6720ECCFCDE0F42C8D28",
    #     # Add other cookies as needed
    # }

    # Get the request payload from the client
    data = request.json

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, cookies=cookies, json=data)

        # Return the response from the external API
        return jsonify({
            "status": response.status_code,
            "data": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


API_URL_CREATE_TASK = "https://api.piapi.ai/api/v1/task"
API_URL = "https://api.piapi.ai/api/v1/task/"
API_KEY = "a9a0e96125d12a2b92f5f514e4d7bd5232ba8a946d557a8424dc30033470fa51"


@app.route('/try-on', methods=['POST'])
def ai_try_on():
    user_data = request.json

    # Validate required fields
    required_fields = ["model_input", "batch_size"]
    for field in required_fields:
        if field not in user_data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Prepare payload for the external API
    payload = {
        "model": "kling",
        "task_type": "ai_try_on",
        "input": {
            "model_input": user_data.get("model_input"),
            "batch_size": user_data.get("batch_size")
        }
    }
    if "dress_input" in user_data:
        payload["upper_input"] = user_data.get("dress_input")
    else:
        payload["input"]["lower_input"] = user_data.get("lower_input")

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    # Call the external API
    try:
        response = requests.post(API_URL_CREATE_TASK, headers=headers, data=json.dumps(payload))
        return jsonify(response.json())  # Forward the response back to the client
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


def image_url(file_to_upload):
    upload_result = cloudinary.uploader.upload(file_to_upload)
    url = upload_result["url"]
    if url.endswith(".webp"):
        url = url[:-5] + ".jpg"  # Remove '.webp' and add '.jpg'
    return url


@app.route('/try-on-with-image', methods=['POST'])
def ai_try_on_image():
    return jsonify("https://storage.midjourneyapi.xyz/images/200088786.png")
    global dress_input_url, upper_input_url, lower_input_url
    user_data = request.form  # Changed to form to handle file uploads

    # Upload files to Cloudinary
    try:
        model_input_file = request.files.get('model_input')
        upper_input_file = request.files.get('upper_input')
        lower_input_file = request.files.get('lower_input')
        dress_input_file = request.files.get('dress_input')

        if not model_input_file:
            return jsonify({"error": "'model_input' file is required"}), 400

        model_input_url = image_url(model_input_file)

        if 'dress_input' in request.files:
            dress_input_url = image_url(dress_input_file)
        elif upper_input_file and lower_input_file:
            upper_input_url = image_url(upper_input_file)
            lower_input_url = image_url(lower_input_file)
        elif upper_input_file:
            upper_input_url = image_url(upper_input_file)
        else:
            lower_input_url = image_url(lower_input_file)

    except Exception as e:
        return jsonify({"error": f"File upload failed: {str(e)}"}), 500

    # Prepare payload for the external API

    payload = {
        "model": "kling",
        "task_type": "ai_try_on",
        "input": {
            "model_input": model_input_url,
            "batch_size": 1
        }
    }

    if dress_input_file:
        payload["input"]["dress_input"] = dress_input_url
    elif upper_input_file and lower_input_file:
        payload["input"]["upper_input"] = upper_input_url
        payload["input"]["lower_input"] = lower_input_url
    elif upper_input_file:
        payload["input"]["upper_input"] = upper_input_url
    else:
        payload["input"]["lower_input"] = lower_input_url

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    # Call the external API
    try:
        response = requests.post(API_URL_CREATE_TASK, headers=headers, json=payload)
        # response.raise_for_status()  # Raise an exception for HTTP errors
        # return jsonify(response.json())  # Forward the response back to the client
        result = response.json()  # Forward the response back to the client
        task_id = result['data']['task_id']
        url = f"{API_URL}{task_id}"
        # Define headers with the API key
        headers = {
            'x-api-key': API_KEY
        }
        start_time = time.time()
        # Make the GET request to the external API
        try:
            while True:
                # Make the GET request to the external API
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise exception for HTTP errors

                # Parse the response JSON
                response_data = response.json()

                print(response.json())

                # Check the status
                if response_data['data']['status'] == 'completed':
                    # Return the final output once the task is completed
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"Request to {url} took {elapsed_time:.2f} seconds")
                    return jsonify(response_data['data']['output']['works'][0]['image']['resource_without_watermark'])
                elif response_data['data']['status'] == 'failed':
                    return jsonify(response_data)

                # Wait before sending the next request
                time.sleep(2)  # Adjust sleep time as per API rate limits
        except requests.exceptions.RequestException as e:
            # Handle errors and return a meaningful message
            return jsonify({"error": str(e)}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/virtual_try-on-with-image', methods=['POST'])
def virtual_ai_try_on_image():
    user_data = request.form  # Changed to form to handle file uploads

    # Validate required fields
    required_fields = ["model_input", "batch_size"]
    for field in required_fields:
        if field not in user_data:
            return jsonify({"error": f"'{field}' is required"}), 400

    return apiLogic.generate_image_with_image_and_return_image(request, user_data)


@app.route('/get-tasks/<task_id>', methods=['GET'])
def get_tasks(task_id):
    # Ensure that task_id is provided
    if not task_id:
        return jsonify({"error": "task_id is required"}), 400

    # Define the URL with the task_id as a query parameter
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
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        # Handle errors and return a meaningful message
        return jsonify({"error": str(e)}), 500


@app.route('/generate-video', methods=['POST'])
def generate_video():
    user_data = request.json

    # Validate required fields
    required_fields = ["prompt", "image"]
    for field in required_fields:
        if field not in user_data:
            return jsonify({"error": f"'{field}' is required"}), 400

    apiLogic.generate_video_prompt(None, user_data)


@app.route('/generate-video-with-image', methods=['POST'])
def generate_video_image():
    user_data = request.form

    # Validate required fields
    required_fields = ["prompt"]
    for field in required_fields:
        if field not in user_data:
            return jsonify({"error": f"'{field}' is required"}), 400

    image_file = request.files.get('image')

    apiLogic.generate_video_prompt(image_file, user_data)


HEYGEN_API_KEY = 'ZWJhNzQwMTczODdjNDg5ZWIwNTFmMGIxMTQzZjNkNjgtMTczNDQ2MTE4Ng=='
HEYGEN_API_URL = 'https://api.heygen.com/v2/video/generate'


@app.route('/heygen-generate-video', methods=['POST'])
def heygen_generate_video():
    """Endpoint to trigger HeyGen API for video generation"""
    try:
        # Extract input data from the incoming request
        input_data = request.get_json()
        if not input_data:
            return jsonify({"error": "Invalid request, JSON payload required"}), 400

        # Set up headers for the HeyGen API request
        headers = {
            'X-Api-Key': HEYGEN_API_KEY,
            'Content-Type': 'application/json'
        }

        # Make the POST request to the HeyGen API
        response = requests.post(HEYGEN_API_URL, headers=headers, json=input_data)

        # Return the response from the HeyGen API
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Failed to generate video",
                "status_code": response.status_code,
                "response": response.json()
            }), response.status_code

    except Exception as e:
        return jsonify({"error": "An error occurred", "message": str(e)}), 500


@app.route('/try-on-return-url', methods=['POST'])
def ai_try_on_return_url():
    user_data = request.json

    # Validate required fields
    required_fields = ["model_input", "batch_size"]
    for field in required_fields:
        if field not in user_data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Prepare payload for the external API
    payload = {
        "model_input": user_data.get("model_input"),
        "batch_size": user_data.get("batch_size")
    }
    if "dress_input" in user_data:
        payload["upper_input"] = user_data.get("dress_input")
    elif "upper_input" not in user_data:
        payload["lower_input"] = user_data.get("lower_input")
    elif "lower_input" not in user_data:
        payload["upper_input"] = user_data.get("upper_input")
    else:
        payload["upper_input"] = user_data.get("upper_input")
        payload["lower_input"] = user_data.get("lower_input")

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    # Call the external API
    try:
        response = requests.post(API_URL_CREATE_TASK, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        # return jsonify(response.json())  # Forward the response back to the client
        result = response.json()  # Forward the response back to the client
        task_id = result['data']['task_id']
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

                # Check the status
                if response_data['data']['status'] == 'completed':
                    # Return the final output once the task is completed
                    return jsonify(response_data['data']['output']['works'][0]['image']['resource_without_watermark'])

                # Wait before sending the next request
                time.sleep(2)  # Adjust sleep time as per API rate limits
        except requests.exceptions.RequestException as e:
            # Handle errors and return a meaningful message
            return jsonify({"error": str(e)}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
