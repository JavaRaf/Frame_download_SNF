from yaml import safe_load, safe_dump
import os


class OpenFiles:

    def __init__(self, config_filepath, ids_filepath, votes_filepath):
        self.config_path = config_filepath
        self.ids_filepath = ids_filepath
        self.votes_filepath = votes_filepath

        self.configs = self.load_configs()
        self.ids = self.load_ids()

    def load_configs(self):
        """Load the configurations from a YAML file."""
        try:
            if self.config_path:
                with open(self.config_path, "r") as file:
                    return safe_load(file)
        except FileNotFoundError:
            print(f"Arquivo {self.config_path} não encontrado\n Um será criado.")
            with open(self.config_path, "w") as file:
                defaults = {"commands": ["!dl", "!gif", "!help"]}
                safe_dump(defaults, file)
                return defaults

    def load_ids(self):
        """Load the configurations from a YAML file."""
        try:
            if self.ids_filepath:
                with open(self.ids_filepath, "r", encoding="utf-8") as file:
                    return file.read().splitlines()
        except FileNotFoundError:
            print(f"Arquivo {self.ids_filepath} não encontrado.\n Um será criado.")
            with open(self.ids_filepath, "w") as file:
                return []

    def save_ids(self, ids: list):
        """Save the ids on finalization."""
        with open(self.ids_filepath, "a", encoding="utf-8") as file:
            for id in ids:
                if id not in self.ids:
                    file.write(f"{id}\n")

    def save_votes(self, data):
        with open(self.votes_filepath, "w") as f:
            safe_dump(data, f)

    def increment_vote(self, id):
        # Verifica se o arquivo existe e carrega os dados, se não cria estrutura vazia
        if os.path.exists(self.votes_filepath):
            with open(self.votes_filepath, "r") as f:
                data = safe_load(f) or {}
        else:
            data = {}

        # Garante que a estrutura de votos exista
        if "votes" not in data:
            data["votes"] = []

        # Busca pelo ID na lista
        for item in data["votes"]:
            if id in item:
                item[id] += 1
                break
        else:
            # Adiciona um novo dicionário à lista se o ID não existir
            data["votes"].append({id: 1})

        # Salva os dados no arquivo
        self.save_votes(data)
