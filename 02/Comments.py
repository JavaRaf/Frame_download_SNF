import httpx
import time
import os
import yaml


class Facebook:
    def __init__(self):
        self.page_id = ""
        self.token = os.environ.get("FB_TOKEN")
        self.configs_path = os.path.join(os.path.dirname(__file__), "Configs.yaml")
        self.configs = self.get_configs()
        self.version = self.configs["facebook_api_version"]
        self.base_url = f"https://graph.facebook.com/{self.version}"
        self.check_fb_token()

    def get_configs(self) -> dict:
        try:
            with open(self.configs_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("Arquivo Configs.yaml não encontrado\ncriando um")
            with open(self.configs_path, "w") as file:
                defaults = {"facebook_page_name": "", "facebook_api_version": "v21.0"}
                yaml.dump(defaults, file)
                return defaults

    def check_fb_token(self) -> str:
        """
        Check if the page_name matches with the FB token
        Returns:
            str: page_name
        """
        url = f"{self.base_url}/me?access_token={self.token}"
        response = httpx.get(url, timeout=10)
        if response.status_code == 200:
            self.page_id = response.json().get("id")
            page_name = response.json().get("name")

            if page_name == self.configs.get("facebook_page_name"):
                return page_name
            else:
                raise Exception(
                    "\n"
                    "your page token dont match with your current page name\n"
                    "Please get a new page token and try again"
                )

    def process_data(self, data):

        data_user = []

        for comment in data:
            comment_data = comment.get("comments", {}).get("data", [])

            if comment_data:
                for comment in comment_data:

                    person_name = comment.get("from", {}).get("name")
                    person_id = comment.get("from", {}).get("id")
                    comment_id = comment.get("id")
                    message = comment.get("message")
                    created_time = comment.get("created_time")
                    post_id = self.page_id + "_" + comment_id.split("_")[0]

                    data_user.append(
                        {
                            "person_name": person_name,
                            "person_id": person_id,
                            "comment_id": comment_id,
                            "message": message,
                            "created_time": created_time,
                            "post_id": post_id,
                        }
                    )
        return data_user

    def get_post_infos(self, post_id):
        url = f"{self.base_url}/{post_id}"
        response = httpx.get(url, params={"access_token": self.token}, timeout=10)
        if response.status_code == 200:
            return response.json()["message"]

    def get_fb_data(self) -> list:

        data = []
        tries = 0
        retries = 1
        params = {
            "fields": "comments.limit(100)",
            "limit": "100",
            "access_token": self.token,
        }
        while tries < retries:

            try:

                response = httpx.get(
                    f"{self.base_url}/me/posts", params=params, timeout=15
                )

                if response.status_code == 200:
                    response_data = response.json()

                    data.extend(self.process_data(response_data.get("data", [])))

                if not "next" in response_data.get("paging", {}):
                    break

                after = (
                    response_data.get("paging", {})
                    .get("cursors", {})
                    .get("after", None)
                )
                params.update(after=after)

                tries += 1
                time.sleep(3)

            except Exception as e:
                print(f"An error occurred: {e}\n. Retrying...")
                tries += 1
                time.sleep(3)

        return data
