import os
import yaml
from .person import Person


class Configs:
    def __init__(self):
        self.configs_path     = os.path.join(os.path.dirname(__file__), '..', "configs.yaml")
        self.replied_ids_path = os.path.join(os.path.dirname(__file__), '..', "replied_ids.txt")

    # ------------------------ yaml configs -------------------------------- #
    def create_config(self) -> None:
        """Create an empty yaml file if it doesn't exist."""
        with open(self.configs_path, "w") as f:
            f.write("")
          
    def load_configs(self) -> dict:
        """Load the configs from the yaml file."""
        configs = {}
        if not os.path.exists(self.configs_path):
            self.create_yaml_config()
            return configs

        with open(self.configs_path, "r") as f:
            configs = yaml.safe_load(f)
        return configs

    def save_configs(self, configs) -> None:
        """Save the configs to the yaml file."""
        with open(self.configs_path, "w") as f:
            yaml.dump(configs, f)

    # ------------------------ replied ids -------------------------------- #
    def create_ids(self) -> None:
        """Create an empty txt file if it doesn't exist."""
        with open(self.replied_ids_path, "w") as f:
            f.write("")

    def load_ids(self) -> list:
        """Load the replied ids from the txt file."""
        ids = []
        if not os.path.exists(self.replied_ids_path):
            self.create_txt_ids()
            return ids

        with open(self.replied_ids_path, "r") as f:
            ids = f.read().splitlines()
        return ids

    def save_ids(self, new_ids: list) -> None:
        """Save the new replied ids to the txt file."""
        with open(self.replied_ids_path, "a") as f:
            for id in new_ids:
                    f.write(f"{id}\n")

    # ------------------------ filter -------------------------------- #
    def filter_ids(self, replied_ids, data_persons: list[Person]) -> list[Person]:
        return [person for person in data_persons if person.comment_id not in replied_ids]
    
