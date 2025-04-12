# save user ids that have been replied
def save_id(comment: dict, message: str) -> None:
    try:
        with open('replyed_ids.txt', 'a', encoding='utf-8') as file:
            file.write(f'{comment["id"]}\n')
            print(message, comment["id"], flush=True)
    except IOError:
        print(f"Erro ao salvar o ID {comment['id']} no arquivo", flush=True)



# used to handle already responded ids. Avoid duplications
def remove_replyed_ids(comments_list: list) -> None:
    if not comments_list:
        return
        
    try:
        with open('replyed_ids.txt', 'r', encoding='utf-8') as file:
            replyed_ids = set(file.read().splitlines())  # usando set para busca mais eficiente
            
            comments_list[:] = [comment for comment in comments_list 
                if comment.get('id') not in replyed_ids]
    
    except FileNotFoundError:
        with open('replyed_ids.txt', 'w', encoding='utf-8') as file:
            print("Arquivo replyed_ids.txt não encontrado\ncriando um", flush=True)