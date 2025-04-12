from pathlib import Path
from src.person_class import Person

FILE_PATH = Path.cwd() / 'seen_ids.txt'


def save_id(person: Person) -> None:
    """
    Save the comment ID to the seen_ids.txt file.

    If the file does not exist, it is created. The comment ID is appended to
    the file with a newline character.
    """
    if not FILE_PATH.exists():
        FILE_PATH.write_text("", encoding='utf-8')
    
    with FILE_PATH.open("a", encoding="utf-8") as file:
        file.write(f'{person.comment_id}\n')
        print(
            f'Comment from person {person.person_name}',
            f'Id: {person.comment_id} replied', flush=True)
    

def remove_seen_comments(persons: list[Person]) -> list[Person]:
    """
    Remove comments that have already been responded to.

    This function reads the seen_ids.txt file and checks if the comment_id
    of each person is in the file. If it is, the person is not added to the
    filtered list.

    Args:
        persons (list[Person]): A list of Person objects.

    Returns:
        list[Person]: A filtered list of Person objects.
    """
    if not FILE_PATH.exists():
        FILE_PATH.write_text("", encoding='utf-8')

    seen_ids = set(FILE_PATH.read_text(encoding='utf-8').splitlines())

    filtered_persons = [
        person for person in persons
        if person.comment_id not in seen_ids
    ]
    return filtered_persons
