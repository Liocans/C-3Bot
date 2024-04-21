from modules.chatbot.chatbot import ChatBot
from utilities.path_finder import PathFinder

if __name__ == '__main__':
    path_to_model = PathFinder().get_complet_path('ressources/models/bow_lemmatizer.pth')
    chatbot = ChatBot(model_file=path_to_model)

    print("Let's chat! type 'quit' to exit.")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break
        response = chatbot.get_response(sentence)
        print("Bot:", response)
