from modules.chatbot.chatbot import ChatBot
from utilities.path_finder import PathFinder

if __name__ == '__main__':
    chatbot = ChatBot(model_file="bert_intent_classificator")

    print("Let's chat! type 'quit' to exit.")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break
        response = chatbot.get_response(sentence)
        print("Bot:", response)
