from modules.configs import Configs
from modules.facebook import Facebook
from modules.commands import Commands
from modules.message import Message
from modules.images import Images
from modules.subtitles import Subtitles
from time import time, sleep


configs  = Configs()
facebook = Facebook()
commands_list = Commands()
messages = Message()
subtitles = Subtitles()
yaml_configs = configs.load_configs()

images = Images(yaml_configs.get("your_github_repo_url"))
replied_ids = configs.load_ids()
data_persons = configs.filter_ids(replied_ids, facebook.search_data())


def main():
    """
    Main function to run the bot. It iterates over the list of comments that start with "!"
    and checks if the command is valid. If it is, it calls the respective functions to
    download the frames, add the subtitle, compile the gif, add the message and upload the
    result to imgBB. Then it sends the result to the Facebook page and saves the new ids to
    the replied_ids list.

    :return: None
    """
    new_comment_ids = []
    commands = yaml_configs.get("commands")

    for person in data_persons:
        commands_list.check_command(commands, person)
        images.download_frames(person)
        subtitles.add_subtitle(person)


main()