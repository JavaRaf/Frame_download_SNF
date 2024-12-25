import user
import re
import httpx
import data
import time
import os
import helper
import ivote

def finder_frame_title_post(comment: dict) -> None:
    post_id = f'{os.environ.get("PAGE_ID")}_{comment["id"].split("_")[0]}'
    retries: int = 0
    max_retries: int = 3

    while retries < max_retries:
        try:
            response = httpx.get(
                f'{data.fb_url}/{post_id}', 
                params={'access_token': data.FB_TOKEN}, 
                timeout=5
            )

            if response.status_code == 200:
                response_data = response.json()

                if 'message' in response_data:
                    # Extrair informações usando regex
                    match = re.search(
                        r'Season\s*(\d+),\s*Episode\s*(\d+),\s*Frame\s*(\d+)', 
                        response_data['message']
                    )
                    if match:
                        season, episode, frame = match.groups()
                        comment['season'] = int(season)
                        comment['episode'] = int(episode)
                        comment['frame_number'] = int(frame)
                        break  
            else:
                print(f"Error module finder_frame_title_post: {response.status_code} {response.content}")
                retries += 1
                time.sleep(3)

        except httpx.RequestError as e:
            print(f"Error module finder_frame_title_post: {e}.\nRetrying ({retries + 1}/{max_retries})...")
        
        retries += 1
        time.sleep(3)


def finder_frame_number(comment: dict) -> None:
    season_number = re.findall(r'-s\s*(\d+)', comment['comment'])
    frame_number = re.findall(r'-\s*f\s*(\d+)', comment['comment'])
    if frame_number and season_number:
        comment['season_number'] = season_number[0].lstrip('0')
        comment['frame_number'] = frame_number[0].lstrip('0')
    
    else:
        finder_frame_title_post(comment)


def finder_subtitle(comment: dict) -> None:
    subtitle = re.findall(r'-t\s*(.*)', comment['comment'])
    if subtitle:
        comment['subtitle'] = subtitle[0]


def finder_commands(comment: dict) -> None:
    if user.str_command_download.lower() in comment.get('comment', '').lower():
        finder_subtitle(comment)
        finder_frame_number(comment)
    
    elif user.str_command_gif.lower() in comment.get('comment', '').lower():
        finder_frame_number(comment)
    
    elif user.str_command_help.lower() in comment.get('comment', '').lower():
        helper.helper(comment)
    
    elif user.str_command_vote.lower() in comment.get('comment', '').lower():
        finder_frame_number(comment)
        comment['vote'] = ivote.add_vote(comment)
    
    else: # remove comment and id if not present command
        comment['comment'] = ''
        comment['id'] = ''

    
