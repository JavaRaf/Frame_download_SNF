import asyncio
import httpx
import data
import os
import glob

# upload gif to giphy server
async def upload_gif(comment: dict):
    if not comment['file_path'].endswith('.gif'):
        print("O arquivo precisa ser uma GIF.")
        return
    

    retries = 0
    while  retries < 3:
        try:
            async with httpx.AsyncClient() as client:
                with open(comment['file_path'], 'rb') as gif_file:
                    files = {'file': gif_file}
                    dados = {
                        'api_key': data.GIPHY_API_KEY
                    }
                    response = await client.post(data.giphy_url, files=files, data=dados, timeout=30)
                    if response.status_code == 200:
                        response_data = response.json()
                        link = 'https://giphy.com/gifs/' + response_data.get("data", {}).get("id", '')
                        comment['link'] = link
                        print(f'GIF enviada para o servidor do Giphy: {link}')
                        break
                    else:
                        print(f'Erro ao enviar a GIF: {response.status_code}, {response.text}')
        except Exception as e:
            print(f'Erro ao abrir o arquivo: {e}')
            print('tentando novamente em 2 segundos...')
            await asyncio.sleep(2)

# sort files by frame number to create gif
def ordenar_frames(file_path: str) -> None:
    """Função síncrona para renomear arquivos"""
    for frame in os.listdir(file_path):
        if frame.endswith('.jpg'):
            # extract frame number 
            num = int(frame.split('.')[0].split('_')[-1])
            # rename frame with 4 digits, zeros in front
            new_name = f'frame_{num:04d}.jpg'
            old_path = os.path.join(file_path, frame)
            if not os.path.exists(os.path.join(file_path, new_name)):
                new_path = os.path.join(file_path, new_name)
                os.rename(old_path, new_path)


# resize images to create gif small
async def resize_images(image_files: list, resize_image_command_base: list):
    """Função assíncrona para redimensionar imagens"""
    resize_image_command = resize_image_command_base + ['-resize', '30%'] + image_files
    try:
        process = await asyncio.create_subprocess_exec(*resize_image_command)
        await process.communicate()
        print("Imagens redimensionadas com sucesso!")
    except Exception as e:
        print(f'Erro ao redimensionar as imagens: {e}')


async def make_gif(comment: dict) -> None:
    """Função principal para criar o GIF"""
    if data.GIPHY_API_KEY and comment.get('file_path', None):
        file_path = comment.get('file_path')
        if file_path:
            # Define commands according to the operating system
            image_magick_command = 'magick' if os.name == 'nt' else 'convert'
            resize_image_command_base = ['magick', 'mogrify'] if os.name == 'nt' else ['mogrify']

            # Gets all .jpg image files in the directory
            image_files = glob.glob(f'{file_path}/frame*.jpg')

            if image_files:
                # Resizes images asynchronously (asynchronous process)
                await resize_images(image_files, resize_image_command_base)

            # command to create gif
            commands = [
                image_magick_command,
                '-delay', '25',
                '-loop', '0',
                f'{file_path}/frame*.jpg',
                '-colors', '32',
                '-layers', 'optimize',
                f'{file_path}/animation.gif',
            ]

            try:
                process = await asyncio.create_subprocess_exec(*commands)
                await process.communicate()
                comment['file_path'] = f'{file_path}/animation.gif'
                print("GIF gerada com sucesso!")
            except Exception as e:
                print(f'Erro ao criar o GIF: {e}')

            # Função de upload do GIF
            await upload_gif(comment)


def run_make_gif(comment: dict) -> None:
    ordenar_frames(comment['file_path'])
    asyncio.run(make_gif(comment))
