from Comments import Facebook
from Filter import Ids
from Commands import FinderCommands

fb = Facebook()
ids = Ids()
cmd = FinderCommands(fb)


def main():

    fb_data = fb.get_fb_data()
    filtered_data = ids.filter(fb_data)

    for person in filtered_data:
        cmd.get_commands(person)
        print(person)


if __name__ == "__main__":
    main()
