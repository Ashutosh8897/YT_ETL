import requests
import json
import os
import dotenv

api_key = os.getenv("API_KEY")
channel_name = "MrBeast"

def get_playlistid():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_name}&key={api_key}"

        response =requests.get(url)
        response.raise_for_status() 
        data = response.json()
        # print(json.dumps(data,indent=4))
        channel_itms = data["items"][0]
        channel_playlistID = channel_itms["contentDetails"]["relatedPlaylists"]['uploads']
        # print(channel_playlistID)
        return channel_playlistID

        
    except requests.exceptions.RequestException as e:
        raise e 
    
if __name__ == "__main__":
    get_playlistid()
