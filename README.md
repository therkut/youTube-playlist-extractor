# YouTube Playlist Extractor

This Python script allows you to fetch videos from a specific YouTube playlist, extract hashtags from the video descriptions, and save the data into CSV and JSON files. If no hashtags are found in the description, the script generates random hashtags from the video title.

## Features

- Fetches all videos from a specified YouTube playlist.
- Extracts hashtags from the video descriptions.
- Generates random hashtags from the video title if no hashtags are found.
- Saves the video data (title, URL, and hashtags) to a CSV file.
- Caches the video data to a JSON file for faster access if already fetched within the last 24 hours.

## Requirements

- Python 3.x
- Google API Client Library (`google-api-python-client`)
  
You can install the required dependencies by running:
```bash
pip install --upgrade google-api-python-client
