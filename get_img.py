import httpx
import asyncio
import os
import data
import user
import save_ids

def get_one_img(comment: dict) -> None:
    response = httpx.get(f'{data.github_url}/frame_{comment["frame_number"]}.jpg', timeout=20)

    if response.status_code == 200:
        file_path = f'images/{comment["id"]}/frame_{comment["frame_number"]}.jpg'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(response.content)
            comment['file_path'] = file_path
    elif response.status_code == 404:
        save_ids.save_id(comment, 'Imagem não encontrada, reposta ignorada, id salvo: ')
    else:
        print(f"Error downloading frame {comment['frame_number']}: {response.status_code} {response.text}")



async def get_manys_img(session: httpx.AsyncClient, frame_number: str, id: str) -> None:
    try:
        response = await session.get(f'{data.github_url}/frame_{frame_number}.jpg', timeout=15)

        if response.status_code == 200:
            file_path = os.path.join(f'images/{id}/frame_{frame_number}.jpg')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return f'images/{id}'
        else:
            print(f"Error downloading frame {frame_number}: {response.status_code} {response.text}")
            return ''

    except Exception as e:
        print(f"Error downloading frame {frame_number}: {e}")
        return ''


# Função principal para gerar o gif
async def img_fetch(comment: dict) -> None:

    if user.str_command_download in comment.get('comment', '').lower():
        get_one_img(comment)

    elif user.str_command_gif in comment['comment'].lower():
        async with httpx.AsyncClient() as session:
            tasks = []
            if int(comment['frame_number']) - 15 > 0:
                start_frame = int(comment['frame_number']) - 10
                end_frame = int(comment['frame_number']) + 20
            else:
                start_frame = 1
                end_frame = 30
            
            for frame_number in range(start_frame, end_frame):
                tasks.append(get_manys_img(session, frame_number, comment['id']))

            file_paths = await asyncio.gather(*tasks)
            
            if file_paths[0] != '':
                comment['file_path'] = file_paths[0]
            else:
                save_ids.save_id(comment, 'Imagem(s) não encontrada(s), reposta ignorada, id salvo: ')



def get_img(comment: dict) -> None:
    if comment.get('comment') and comment.get('id') and comment.get('frame_number'):
        asyncio.run(img_fetch(comment))



    