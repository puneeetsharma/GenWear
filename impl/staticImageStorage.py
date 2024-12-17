import base64
import requests

GITHUB_API_URL = "https://api.github.com"
OWNER = "puneeetsharma"
REPO = "GenWear"
BRANCH = "main"


def store_image_to_github(file_path: str, image_name: str, commit_message: str = "Add image") -> dict:
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()

    # Encode image in base64 as required by GitHub API
    encoded_content = base64.b64encode(image_data).decode("utf-8")

    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/contents/{image_name}"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": BRANCH
    }

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"Image '{image_name}' successfully uploaded to GitHub.")
    else:
        print(f"Failed to upload image. Status Code: {response.status_code}, Response: {response.json()}")

    return response.json()


def fetch_image_from_github(image_name: str) -> bytes:
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/contents/{image_name}"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Successfully fetched image '{image_name}' from GitHub.")
        return response.content  # Binary content of the image
    else:
        print(f"Failed to fetch image. Status Code: {response.status_code}, Response: {response.json()}")
        return None


# Example usage
if __name__ == "__main__":
    image_content = fetch_image_from_github("images/model.png")

    if image_content:
        with open("downloaded_image.png", "wb") as f:
            f.write(image_content)

