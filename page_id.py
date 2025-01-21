import os
import httpx
import time
import data


# function to get the facebook page id and store it in the PAGE_ID environment variable

def get_id():
    if 'PAGE_ID' not in os.environ:
        retries: int = 0
        max_retries: int = 3
        while retries < max_retries:
            try:
                response = httpx.get(f'{data.fb_url}/me?access_token={data.FB_TOKEN}', timeout=10)
                if response.status_code != 200:
                    print(f"Failed to get page ID: {response.status_code} {response.content}", flush=True)
                    retries += 1
                else:
                    PAGE_ID: str = response.json().get('id')
                    if PAGE_ID:
                        os.environ.setdefault("PAGE_ID", PAGE_ID)
                        print('Facebok PAGE_ID set successfully', flush=True)
                        break
                    
            except httpx._exceptions as e:
                retries += 1
                print(f"Request error: {e}\n. Retrying...", flush=True)
                time.sleep(3)
        
        if retries == max_retries:
            print("Failed to get page ID after maximum retries", flush=True)
