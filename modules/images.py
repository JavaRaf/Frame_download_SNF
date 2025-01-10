from .person import Person
import os
import time
import httpx
import asyncio


class Images:
    def __init__(self, github_repo_link: str) -> None:
        self.github_base_url = "https://raw.githubusercontent.com"
        self.github_repo_link = github_repo_link

        self.repo_owner = ""
        self.repo = ""
        self.branch = ""
        self.frames_folder = "frames"
        self.resolve_github_repo_link()

    def resolve_github_repo_link(self) -> None:
        if self.github_repo_link.endswith(".git"):
            self.github_repo_link = self.github_repo_link[:-4]

        self.repo_owner = self.github_repo_link.split("/")[-2]
        self.repo = self.github_repo_link.split("/")[-1]

        for _ in range(2):
            response = httpx.get(f"https://api.github.com/repos/{self.repo_owner}/{self.repo}")
            
            if response.status_code == 200:
                self.branch = response.json()["default_branch"]
                break  

            print("Error when trying to get name, repo and branch from github. Retrying...\n", response.text)

    def upload(self, url: str, path: str) -> None:
        pass


    async def fetch_image(self, url: str, path: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=15)
            response.raise_for_status()

            with open(path, "wb") as file:
                file.write(response.content)

    async def fetch_frames(self, person: Person) -> None:
        tasks = []
        for frame in person.frames:
            file_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "images",
                    f"{person.comment_id}",
                    f"frame_{frame}.jpg",
                )
            )
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            frame_url = "/".join(
                [
                    self.github_base_url,
                    self.repo_owner,
                    self.repo,
                    self.branch,
                    self.frames_folder,
                    f"frame_{frame}.jpg",
                ]
            )

            tasks.append(self.fetch_image(frame_url, file_path))

            if not person.file_path:
                person.file_path = os.path.dirname(file_path)

        await asyncio.gather(*tasks)
      
    def download_frames(self, person: Person) -> None:
        asyncio.run(self.fetch_frames(person))