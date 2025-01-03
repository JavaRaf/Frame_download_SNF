import httpx
import data
from time import sleep


# module for uploading image in imgBB
def imgBB(comment: dict) -> None:
    retries = 0
    while retries < 3:
        try:
            dados = {'key': data.IMG_TOKEN, 'name': f'frame_{comment["frame_number"]}', 'expiration': 600000}

            with open(comment['file_path'], 'rb') as file:
                files = {'image': file}
                
                response = httpx.post(data.img_url, data=dados, files=files, timeout=15)
                if response.status_code == 200:
                    response_data = response.json()
                    link = response_data['data']['url']
                    
                    if link:
                        comment['link'] = link
                        break

                else:
                    print('erro no imgbb', response.status_code)
                    print(response.text)
                    sleep(3)
                    retries += 1
                    
        except FileNotFoundError:
            print(f"O arquivo {comment['file_path']} não foi encontrado.")
            retries += 1