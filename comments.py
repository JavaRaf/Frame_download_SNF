import httpx
import time
import os
import data


def get_comments() -> list:
    comments_list: list[dict] = []  
    dados = {'fields': 'comments.limit(100)', 'limit': '100', 'access_token': data.FB_TOKEN}

    try:
        retries: int = 0
        max_retries: int = 5
        max_pages: int = 5
        current_page: int = 0
        
        while retries < max_retries and current_page < max_pages:
            response = httpx.get(f'{data.fb_url}/{os.environ.get("PAGE_ID")}/posts', params=dados, timeout=15)

            if response.status_code == 200:
                response_data = response.json()
                for item in response_data.get('data', []):
                    comments_data = item.get('comments', {}).get('data', [])
                    if len(comments_data) >= 1:
                        for comment in comments_data:
                            if 'id' in comment:
                                if not comment['message'].startswith('Random Crop.') or not comment['message'].startswith('Subtitles:'):
                                    comments_list.append({'comment': comment['message'], 'id': comment['id']})
                
                # Check for pagination
                if response_data.get('paging') and response_data['paging'].get('next'):
                    after = response_data['paging']['cursors'].get('after', '')
                    dados['after'] = after
                    current_page += 1  # Increment the current page
                else:
                    break
            
            else:
                print(f"Error module comments: status_code != 200 {response.status_code}")
                retries += 1
                time.sleep(2)  # wait 2 seconds before retrying

        if retries == max_retries:
            print("Error module comments: Failed to get comments after maximum retries")

    except httpx._exceptions.RequestError as e:
        print(f"Error module comments: {e}")

    print(f'size of comments list: {len(comments_list)}')
    return comments_list

