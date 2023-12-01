import pyperclip
from pynput.keyboard import Key, Controller, Listener
from ai_model import AI


class KeyBoardListener:
    def __init__(self, ai_model, rules):
        self.keyboard = Controller()
        self.rules = rules
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
            print(f'key_pressed...: {key.char}')
        except AttributeError: # Some keys have no char, ignore
            pass
        except TypeError: # Some keys may be None, ignore
            pass
        

        matched_rule_idx = self.match(self.input_buffer, self.rules)
        if matched_rule_idx == -1: # No match
            return
        matched_rule = self.rules[matched_rule_idx]
        if matched_rule['type'] == 'prompt':  # Matched GPT prompt
            print('shortcut prompt matched')
            self.delete_last_n_characters(len(matched_rule['shortcut']))
            clipboard_content = pyperclip.paste() # Get clipboard content
            # call GPT model to respond with prompt and clipoard content
            self.ai_model.respond(f"{matched_rule['prompt']} ",clipboard_content,self.keyboard)
            self.input_buffer = ''
        elif matched_rule['type'] == 'replace': # Matched simple text replacement
            self.replace_command_with_text(matched_rule['shortcut'], matched_rule['text'])
        else:
            raise Exception('Rules error.')
            

    def match(self, input: str, rules: list):
        for i in range(len(rules)):
            if rules[i]['shortcut'] in input:
                return i
        return -1

    def replace_command_with_text(self, command, text):
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

    
