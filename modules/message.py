from .person import Person

class Message:
    def __init__(self):
        self.help_message = (
            "Para ver os comandos, digite !help or !h\n",
            "Para baixar o gif, digite !gif or !g\n",
            "Para votar, digite !vote or !v\n",
        )

        self.download_message = (
            "Para baixar o gif, digite !gif or !g\n",
        )


    def customize_message(self,  person: Person):
        pass
    

    def help_message(self, person: Person):
        person.response_message = self.help_message
        pass