import httpx
import time
import os
import data


def get_comments() -> list[dict]:
    """Returns a list[dict] of messages and ids"""

    retries     = 0
    max_retries = 5
    comments_list: list[dict] = [] 
    filter = ['Random Crop.','Subtitles:']
    comments_params = {'fields': 'comments.limit(100)', 'limit': '100', 'access_token': data.FB_TOKEN}

    try:
        while retries < max_retries:
            response = httpx.get(f'{data.fb_url}/{os.environ.get("PAGE_ID")}/posts', params=comments_params, timeout=15)
            if response.status_code == 200:
                response_data = response.json()
                for item in response_data['data']:
                    comment_data = item.get('comments', {}).get('data', [])
                    for comment in comment_data:
                        id, message = comment.get('id'), comment.get('message')
                        if id and message and not any(message.startswith(f) for f in filter):
                            comments_list.append({'comment': message, 'id': id})
                            
                # Check for pagination
                if response_data.get('paging') and response_data['paging'].get('next'):
                        after = response_data['paging']['cursors'].get('after', '')
                        comments_params['after'] = after
                        retries += 1 
                else:
                    break
            else:
                print(f"Error: {response.status_code} {response.content}")
                retries += 1
                time.sleep(3)

    except httpx.RequestError as e:
        print(f"Error: {e}")

    print("Number of comments:", len(comments_list))
    return comments_list


