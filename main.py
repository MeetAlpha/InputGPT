from keyboard_listener import KeyBoardListener
import config_handler

def main():
    config = config_handler.load_config()
    listener = KeyBoardListener(**config)
    listener.run()

    

if __name__ == "__main__":
    main()
