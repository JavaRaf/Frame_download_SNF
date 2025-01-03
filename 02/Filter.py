import os


class Ids:

    def __init__(self):
        self.ids_filepath = os.path.join(os.path.dirname(__file__), 'replied_ids.txt')
        self.replied_ids = []

    def get_replied_ids(self):
        if not os.path.exists(self.ids_filepath):
            with open(self.ids_filepath, 'w') as file:
                print('Replied ids file created successfully')
                self.replied_ids = []

        with open(self.ids_filepath, 'r', encoding='utf-8') as file:
            self.replied_ids = file.read().splitlines()

    def filter_ids_and_messages(self, data):
        filtered_data = []

        for person in data:
            if person.get('comment_id', '') not in self.replied_ids and \
            person.get('message', '').replace(' ', '').startswith('!'):
                
                filtered_data.append(person)

        return filtered_data

    def save_id(self, comment_id):
        with open(self.ids_filepath, 'a', encoding='utf-8') as file:
            file.write(f'{comment_id}\n')
             
    def filter(self, data):
        self.get_replied_ids()
        filtered_data = self.filter_ids_and_messages(data)

        return filtered_data
        


