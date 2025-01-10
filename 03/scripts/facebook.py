import httpx
import time
import logging
import re
import os


class Facebook:
    def __init__(self, fb_token, ids, commands):
        """
        Inicializa a classe Facebook.

        :param fb_token: Token de acesso ao Facebook.
        :param ids: Lista de IDs já respondidos.
        :param commands: Lista de comandos disponíveis.
        """
        self.token = fb_token
        self.base_url = "https://graph.facebook.com"
        self.page_id = ""
        self.page_name = ""
        self.replied_ids = ids
        self.commands = commands
        self.fetch_page_name_and_id()

    def fetch_post_info(self, person):
        """
        Busca informações de um post no Facebook.

        :param person: Dicionário contendo informações sobre o post.
        """
        post_id = person.get("post_id")
        url = f"{self.base_url}/{post_id}"
        params = {"access_token": self.token}

        try:
            response = httpx.get(url, params=params, timeout=10)
            response.raise_for_status()  # Verifica erros de HTTP (status != 2xx)
            data = response.json()  # Converte a resposta para JSON

            if "message" not in data:
                raise ValueError("Response JSON is missing required field: 'message'")

            post_info = re.match(
                r"Season (\d+), Episode (\d+), Frame (\d+)", data["message"]
            )
            if post_info:
                person["season"] = int(post_info.group(1))
                person["episode"] = int(post_info.group(2))
                person["frame"] = int(post_info.group(3))

            person["gif_start"] = person["frame"] - 10
            person["gif_end"] = person["frame"] + 40

        except httpx.RequestError as e:
            raise RuntimeError(f"Error connecting to Facebook API: {e}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HTTP error occurred: {e.response.status_code}, {e.response.text}"
            )

        return person

    def fetch_page_name_and_id(self) -> tuple:
        """
        Busca o nome e ID da página do Facebook.

        :return: Uma tupla contendo o nome e ID da página.
        """
        if self.token is None:
            raise ValueError("Facebook token not found")

        url = f"{self.base_url}/me"
        params = {"access_token": self.token}

        try:
            response = httpx.get(url, params=params, timeout=10)
            response.raise_for_status()  # Verifica erros de HTTP (status != 2xx)
            data = response.json()  # Converte a resposta para JSON

            if "id" not in data or "name" not in data:
                raise ValueError(
                    "Response JSON is missing required fields: 'id' or 'name'"
                )

            self.page_id = data["id"]
            self.page_name = data["name"]

            return self.page_name, self.page_id

        except httpx.RequestError as e:
            raise RuntimeError(f"Error connecting to Facebook API: {e}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HTTP error occurred: {e.response.status_code}, {e.response.text}"
            )

    def process_comments(self, comments):
        processed_data = []
        for comment in comments:
            data_comments = comment.get("comments", {}).get("data", [])

            for data_comment in data_comments:
                if (data_comment["id"] not in self.replied_ids) and data_comment[
                    "message"
                ].startswith("!"):
                    person = {
                        "person_name": data_comment.get("from", {}).get("name"),
                        "person_id": data_comment.get("from", {}).get("id"),
                        "comment_id": data_comment.get("id"),
                        "message": data_comment.get("message"),
                        "created_time": data_comment.get("created_time"),
                        "post_id": self.page_id
                        + "_"
                        + data_comment.get("id").split("_")[0],
                    }
                    for cmd in self.commands:
                        if data_comment.get("message").startswith(cmd):
                            person["cmd"] = cmd
                            break
                    processed_data.append(person)

        return processed_data

    def search_data(self):
        tries = 0
        max_retries = 1
        data = []
        params = {
            "fields": "comments.limit(100)",
            "limit": "100",
            "access_token": self.token,
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

                tries += 1
                time.sleep(3)

            except httpx.RequestError as e:
                logging.error(f"An error occurred: {e}\nRetrying...")
                tries += 1
                time.sleep(3)

        return data
