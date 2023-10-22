import pyperclip
from pynput.keyboard import Key, Controller, Listener
from ai_model import AI


class KeyBoardListener:
    def __init__(self, ai_model):
        self.keyboard = Controller()
        self.command_name = ';name'
        self.command_clipboard = ';clipboard'
        self.command_respond = ';respond'
        self.input_buffer = ''
        self.buffer_max_size = 50
        self.ai_model = ai_model

    def on_key_release(self, key):
        # If input_buffer is too long, clear it to save checking time
        if len(self.input_buffer) > self.buffer_max_size:
            self.input_buffer = self.input_buffer[-self.buffer_max_size:]

        try:
            # detect character typed，put to current_input
            self.input_buffer += key.char
        except AttributeError: # Some keys have no char, ignore
            pass
        except TypeError: # Some keys may be None, ignore
            pass
        
        # check if command in current_input
        if self.command_name in self.input_buffer:
            self.replace_command_with_text(self.command_name,"Name is Alice")
        elif self.command_clipboard in self.input_buffer:
            clipboard_content = pyperclip.paste()
            self.replace_command_with_text(self.command_clipboard,clipboard_content)
        elif self.command_respond in self.input_buffer:
            self.delete_last_n_characters(len(self.command_respond))
            clipboard_content = pyperclip.paste()
            # call GPT model to respond
            self.ai_model.respond('',clipboard_content,self.keyboard)
            self.input_buffer = ''

    
    def replace_command_with_text(self,command,text):
        self.delete_last_n_characters(len(command))
        self.keyboard.type(text)
        # clear input
        self.input_buffer = ''

    
    def delete_last_n_characters(self, n):
        # Send backspaces to delete the last n characters
        for _ in range(n):
            self.keyboard.press(Key.backspace)
            self.keyboard.release(Key.backspace)

    def run(self):
        with Listener(on_release=self.on_key_release) as listener:
            print("Listnening Keyboard...")
            listener.join()
