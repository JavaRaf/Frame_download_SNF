import re
import os
from Comments import Facebook

class FinderCommands():

    def get_gif_props(self, person):

        gif_number = re.search(r'-f\s*(\d+)', person.get('message'))

        if gif_number:
            if gif_number.group(1) - 10 > 0:
                person['gif_start'] = gif_number.group(1) - 10
                person['gif_end']   = gif_number.group(1) + 40
            else:
                person['gif_start'] = 1
                person['gif_end']   = 50

            return person
        
        post_infos = re.findall(r'\d+', self.facebook.get_post_infos(person.get('post_id')))
        if post_infos:
            if  int(post_infos[2]) - 10 > 0:
                person['gif_start'] = int(post_infos[2]) - 10
                person['gif_end'] = int(post_infos[2])   + 40
            else:
                person['gif_start'] = 1
                person['gif_end']   = 50
        else:
            raise ValueError("Não foi possível encontrar as informações do GIF nos dados fornecidos.")
        
        return person

    def computer_vote(self, person):
        person['response_message'] = self.configs.get('vote_message', '')
        return person

    def add_help_message(self, person):
        person['response_message']  = self.configs.get('help_message', '')
        person['help_filepath']     = os.path.join(os.path.dirname(__file__), 'images',  'help.png')
        return person  

    def get_post_infos(self, person):
        try:
            message = person.get('message', '')

            # Captura de informações usando expressões regulares com validação
            subtitle = re.search(r'-t\s*(.*)', message)
            season = re.search(r'-s\s*(\d+)', message)
            episode = re.search(r'-e\s*(\d+)', message)
            frame_number = re.search(r'-f\s*(\d+)', message)

            # Atualizando os campos somente se houverem valores válidos
            if subtitle:
                person['subtitle'] = subtitle.group(1)

            if season and episode and frame_number:
                person['season']    = int(season.group(1))
                person['episode']   = int(episode.group(1))
                person['frame']     = int(frame_number.group(1))

            # Verificando informações complementares, se disponíveis
            if 'season' not in person or 'episode' not in person or 'frame' not in person:
                post_infos = self.facebook.get_post_infos(person.get('post_id'))
                if post_infos:
                    match = re.match(r"Season (\d+), Episode (\d+), Frame (\d+) out of (\d+)", post_infos)
                    if match:
                        person['season']        = int(match.group(1))
                        person['episode']       = int(match.group(2))
                        person['frame']         = int(match.group(3))
                        person['total_frames']  = int(match.group(4))

            return person
        except Exception as e:
            print(f"Erro ao processar informações: {e}")

    def get_commands(self, person):
        message = person.get('message', '').replace(' ', '').lower()

        if self.download == message:
            self.get_post_infos(person)
        elif self.gif == message:
            self.get_gif_props(person)           
        elif self.help == message:
            self.add_help_message(person)
        elif self.vote == message:
            self.computer_vote(person)



            

