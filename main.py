import os
import time

from dotenv import load_dotenv; load_dotenv(override=False)

from src.comments import get_fb_posts, person_data
from src.save_ids import remove_seen_comments




def main():

    if os.getenv("FB_TOKEN") is None:
        raise ValueError("FB_TOKEN not defined.")

    posts = get_fb_posts(max_attempts=2)  # Gets 200 comments (2 attempts)
    persons = person_data(posts)  # Creates Person objects for each comment
    persons = remove_seen_comments(persons)

    posts = get_fb_posts(max_attempts=2)  # Gets 200 comments (2 attempts)
    persons = remove_seen_comments(person_data(posts))  # get person objects for each comment, filter seen_ids
    










if __name__ == '__main__':

    start: float = time.time()
    while (time.time() - start) < (180 * 60):  # 3 hours
        main()
        print('Sleeping for 60 seconds...\n', flush=True)
        time.sleep(60)