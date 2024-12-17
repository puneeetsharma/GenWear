import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader
import json

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
    'Partners-Signature': 'C0C85D03142769EA34C1E51658297CD6CB2CACDBBC5CBBA0ED2B009E2297A11D',
    'Blibli-Extras-MerchantId': 'DED-70077',
    '__cf_bm': 'GPtjjRJh48YkBY_gl2Ze9UzRQrxJWc6oTM7koyqsZKw-1734427528-1.0.1.1-t4aCPl16OCyo4.fxr5pa7.1wMnXRuv9WlnL8ZRG1nC58ijI90dcHsV_8euXQfO8j4jdCiNayGZLDxw5Pw2mF_g',
    '__bwa_session_id': '1734433381.bd5ae846-8d1f-4e6b-b488-b2c983f82d5f'
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
    cookies = {
        "__bwa_user_id": "723337755.U.1481629537580909.1703572604",
        "_fbp": "fb.1.1703572603948.650712607",
        "_vwo_ssm": "1",
        "_vwo_uuid": "D0FECF4DA90DB71E169FD408AF48C2A90",
        "__bwa_session_id": "1734427529.f2803e92-57c0-4718-ad80-f27d3516118b",
        "__bwa_session_action_sequence": "2",
        "JSESSIONID": "37EF6BEE093E6720ECCFCDE0F42C8D28",
        # Add other cookies as needed
    }

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
API_KEY = "e2adc30848fb4497f5f496be2ab86f99cbed7e1c9e12c9382193521b692d4fa3"


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
        "model_input": user_data.get("model_input"),
        "batch_size": user_data.get("batch_size")
    }
    if "dress_input" in user_data:
        payload["upper_input"] = user_data.get("dress_input")
    else:
        if "upper_input" not in user_data or "lower_input" not in user_data:
            return jsonify(
                {"error": "'upper_input' and 'lower_input' are required when 'dress_input' is not provided"}), 400
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
        return jsonify(response.json())  # Forward the response back to the client
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
