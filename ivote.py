import yaml


def add_vote(comment: dict) -> str:
    try:
        # Tenta carregar o arquivo YAML
        try:
            with open('frame_votes.yaml', 'r', encoding='utf-8') as file:
                votes = yaml.safe_load(file) or {}
        except FileNotFoundError:
            # Cria o arquivo vazio se ele não existir
            votes = {}

        # Obtém season, episode e frame do comentário
        season = comment['season']
        episode = comment['episode']
        frame = comment['frame_number']

        # Constrói a estrutura de votação
        key = f"season {season}, episode {episode}, frame {frame}"
        if key in votes:
            votes[key]['votes'] += 1
        else:
            votes[key] = {'votes': 1}

        # Salva novamente no arquivo YAML
        with open('frame_votes.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(votes, file)

        return f"{votes[key]['votes']}"

    except Exception as e:
        return f"Erro ao salvar o voto: {e}"

