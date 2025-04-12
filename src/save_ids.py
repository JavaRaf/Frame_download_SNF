from pathlib import Path
from src.comments import Person

FILE_PATH = Path.cwd() / 'seen_ids.txt'


def save_id(person: Person) -> None:
    """
    Salva o ID do comentário no arquivo seen_ids.txt.
    """
    if not FILE_PATH.exists():
        FILE_PATH.write_text("", encoding='utf-8')
    
    with FILE_PATH.open("a", encoding="utf-8") as file:
        file.write(f"{person.comment_id}\n")
        print(f"ID {person.comment_id} salvo", flush=True)


def remove_seen_comments(persons: list[Person]) -> list[Person]:
    """
    Remove comentários que já foram respondidos.
    """
    if not FILE_PATH.exists():
        FILE_PATH.write_text("", encoding='utf-8')

    seen_ids = set(FILE_PATH.read_text(encoding='utf-8').splitlines())

    filtered = [
        person for person in persons
        if person.comment_id not in seen_ids
    ]
    return filtered
