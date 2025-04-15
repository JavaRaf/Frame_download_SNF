import os
import time

from dotenv import load_dotenv
from src.comments import Person, process_comments
from src.load_configs import load_configs

load_dotenv(override=False)
configs = load_configs()



def main():
    if os.getenv("FB_TOKEN") is None:
        raise ValueError("FB_TOKEN not defined.")

    persons: list[Person] = process_comments() # you can pass fb_version and max_attempts
    
    if not persons:
        print("no comments to process.", flush=True)
        return
    
    for person in persons:
        pass
    



if __name__ == '__main__':
    start: float = time.time()
    while (time.time() - start) < (180 * 60):  # 3 hours
        main()
        print('Sleeping for 60 seconds...\n', flush=True)
        time.sleep(60)