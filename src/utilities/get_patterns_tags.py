import json

from utilities.path_finder import PathFinder

if __name__ == '__main__':
    file_path = PathFinder().get_complet_path(path_to_file='ressources/json_files/intents.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        intents_data = json.load(file)

    for intent in intents_data["intents"]:
        for text in intent["patterns"]:
            print('{ "user_input": "' + text + '", "tag": "' + intent["tag"] + '" },')
