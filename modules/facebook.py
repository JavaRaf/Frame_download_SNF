import os
import re
import httpx
import time
from .person import Person


class Facebook:
    def __init__(self):
        self.fb_token =  os.environ.get("FB_TOKEN", None)
        self.api_version = "v21.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.page_name = ""
        self.page_id = ""
        self.get_page_name_and_id()

    def get_page_name_and_id(self) -> tuple[str, str]:
        """
        Busca o nome e ID da página do Facebook.
        """
        if not self.fb_token:
            raise ValueError("Facebook token not found")

        url = f"{self.base_url}/me"
        params = {"access_token": self.fb_token}

        try:
            response = httpx.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            self.page_id = data.get("id", "")
            self.page_name = data.get("name", "")

            if not self.page_id or not self.page_name:
                raise ValueError("Unable to fetch page information. Check your token.")

            return self.page_name, self.page_id

        except httpx.RequestError as e:
            raise RuntimeError(f"Error connecting to Facebook API: {e}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HTTP error occurred: {e.response.status_code}, {e.response.text}"
            )

    def process_comments(self, comments_list) -> list[Person]:
        """
        Processa comentários e retorna uma lista de instancias de Person, contendo informações relevantes.
        """
        processed_data: list[Person] = []

        for comment_dict in comments_list:
            
            post_message = re.match(r"Season (\d+), Episode (\d+), Frame (\d+)", comment_dict["message"])
            post_id = comment_dict["id"]

            data_comments = comment_dict.get("comments", {}).get("data", [])

            for comment in data_comments:
                if comment["message"].startswith("!"):

                    person = Person()

                    person.post_id = post_id
                    person.person_name = comment.get("from", {}).get("name")
                    person.person_id = comment.get("from", {}).get("id")
                    person.comment_id = comment.get("id")
                    person.message = comment.get("message")
                    person.created_time = comment.get("created_time")

                    if post_message:
                        person.season = int(post_message.group(1))
                        person.episode = int(post_message.group(2))
                        person.frames.append(int(post_message.group(3)))


                    processed_data.append(person)
     
        return processed_data

    def send(self, person: Person) -> str:
        pass

    def search_data(self) -> list[Person]:
        """ Busca comentários na página do Facebook que comecem com "!"
        return: Lista de instancias de Person com dados relevantes.
        """
        # me/posts?fields=message,comments.limit(100)&limit=100
        tries = 0; max_retries = 1; data = []
        params = {
            "fields": "message,comments.limit(100)",
            "limit": "100",
            "access_token": self.fb_token,
        }

        while tries < max_retries:
            try:
                response = httpx.get(
                    f"{self.base_url}/me/posts", params=params, timeout=15
                )

                if response.status_code == 200:
                    response_data = response.json()

                    if response_data:
                        comments = response_data.get("data", [])
                        data.extend(self.process_comments(comments))

                        # Verifica se há mais páginas para carregar
                        if not response_data.get("paging", {}).get("next"):
                            break

                        after = (
                            response_data.get("paging", {})
                            .get("cursors", {})
                            .get("after", None)
                        )
                        if after:
                            params.update({"after": after})

                tries += 1; time.sleep(3)

            except httpx.RequestError as e:
                print(f"Error fetching data: {e}")
                tries += 1; time.sleep(3)

        return data





