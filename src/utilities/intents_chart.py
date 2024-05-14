import json
import matplotlib.pyplot as plt
import pandas
import pandas as pd

from utilities.path_finder import PathFinder


# Load the intents JSON file
def load_intents(file_path: str) -> dict:
    """
    Loads intents data from a specified JSON file.

    Parameters:
        file_path (str): The path to the JSON file containing intent data.

    Returns:
        dict: A dictionary containing the loaded intents data.
    """

    file_path = PathFinder.get_complet_path(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def count_patterns_responses(intents_data: dict) -> pandas.DataFrame:
    """
    Counts the number of patterns and responses for each tag in the intents data.

    Parameters:
        intents_data (dict): The intents data loaded from a JSON file.

    Returns:
        pandas.DataFrame: A DataFrame containing the counts of patterns and responses per tag.
    """

    tags = []
    pattern_counts = []
    response_counts = []

    for intent in intents_data['intents']:
        tags.append(intent['tag'])
        pattern_counts.append(len(intent['patterns']))
        response_counts.append(len(intent['responses']))

    return pd.DataFrame({'Tag': tags, 'Pattern Count': pattern_counts, 'Response Count': response_counts})


# Plot patterns per tag in a separate chart
def plot_patterns(data_frame: pandas.DataFrame) -> None:
    """
    Plots the number of patterns per tag.

    Parameters:
        data_frame (pandas.DataFrame): A DataFrame containing the counts of patterns and responses per tag.
    """

    plt.figure(figsize=(10, 8))
    bars = plt.bar(data_frame['Tag'], data_frame['Pattern Count'], color='skyblue')
    plt.title('Number of Patterns per Tag')
    plt.xlabel('Tags')
    plt.ylabel('Number of Patterns')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom')
    plt.xticks(rotation=90)
    plt.tight_layout()


# Plot responses per tag in a separate chart
def plot_responses(data_frame: pandas.DataFrame) -> None:
    """
    Plots the number of responses per tag.

    Parameters:
        data_frame (pandas.DataFrame): A DataFrame containing the counts of patterns and responses per tag.
    """

    plt.figure(figsize=(10, 9))
    bars = plt.bar(data_frame['Tag'], data_frame['Response Count'], color='lightgreen')
    plt.title('Number of Responses per Tag')
    plt.xlabel('Tags')
    plt.ylabel('Number of Responses')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom')
    plt.xticks(rotation=90)
    plt.tight_layout()


if __name__ == '__main__':
    # Assuming the intents file is located at 'ressources/json_files/intents.json'
    intents_data = load_intents('ressources/json_files/intents.json')
    df = count_patterns_responses(intents_data)

    # Call the plot functions
    plot_patterns(df)
    plot_responses(df)
    plt.show()
