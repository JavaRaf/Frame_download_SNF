from page_id import get_id 
from comments import get_comments
from get_img import get_img
from finder import finder_commands
from responses import response
from save_ids import remove_replyed_ids
import time
import os 



def main():

    get_id() # get page id
    if os.environ.get('PAGE_ID') == None: # if page id is not specified then exit with error
        print('Failed to get page id: No page ID found or wrong page ID', flush=True)
        os.sys.exit(1)
    
    comments_list: list[dict] = get_comments()
    remove_replyed_ids(comments_list) # remove comments with id in replyed_ids.txt
    
    if comments_list is not None:
        for comment in comments_list:
            finder_commands(comment)
            get_img(comment)
            response(comment)
        
        

if __name__ == '__main__':
    start: float = time.time()
    while (time.time() - start) < (180 * 60):  # 3 hours
        main()
        print('Sleeping for 50 seconds...\n', flush=True)
        time.sleep(50)
        