import datetime
from pynput.keyboard import Key, Controller, Listener

# type :date, and replace it to the date today
class DateReplacer:
    keyboard = Controller()
    # command to detect
    command = ':date'
    # current input
    current_input = ''

    def on_key_release(self, key):
        try:
            # detect character typed，put to current_input
            self.current_input += key.char
        except AttributeError:
            pass

        # check if command in current_input
        if self.command in self.current_input:
            # del the len of command (using backspace here)
            for _ in range(len(self.command)):
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
            # write the current date
            self.keyboard.type("Today is " + datetime.datetime.now().strftime('%Y-%m-%d'))
            # clear input
            self.current_input = ''

        # If input is too long, only keep the last part to save checking time
        if len(self.current_input) > len(self.command) + 50:
            self.current_input = self.current_input[-len(self.command)-50:]
    
    def run(self):
        with Listener(on_release=self.on_key_release) as listener:
            print("Listnening Keyboard...")
            listener.join()

if __name__ == '__main__':
    replacer = DateReplacer()
    replacer.run()
    
