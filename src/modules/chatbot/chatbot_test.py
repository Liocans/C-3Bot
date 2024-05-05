import json

import torch

from modules.chatbot.chatbot import ChatBot
from utilities.path_finder import PathFinder


def test_chatbot(mode_filename: str) -> None:
    file_path = PathFinder().get_complet_path(f"ressources/models/{mode_filename}.pth")
    intent_test_path = PathFinder().get_complet_path(f"ressources/json_files/chatbot_intent_test.json")
    result_test_path = PathFinder().get_complet_path(f"ressources/json_files/chatbot_test_result.json")

    score_known_data = 0
    score_unknown_data = 0
    data = torch.load(file_path)
    chatbot = ChatBot(model_file=file_path)
    result = {
        'modeling': data["modeling_name"],
        'preprocessing': data["preprocessor"],
        'extractor': data["extractor"],
        'stopword': data["remove_stopwords"],
        'epochs': data["num_epochs"],
        'batch_size': data["batch_size"],
        'learning_rate': data["learning_rate"],
        'hidden_size': data["hidden_size"],
        'score_known_data': "",
        'score_unknown_data': ""
    }

    with open(intent_test_path, 'r', encoding='utf-8') as file:
        intent_test_data = json.load(file)

    with open(result_test_path, 'r', encoding='utf-8') as result_file:
        existing_results = json.load(result_file)

    for known_data in intent_test_data["known_data"]:
        if chatbot.predict_tag(known_data["user_input"]) == known_data["tag"]:
            score_known_data += 1

    result["score_known_data"] = f"{round((score_known_data / len(intent_test_data["known_data"])) * 100, 2)} %"

    for unknown_data in intent_test_data["unknown_data"]:
        if (chatbot.predict_tag(unknown_data["user_input"]) == unknown_data["tag"]):
            score_unknown_data += 1

    result["score_unknown_data"] = f"{round((score_unknown_data / len(intent_test_data["unknown_data"])) * 100, 2)} %"

    with open(result_test_path, "w+", encoding='utf-8') as result_file:
        existing_results["tests"].insert(0, result)
        json.dump(existing_results, result_file, indent=4)
