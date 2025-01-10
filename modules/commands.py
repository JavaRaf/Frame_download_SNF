from .person import Person



class Commands:

    def check_command(self, commands: list[list[str]], person: Person):
        for command_group in commands:
            for command in command_group:
                if command in person.message.replace(" ", "").lower():
                    person.command = command_group[0]
                    self.parameter_check(person)



    def parameter_check(self, person: Person):
        parameters = ["-f", "-t"]

        for parameter in parameters:
            if parameter in person.message.replace(" ", "").lower():
                person.parameter = parameter



