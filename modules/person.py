from dataclasses import dataclass, field


@dataclass
class Person:
    person_name: str = ""
    person_id: str = ""
    comment_id: str = ""
    post_id: str = ""
    message: str = ""
    created_time: str = ""
    command: str = ""
    file_path: str = ""
    parameter: str = ""
    subtitle: str = ""
    season: int = 0
    episode: int = 0
    frames: list[int] = field(default_factory=list)
