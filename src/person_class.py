from dataclasses import dataclass
from typing import Optional
from dataclasses import field



@dataclass
class Person:
    # Campos obrigatórios da postagem
    post_message: str
    post_id: str

    # Informações da pessoa que comentou
    person_name: str
    person_id: str
    comment: str
    comment_id: str
    created_time: str 

    # Informações extras que podem ser extraídas
    season: Optional[int] = field(default=None)
    episode: Optional[int] = field(default=None)
    frame: Optional[int] = field(default=None)