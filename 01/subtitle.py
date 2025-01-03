import subprocess
import os
import math

def subtitle(comment: dict) -> None:

        if 'subtitle' in comment and 'file_path' in comment and 'frame_number' in comment:
            subtitle = comment['subtitle']

            # break subtitle into lines 
            subtitle_partes = subtitle.split(' ')

            # Calculates the number of lines and adjusts the background size
            lines = math.ceil(len(subtitle_partes) / 5)
            backgound_size = f'0x{str(int(lines) * 120)}'

            # Inserts line breaks every 5 words, but avoids the last unnecessary line break
            subtitle_com_quebras = []
            for i in range(0, len(subtitle_partes), 5):
                subtitle_com_quebras.append(' '.join(subtitle_partes[i:i+5]))

            # Join the lines with '\n' so that the text is displayed correctly
            subtitle = '\n'.join(subtitle_com_quebras).strip()

            # parameters to the image magick
            file_path = comment['file_path']
            gravity = '-gravity'
            gravity_value = 'North'
            font = '-font'
            font_path = 'font/Cooper.otf'
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