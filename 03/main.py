# imports ---------------------------------------------------------------------------------------------
import os
from scripts import Facebook
from scripts import OpenFiles
from scripts import ProcessData
from scripts import DownloadImg
# -----------------------------------------------------------------------------------------------------


# Arquivos de configuração e ids respondidos ----------------------------------------------------------
configs_filepath  = os.path.join(os.path.dirname(__file__), 'configs.yaml')
ids_filepath      = os.path.join(os.path.dirname(__file__), 'replied_ids.txt')
votes_filepath    = os.path.join(os.path.dirname(__file__), 'fb', 'votes.yaml')
# -----------------------------------------------------------------------------------------------------
token    = 'EAAPqUmuoddwBOZBYmgq0d9VeJYIKWDxUDfqULHBvHE0ylqmlg2IZCf7AyU7rNzgr4ThKqaQvA8qqcW2dA35I9voEMdbXBVnvohrynmdDdS4C80BHTQw4dnfmdXWBCkEu2IOpTdYiLKOPG3fI2bn1PGSzv17SHPAii4SO3MmDAz3hkcpUklNBNRgpUvQaYZD'
fb_token = token or os.getenv('FB_TOKEN') # set FB_TOKEN for test, or default token if not set
# -----------------------------------------------------------------------------------------------------

# instantiate Classes ---------------------------------------------------------------------------------
open     = OpenFiles(configs_filepath, ids_filepath, votes_filepath) 
facebook = Facebook(fb_token, open.ids, open.configs['commands'])
process  = ProcessData()
github   = DownloadImg(**{
    'repo_owner':   open.configs['repo_owner'],
    'repo':         open.configs['repo'],
    'branch':       open.configs['branch'],
    'frames':       open.configs['frames']
})



# main function ---------------------------------------------------------------------------------------

def main():
    
    fb_data = facebook.search_data()
    
    for person in fb_data:
        if person['cmd'] == open.configs['commands'][0]:      # !dl
            if process.check_episode_frame(person) == False:
                facebook.fetch_post_info(person)
            github.download_frame(person, person['frame'])

            if process.check_subtitle(person) == True:
                process.add_subtitle(person)

            
        elif person['cmd'] == open.configs['commands'][1]:    # !gif
            if process.check_gif_params(person) == False:
                facebook.fetch_post_info(person)        
            github.get_gif_frames(person)


        elif person['cmd'] == open.configs['commands'][2]:    # !vote
            facebook.fetch_post_info(person)
            vote_id = f'season({person['season']}) ({person['episode']}), frame({person["frame"]})'
            open.increment_vote(vote_id)


        elif person['cmd'] == open.configs['commands'][3]:    # !help
            process.add_help_message(person)


        else:
            process.add_help_message(person)
    
    
if __name__ == '__main__':
    main()
# -----------------------------------------------------------------------------------------------------