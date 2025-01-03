import os
import re
import math
import subprocess



class ProcessData():
    
    @staticmethod
    def check_subtitle(person) -> bool:
        subtitle = re.findall(r'-t\s*(.*)', person['message'])
        if subtitle:
            person['subtitle'] = subtitle[0]
            return True  
        return False
    
    @staticmethod
    def add_subtitle(person):

        subtitle = person['subtitle']

        # break subtitle into lines 
        subtitle_partes = subtitle.split(' ')
        back_spaces = str.count(subtitle, '\\n') # get the number of '\\n' characters in the subtitle

        # Calculates the number of lines and adjusts the background size
        

        lines = math.ceil(len(subtitle_partes) / 5)
        backgound_size = f'0x{str(int(lines + back_spaces) * 120)}' # calculate the number of lines and adjust the background size

        # Inserts line breaks every 5 words, but avoids the last unnecessary line break
        subtitle_com_quebras = []
        for i in range(0, len(subtitle_partes), 5):
            subtitle_com_quebras.append(' '.join(subtitle_partes[i:i+5]))

        # Join the lines with '\n' so that the text is displayed correctly
        subtitle = '\n'.join(subtitle_com_quebras).strip()

        # parameters to the image magick
        file_path = person['file_path']
        gravity = '-gravity'
        gravity_value = 'North'
        font = '-font'
        font_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'font', 'Cooper.otf')).replace('\\', '/'))
        font_size = '-pointsize'
        font_size_value = '100'
        background_color = '-background'
        background_color_value = 'White'
        splice = '-splice'
        splice_value = backgound_size
        annotate = '-annotate'
        annotate_position = '+0+20'
        output_name = file_path
        image_magick_command = 'magick' if os.name == 'nt' else 'convert' #  magick to windows || convert to linux

        command = [
            image_magick_command,  
            file_path,
            gravity, gravity_value,
            background_color, background_color_value,
            splice, splice_value,
            font, font_path,
            font_size, font_size_value,
            annotate, annotate_position,
            subtitle,
            output_name
        ]

        try:
            # Run the image magick command
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ocorreu um erro ao executar o comando: {e}")
       
    
    @staticmethod
    def check_episode_frame(person) -> bool:
        episode = re.findall(r'-e\s*(\d+)', person['message'])
        frame = re.findall(r'-f\s*(\d+)', person['message'])
        if episode and frame:
            person['episode'] = int(episode[0])
            person['frame']   = int(frame[0])

            return True
        else:
            return False


    @staticmethod
    def check_gif_params(person):
        gif_number = re.findall(r"\d+", person['message'])

        if gif_number:
            person['gif_start'] = int(gif_number[0]) - 10
            person['gif_end']   = int(gif_number[0]) + 40

            return True
        else:
            return False

        
    @staticmethod
    def add_help_message(person):
        person['response_message'] = 'Available commands'
        person['file_path'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', 'help.png'))
        




    