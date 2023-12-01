from keyboard_listener import KeyBoardListener
import config_handler
from ai_model import AI

def main():
    rules = config_handler.load_rules()
    config = config_handler.load_config()
    ai_model = AI(**config)
    listener = KeyBoardListener(ai_model, rules)
    listener.run()


if __name__ == "__main__":
    main()
