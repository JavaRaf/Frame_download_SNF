import httpx
import time
import os
import data



def get_messages_and_ids(response_data) -> list[dict]:
    """
    Obtém mensagens e IDs de comentários de uma página do Facebook.
    
    Args:
        response_data (list[dict]): Dados da resposta da API do Facebook
    
    Returns:
        list[dict]: Lista de comentários com suas informações associadas
    """
    messages_and_ids: list[dict] = []
    FILTERED_PREFIXES = ['Random Crop.', 'Subtitles:']  # Constante em maiúsculas
    
    for item in response_data:
        comment_data = item.get('comments', {}).get('data', [])
        for comment in comment_data:
            try:
                # Extrair dados em um dicionário separado para melhor legibilidade
                comment_info = {
                    'comment': comment.get('message'),
                    'id': comment.get('id'),
                    'created_time': comment.get('created_time'),
                    'person_name': comment.get('from', {}).get('name'),
                    'person_id': comment.get('from', {}).get('id')
                }
                
                if (comment_info['id'] and 
                    comment_info['comment'] and 
                    not any(comment_info['comment'].startswith(prefix) for prefix in FILTERED_PREFIXES)):
                    messages_and_ids.append(comment_info)
            except Exception as e:
                print(f"Erro ao processar comentário: {e}")
                continue
    
    return messages_and_ids

def get_comments() -> list[dict]:
    """
    Obtém comentários de uma página do Facebook.
    
    Returns:
        list[dict]: Lista de comentários com suas informações associadas
    """
    MAX_RETRIES = 6
    SLEEP_TIME = 3
    
    messages_and_ids = []
    params = {
        'fields': 'comments.limit(100)',
        'limit': '100',
        'access_token': data.FB_TOKEN
    }
    
    for retry in range(MAX_RETRIES):
        try:
            response = httpx.get(
                f'{data.fb_url}/{os.environ.get("PAGE_ID")}/posts',
                params=params,
                timeout=15
            )
            response.raise_for_status()  # Lança exceção para status codes não-200
            
            response_json = response.json()
            response_data = response_json.get('data', [])
            messages_and_ids.extend(get_messages_and_ids(response_data))
            
            # Verificar próxima página
            paging = response_json.get('paging', {})
            if not paging.get('next'):
                break
                
            params['after'] = paging['cursors']['after']
            
        except httpx.RequestError as e:
            print(f"Erro na requisição HTTP: {e}", flush=True)
        except Exception as e:
            print(f"Erro inesperado: {e}", flush=True)
        finally:
            time.sleep(SLEEP_TIME)
    
    print(f'Total de comentários coletados: {len(messages_and_ids)}', flush=True)
    return messages_and_ids


