import os

import re
import time

import httpx
from httpx import Client, Timeout

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

from src.person_class import Person
from src.save_ids import remove_seen_comments


def find_frame_subtitle(personComment: str) -> str:
    """
    Extracts the frame subtitle from the person's comment.
    The frame subtitle is expected to be present after the "-t" prefix in the comment.
    """
    match = re.search(r"-t", personComment)
    if not match:
        return None
    
    return personComment[match.end():].strip()
  
def is_person_comment_filtered(personComment: str) -> bool:
    """
    Checks if the person's comment contains one of the filtered prefixes.
    """
    filtered_prefixes = [
        "Random Crop.",
        "Subtitles:",
        "𝑺𝒖𝒃𝒕𝒊𝒕𝒍𝒆𝒔:",
    ]
    return personComment.startswith(tuple(filtered_prefixes))

def process_post_message(persons: list[Person]) -> list[Person]:
    """
    Extracts the season, episode, and frame information from the post message.

    This function processes a list of Person objects and extracts the following information:
    - season: The season number.
    - episode: The episode number.
    - frame: The frame number.

    Args:
        persons (list[Person]): A list of Person objects containing the post message.

    Returns:
        list[Person]: A list of Person objects with the extracted information.
    """
    pattern = r"Season (\d+), Episode (\d+), Frame (\d+)"
    
    for person in persons:
        match = re.search(pattern, person.post_message)
        if match:
            person.season = int(match.group(1))
            person.episode = int(match.group(2))
            person.frame = int(match.group(3))
    
    return persons

def person_data(posts: list) -> list[Person]:
    """
    Processes a list of posts to extract relevant comment data and create Person objects.

    This function iterates through a list of posts, extracting information about the post,
    the author of the comments, and the comments themselves. It creates a list of Person
    objects containing the following information:
    - post_message: The message of the post.
    - post_id: The ID of the post.
    - person_name: The name of the person who made the comment.
    - person_id: The ID of the person who made the comment.
    - comment: The comment message.
    - comment_id: The ID of the comment.
    - created_time: The time the comment was created.
    - frame_subtitle: The frame subtitle extracted from the comment (if present).

    Args:
        posts (list): A list of posts from the Facebook Graph API.

    Returns:
        list[Person]: A list of Person objects containing the extracted information.
    """
    persons: list[Person] = []
    for post in posts:
        comments = post.get('comments', {}).get('data', [])
        for comment in comments:
            try:
                author = comment.get('from', {})
                person = Person(
                    post_message=post.get('message'),           # post info
                    post_id=post.get('id'),                     # post info

                    person_name=author.get('name'),             # author info
                    person_id=author.get('id'),                 # author info

                    comment=comment.get('message'),                             # comment info
                    comment_id=comment.get('id'),                               # comment info
                    created_time=comment.get('created_time'),                   # comment info
                    frame_subtitle=find_frame_subtitle(comment.get('message')), # comment info
                )

                if not is_person_comment_filtered(person.comment):
                    persons.append(person)

            except Exception as e:
                print(f"Error processing comment: {e}")
                continue
    return persons

@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=2, min=1, max=10))
def get_fb_posts(fb_version: str = "v21.0", max_attempts: int = 6) -> list:
    """
    Fetches the latest posts from a Facebook page using the specified Facebook Graph API version.

    Args:
        fb_version (str, optional): The Facebook Graph API version to use. Defaults to 'v21.0'.
        max_attempts (int, optional): attempts equivalent to a number of posts processed. Defaults to (6 == 600 posts)

    Returns:
        list: A list of posts from the Facebook Graph API.
    """
    timeout = Timeout(connect=10, read=10, write=10, pool=10)
    fb_url = f'https://graph.facebook.com/{fb_version}'
    posts_data = []
    SLEEP_TIME = 2

    access_token = os.getenv("FB_TOKEN")
    if not access_token:
        raise ValueError("FB_TOKEN not defined.")

    params = {
        'fields': 'message, comments.limit(50)',
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

                time.sleep(SLEEP_TIME)

            except httpx.RequestError as e:
                print(f"Erro na requisição HTTP: {str(e)}", flush=True)
                time.sleep(SLEEP_TIME)
                continue

            except Exception as e:
                print(f"Erro inesperado: {str(e)}", flush=True)
                time.sleep(SLEEP_TIME)
                continue
    
    return posts_data

# agregates functions
def process_comments(fb_version: str = 'v21.0', max_attempts: int = 6) -> list[Person]:
    """
    Downloads and processes comments from a Facebook page, returning a list of Person objects.
    
    It fetches the latest posts using the specified Facebook Graph API version,
    extracts relevant comment data, and filters out comments that have already been handled.

    Args:
        fb_version (str, optional): The Facebook Graph API version to use. Defaults to 'v21.0'.
        max_attempts (int, optional): attempts equivalent to a number of posts processed. Defaults to (6 == 600 posts).

    Returns:
        list[Person]: A list of Person objects removed from seen_ids.
    """
    return remove_seen_comments(
    process_post_message(
        person_data(
            get_fb_posts(fb_version, max_attempts)
        )
    )
)




