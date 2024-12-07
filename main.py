import os
import json
import time
import csv
import re
import random
from googleapiclient.discovery import build

# Add your API key here
API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXX"
PLAYLIST_ID = "PL_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Initialize the YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Folder name (e.g., 'data')
OUTPUT_FOLDER = "data"

# Playlist ID (e.g., 'PLk9rTA29Neh0gETq8rXlgd9lNiWzZJMiT')
PLAYLIST_ID = PLAYLIST_ID  # Add the relevant playlist ID here

# Function to extract hashtags from the description
def extract_hashtags(description):
    # Regular expression to capture all #hashtags in the description
    hashtags = re.findall(r'#\w+', description)
    return hashtags

# Function to generate random hashtags from the title
def generate_hashtags_from_title(title):
    # Split the title into words and shuffle them
    words = title.split()
    random.shuffle(words)
    hashtags = ['#' + word for word in words[:3]]  # Use the first 3 words as hashtags
    return hashtags

# Function to fetch videos from a playlist
def get_playlist_videos(playlist_id):
    # Check if the folder exists, create it if not
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    # Define the path for the cache file
    CACHE_FILE = os.path.join(OUTPUT_FOLDER, f"{playlist_id}_videos_cache.json")
    
    # Check if the cache file exists
    if os.path.exists(CACHE_FILE):
        # Get the last modified time of the file
        file_mod_time = os.path.getmtime(CACHE_FILE)
        current_time = time.time()

        # If the file is older than 24 hours (86400 seconds), fetch data from the API
        if current_time - file_mod_time < 86400:
            print("Data is being fetched from the cache...")
            with open(CACHE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

    # If the cache doesn't exist or is outdated, fetch data from the API
    print("Data is being fetched from the API...")
    
    video_list = []
    next_page_token = None
    
    # Fetch all videos with pagination
    while True:
        # Request to fetch playlist videos
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,  # Maximum 50 videos per request
            pageToken=next_page_token  # If available, fetch the next page
        )
        response = request.execute()

        # Process each video in the response
        for item in response["items"]:
            title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
            description = item["snippet"].get("description", "")
            hashtags = extract_hashtags(description)
            
            # If no hashtags are found, generate them from the title
            if not hashtags:
                hashtags = generate_hashtags_from_title(title)
            
            # Add video information to the list
            video_list.append([title, video_url, ", ".join(hashtags)])

        # If there's a next page, continue fetching
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    # Save the data to the JSON file
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump({"PLAYLIST_ID": playlist_id, "videos": video_list}, file, ensure_ascii=False, indent=4)

    return video_list


# Function to save the data to a CSV file
def save_to_csv(videos, playlist_id):
    # Dynamically generate the file name
    CSV_FILE = os.path.join(OUTPUT_FOLDER, f"{playlist_id}_videos.csv")
    
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL", "Hashtags"])  # Column headers
        writer.writerows(videos)  # Write video data to the file


# Main function
def main():
    videos = get_playlist_videos(PLAYLIST_ID)
    save_to_csv(videos, PLAYLIST_ID)
    print(f"Saved to CSV: {os.path.join(OUTPUT_FOLDER, f'{PLAYLIST_ID}_videos.csv')}")
    print(f"Saved to JSON: {os.path.join(OUTPUT_FOLDER, f'{PLAYLIST_ID}_videos_cache.json')}")

if __name__ == "__main__":
    main()
