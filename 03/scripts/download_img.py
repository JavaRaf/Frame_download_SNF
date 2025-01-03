import httpx
import asyncio
import os


class DownloadImg:

    def __init__(self, **kwargs):
        self.github_base_url    = 'https://raw.githubusercontent.com'
        self.repo_owner         = kwargs.get('repo_owner')
        self.repo               = kwargs.get('repo')
        self.branch             = kwargs.get('branch')
        self.frames_folder      = kwargs.get('frames')


    async def async_download_frame(self, person, frame) -> str:
        frame_url = '/'.join([
            self.github_base_url,
            self.repo_owner,
            self.repo,
            self.branch,
            self.frames_folder,
            f'frame_{frame}.jpg'
        ])

        async with httpx.AsyncClient() as client:
            response = await client.get(frame_url, timeout=15)
            response.raise_for_status()

            file_path = os.path.join(
                os.path.dirname(__file__),
                '..', 'images',
                f'{person["comment_id"]}',
                f'frame_{frame}.jpg'
            )
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as file:
                file.write(response.content)

            person['file_path'] = file_path
            return file_path

    async def fetch_imgs(self, person):
        tasks = []

        for frame in range(person['gif_start'], person['gif_end'] + 1):
            tasks.append(self.async_download_frame(person, frame))  # Adiciona tarefas

        gif_paths = await asyncio.gather(*tasks)  # Executa todas as tarefas simultaneamente

        person['file_path'] = os.path.dirname(gif_paths[0])
        return person['file_path']
        


    def download_frame(self, person, frame):
        asyncio.run(self.async_download_frame(person, frame))
        
    def get_gif_frames(self, person):
        asyncio.run(self.fetch_imgs(person))
        