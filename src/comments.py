import os

from dataclasses import dataclass
import httpx
from httpx import Client, Timeout
from retry import retry
import time


@dataclass
class Person:
    person_name: str
    person_id: str
    comment: str
    comment_id: str
    created_time: str

def is_person_comment_filtered(person: Person) -> bool:
    """
    Verifica se o comentário da pessoa contém um dos prefixos filtrados.
    """
    filtered_prefixes = [
        "Random Crop.",
        "Subtitles:",
        "𝑺𝒖𝒃𝒕𝒊𝒕𝒍𝒆𝒔:",
    ]
    return person.comment and person.comment.startswith(tuple(filtered_prefixes))

def person_data(posts: list) -> list[Person]:
    persons: list[Person] = []
    for post in posts:
        comments = post.get('comments', {}).get('data', [])
        for comment in comments:
            try:
                author = comment.get('from', {})
                person = Person(
                    person_name=author.get('name'),
                    person_id=author.get('id'),
                    comment=comment.get('message'),
                    comment_id=comment.get('id'),
                    created_time=comment.get('created_time'),
                )
                if not is_person_comment_filtered(person):
                    persons.append(person)
            except Exception as e:
                print(f"Erro ao processar comentário: {e}")
                continue
    return persons

@retry(tries=2, delay=2, max_delay=10, backoff=2)
def get_fb_posts(fb_version: str = "v21.0", max_attempts: int = 6) -> list:
    timeout = Timeout(connect=10, read=10, write=10, pool=10)
    fb_url = f'https://graph.facebook.com/{fb_version}'
    posts_data = []
    SLEEP_TIME = 2

    access_token = os.getenv("FB_TOKEN")
    if not access_token:
        raise ValueError("FB_TOKEN não definido.")

    params = {
        'fields': 'comments.limit(100)',
        'limit': '100',
        'access_token': access_token
    }

    next_url = f'{fb_url}/me/posts'

    with Client(timeout=timeout) as client:
        for _ in range(max_attempts):
            try:
                response = client.get(next_url, params=params)
                response.raise_for_status()
                data = response.json()

                posts_data.extend(data.get('data', []))

                paging = data.get('paging', {})
                next_url = paging.get('next')
                if not next_url:
                    break

                params = None

            except httpx.RequestError as e:
                print(f"Erro na requisição HTTP: {str(e)}", flush=True)
            except Exception as e:
                print(f"Erro inesperado: {str(e)}", flush=True)
            time.sleep(SLEEP_TIME)
    
    return posts_data

# test

# posts = get_fb_posts(max_attempts=2) # Atemps is number of posts (1==100, 2==200 ...)
# persons = person_data(posts) # Each with person_name, person_id, comment, comment_id, created_time

# for person in persons:
#     print(person.person_name, "\n")
#     print(person.person_id, "\n")
#     print(person.comment, "\n")
#     print(person.comment_id, "\n")
#     print(person.created_time, "\n")
#     print("\n")
