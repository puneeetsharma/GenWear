import os
import requests
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes required for the YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate_youtube():
    """
    Authenticates the user and returns the YouTube service object.
    """
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube


def download_video(video_url, output_path='downloaded_video.mp4'):
    """
    Downloads a video from the given URL and saves it to the specified path.

    Args:
        video_url (str): The URL of the video to download.
        output_path (str): The path where the video will be saved.

    Returns:
        str: The path of the downloaded video.
    """
    print(f"Downloading video from {video_url}...")
    response = requests.get(video_url, stream=True)

    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded successfully and saved to {output_path}")
    else:
        raise Exception(f"Failed to download video. Status code: {response.status_code}")

    return output_path


def upload_video_to_youtube(youtube, video_path, title="Uploaded Video", description="Uploaded via API", tags=None):
    """
    Uploads a video to YouTube.

    Args:
        youtube: The authenticated YouTube API service object.
        video_path (str): The path to the video file.
        title (str): The title of the video.
        description (str): The description of the video.
        tags (list): A list of tags for the video.

    Returns:
        str: The URL of the uploaded video.
    """
    print("Uploading video to YouTube...")
    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or [],
            'categoryId': '22'  # 22 is the category for "People & Blogs"
        },
        'status': {
            'privacyStatus': 'public'  # Options: 'private', 'public', 'unlisted'
        }
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    video_id = response['id']
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"Video uploaded successfully. YouTube URL: {youtube_url}")
    return youtube_url


def main(video_url):
    """
    Main function to download the video and upload it to YouTube.

    Args:
        video_url (str): The URL of the video to be downloaded and uploaded.

    Returns:
        str: The URL of the uploaded video on YouTube.
    """
    try:
        # Step 1: Download the video from the provided URL
        video_path = download_video(video_url)

        # Step 2: Authenticate and upload the video to YouTube
        youtube = authenticate_youtube()
        youtube_url = upload_video_to_youtube(youtube, video_path)

        # Clean up the downloaded video file
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Temporary video file {video_path} deleted.")

        return youtube_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    video_url = "https://storage.midjourneyapi.xyz/videos/199882249.mp4"  # Example video URL
    youtube_url = main(video_url)
    if youtube_url:
        print(f"Video successfully uploaded to: {youtube_url}")
