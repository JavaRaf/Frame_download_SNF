import user
from make_gif import run_make_gif
from imgBB import imgBB
from facebook import post_fb, publish_fb
from save_ids import save_id
from subtitle import subtitle

# module that deals with responding to commands and sending them to Facebook and saving the ids

def response(comment: dict) -> None:

    if (comment.get('file_path') and comment.get('id')) or (comment.get('message', '').lower() == user.str_command_help.lower()):

        if user.str_command_gif.lower() in comment.get('comment', '').lower():
            run_make_gif(comment)
        
        if user.str_command_download.lower() in comment.get('comment', '').lower():
            subtitle(comment)
            imgBB(comment)
        
        
        post_fb(comment)
        publish_fb(comment)
        save_id(comment, 'Comentário respondido e id salvo: ')

