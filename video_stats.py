import requests
import json
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv(dotenv_path = "./.env")

api_key = os.getenv("API_KEY")
channel_name = "MrBeast"
max_results = 50

def get_playlistid():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_name}&key={api_key}"

        response =requests.get(url)
        response.raise_for_status() 
        data = response.json()
        # print(json.dumps(data,indent=4))
        channel_itms = data["items"][0]
        channel_playlistID = channel_itms["contentDetails"]["relatedPlaylists"]['uploads']
        print(channel_playlistID)
        return channel_playlistID

        
    except requests.exceptions.RequestException as e:
        raise e 
    

def get_videoID(playlistID):
    video_IDs = []
    pageToken = None
    base_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistID}&key={api_key}"

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
        
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
              
            for item in data.get("items", []):
                video_ID = item['contentDetails']['videoId']
                video_IDs.append(video_ID)

            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        return video_IDs


    except requests.exceptions.RequestException as e:
        raise e
    



def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_lst, batch_size):
        for video_id in range(0, len(video_id_lst),batch_size):
            yield video_id_lst[video_id:video_id+batch_size]
    
    


    try:
        for batch in batch_list(video_ids, max_results):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={api_key}"
            response  = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']


                video_data = {
                    "video_id" : video_id,
                    "title" : snippet['title'],
                    "publishedAt" : snippet['publishedAt'],
                    "duration" : contentDetails['duration'],
                    "viewCount" : statistics.get('viewCount', None),
                    "likeCount" : statistics.get('likeCount',None),
                    "commnetCount" : statistics.get('commnetCount', None)
                }

                extracted_data.append(video_data)
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json" 
    with open(file_path, "w", encoding= "utf-8") as json_outputfile:
        json.dump(extracted_data, json_outputfile, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    playlistID = get_playlistid()
    video_ids =(get_videoID(playlistID))
    video_data = (extract_video_data(video_ids))
    save_to_json(video_data)
