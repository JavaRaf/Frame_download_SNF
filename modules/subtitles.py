import os
import re
import subprocess
from .person import Person


class Subtitles:
    def __init__(self):
        pass

    def format_subtitle_lines(self, text: str) -> str:
        """Divide o texto em linhas com no máximo 5 palavras."""
        words = text.split(" ")
        lines = [" ".join(words[i:i + 5]) for i in range(0, len(words), 5)]
        return "\n".join(lines).strip()

    def extract_subtitle(self, person: Person):
        """Extrai a legenda do comando na mensagem."""
        subtitle_match = re.findall(r"-t\s*(.*)", person.message)
        if subtitle_match:
            person.subtitle = self.format_subtitle_lines(subtitle_match[0])

    def add_subtitle(self, person: Person):
        """Adiciona a legenda às imagens."""
        if person.parameter == "-t":
            self.extract_subtitle(person)

            if not person.subtitle:
                print("Nenhuma legenda encontrada.")
                return

            # Define o tamanho do fundo para acomodar a legenda
            background_size = "0x" + f"{int(person.subtitle.count('\n') + 1) * 125}"
            image_magick_command = "magick" if os.name == "nt" else "convert"

            # Caminho da fonte
            font_dir = os.path.abspath(
                os.path.join(
                os.path.dirname(__file__),
                "..",
                "font"
                )
            )
            font = os.path.join(font_dir, os.listdir(font_dir)[0]).replace("\\", "/")


            # Itera sobre os frames
            for idx, frame in enumerate(sorted(os.listdir(person.file_path))):
                file_path = os.path.join(person.file_path, frame)

                if not os.path.isfile(file_path):
                    print(f"Arquivo não encontrado: {file_path}")
                    continue

                self.run_image_magick(
                    image_magick_command, file_path, person.subtitle, background_size, font
                )

    def run_image_magick(self, image_magick_command: str, file_path: str, subtitle: str, background_size: str, font: str):
        """Executa o comando ImageMagick para adicionar legenda."""
        command = [
            image_magick_command,
            file_path,
            "-gravity", "North",
            "-background", "White",
            "-splice", background_size,
            "-font", font,
            "-pointsize", "100",
            "-annotate", "+0+30",
            subtitle,
            file_path,
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ocorreu um erro ao executar o comando: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")