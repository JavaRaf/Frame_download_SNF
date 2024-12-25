import httpx
import os
import time
import data
import user



def post_fb(comment: dict) -> None:

    if comment['file_path'].endswith('.gif'):
        comment['foto_id'] = ''
        return

    retries = 0
    while retries < 3:
        try:
            
            mimetype = 'image/jpeg'
            endpoint = f'{data.fb_url}/me/photos'
            
            # Verificar se o caminho fornecido está correto
            with open(comment['file_path'], 'rb') as frame:
                files = {'file': (os.path.basename(comment['file_path']), frame, mimetype)}
                
                dados = {
                    'published': 'false',
                    'access_token': data.FB_TOKEN  # Use o FB_TOKEN diretamente
                }
                response = httpx.post(endpoint, files=files, data=dados, timeout=20)
                
            if response.status_code == 200:
                foto_id = response.json().get('id')
                if foto_id:
                    comment['foto_id'] = foto_id
                    break
            else:
                print(f'Erro ao fazer upload: {response.status_code}, {response.text}')
                retries += 1
                time.sleep(3)
            
        except Exception as e:
            print(f'Erro ao fazer upload: {e}')
            retries += 1
            time.sleep(3)



def publish_fb(comment: dict) -> None:
    retries = 0
    while retries < 3:

        if comment.get('file_path') and comment['file_path'].endswith('.jpg'):
            message = f'{user.message_response_frame_download.format(FRAME=comment["frame_number"], LINK=comment["link"])}'
        else:
            if comment.get('message') and comment['message'].startswith('Helper'):
                message = comment['message'] + f'{user.message_response_helper.format(LINK_GIF=comment["link"])}'
            else:
                message = f'{user.message_response_gif_download.format(FRAME_START=comment["frame_start"], FRAME_END=comment["frame_end"], LINK=comment["link"])}'

        dados = {
            'message': message,
            'access_token': data.FB_TOKEN
        }
        if comment.get('foto_id'):
            dados['attachment_id'] = comment['foto_id']
            
        response = httpx.post(f'{data.fb_url}/{comment["id"]}/comments', data=dados, timeout=20)
        
        if response.status_code == 200:
            id = response.json().get('id')
            if id:
                comment['response_id'] = id
                break
        else:
            print('erro ao postar a imagem pro fb', response.status_code, response.text)
            retries += 1
            time.sleep(3)