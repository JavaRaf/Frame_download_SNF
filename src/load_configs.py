from ruamel.yaml import YAML
from pathlib import Path

yaml: YAML = YAML()  # Criando a instância primeiro
yaml.preserve_quotes = True  # Configurando preserve_quotes separadamente
yaml.indent(mapping=2, sequence=4, offset=2)  # Corrigindo a indentação corretamente
yaml.default_flow_style = False


FILE_PATH = Path.cwd() / 'configs.yml'


def load_configs(FILE_PATH: Path) -> dict:
    if not FILE_PATH.exists():
        FILE_PATH.touch(exist_ok=True)
        return {}

    try:
        with open(FILE_PATH, "r") as file:
            return yaml.load(file)
    except Exception as e:
        print(f"Error while loading configs: {e}")
        return {}
