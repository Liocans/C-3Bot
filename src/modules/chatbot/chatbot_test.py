import json
import os

import torch

from modules.chatbot.chatbot import ChatBot
from utilities.path_finder import PathFinder


def test_chatbot(model_filename: str) -> None:
    """
    Tests a ChatBot model with predefined input data for known and unknown intents
    and writes the test results to a JSON file.

    This function retrieves paths for model resources and JSON files using `PathFinder`.
    It then initializes a `ChatBot` instance with the specified model file. Depending
    on the model's file structure, configuration parameters are loaded either from a
    JSON file within a directory (if the model is stored in a directory) or directly
    from a model data file (if the model is stored in a file).

    The test involves scoring the ChatBot's ability to correctly predict intent tags
    for known and unknown data sets. These scores are then written back to a JSON file
    that aggregates test results.

    Parameters:
    - model_filename (str): The filename of the model to test. This is used to locate
      the actual model file and its associated configuration.

    Raises:
    - FileNotFoundError: If the model file or any necessary JSON files are not found.
    - Exception: For errors that occur during file reading or writing.

    Outputs:
    - No direct output, but updates a JSON file with the test results and prints a message
      upon completion of the test.
    """

    file_path = PathFinder().get_complet_path(f"ressources/models/{model_filename}")
    intent_test_path = PathFinder().get_complet_path(f"ressources/json_files/chatbot_intent_test.json")
    result_test_path = PathFinder().get_complet_path(f"ressources/json_files/chatbot_test_result.json")

    score_known_data = 0
    score_unknown_data = 0
    chatbot = ChatBot(model_file=model_filename)
    if os.path.isdir(file_path):
        config_path = file_path + "/config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)

            result = {
                'modeling': config["model_type"],
                'preprocessing': "None",
                'extractor': "BERT",
                'stopword': "None",
                'epochs': config["num_epochs"],
                'batch_size': config["batch_size"],
                'learning_rate': config["learning_rate"],
                'hidden_size': "None",
                'score_known_data': "",
                'score_unknown_data': ""
            }
    else:
        data = torch.load(file_path)
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

    print(f"Test done for the model {model_filename}")