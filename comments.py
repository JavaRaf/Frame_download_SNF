import httpx
import time
import os
import data



def get_messages_and_ids(response_data) -> list[dict]:

    messages_and_ids: list[dict] = []
    filter = ['Random Crop.', 'Subtitles:']

    for item in response_data:
        comment_data = item.get('comments', {}).get('data', [])
        for comment in comment_data:
            created_time = comment.get('created_time')
            person_name = comment.get('from', {}).get('name')
            person_id = comment.get('from', {}).get('id')
            comment_id = comment.get('id')
            message = comment.get('message')

            if comment_id and message:
                if not any(message.startswith(f) for f in filter):
                    messages_and_ids.append({
                        'comment': message,
                        'id': comment_id,
                        'created_time': created_time,
                        'person_name': person_name,
                        'person_id': person_id
                    })

    return messages_and_ids

def get_comments() -> list[dict]:
    """Returns a list[dict] of comments from the specified Facebook page"""

    retries, max_retries, messages_and_ids = 0, 6, []
    params = {'fields': 'comments.limit(100)', 'limit': '100', 'access_token': data.FB_TOKEN}

    while retries < max_retries:
        try:
            response = httpx.get(f'{data.fb_url}/{os.environ.get("PAGE_ID")}/posts', params=params, timeout=15)

            if response.status_code == 200:
                response_json = response.json()
                response_data = response_json.get('data', [])
                messages_and_ids.extend(get_messages_and_ids(response_data))

                # Verificar se há próxima página
                paging = response_json.get('paging', {})
                if 'next' in paging:
                    after = paging['cursors']['after']
                    params['after'] = after
                else:
                    break  # Sai do loop se não houver próxima página

            time.sleep(3)
            retries += 1

        except httpx.RequestError as e:
            print(f"Error: {e}")
            time.sleep(3)
            retries += 1
    print('len(messages_and_ids)', len(messages_and_ids))
    return messages_and_ids


