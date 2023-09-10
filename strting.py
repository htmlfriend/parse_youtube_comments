# -*- coding: utf-8 -*-

import os , sys



from dotenv import load_dotenv

from googleapiclient.discovery import build

from utils.comments import process_comments, make_csv
load_dotenv()


API_KEY = os.getenv("API_KEY")
    

youtube = build(
        "youtube", "v3", developerKey = API_KEY)
def comment_threads(channelID, to_csv=True):
    comments_list = []
    request= youtube.commentThreads().list(
        part="id, replies, snippet",
        videoId=channelID,
        # maxResults=5
    )
    response =request.execute()
    # print(response)
    comments_list.extend(process_comments(response['items']))
    # print(len(response['items']))
    # print(comments_list)

    while response.get('nextPageToken', None):
        request= youtube.commentThreads().list(
        part="id, replies, snippet",
        videoId=channelID,
        pageToken= response['nextPageToken']
    )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    print(f'Finished fetching comment for {channelID}. {len(comments_list)} comments found')

    if to_csv:
        make_csv(comments_list, channelID)

        return comments_list

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    comment_threads('e9zLc204npU')

if __name__ == "__main__" :
    main()   