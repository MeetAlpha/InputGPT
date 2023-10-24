import time
import db_handler as db
from datetime import datetime

class ConversationHandler:
    def __init__(self, history_table: str = None, system_msg: dict = None):
        if not history_table or not db.exist_table(history_table):  # New conversation
            # Create a new table
            self.history_table = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # '2023-10-21_21-50-00'
            db.create_table(self.history_table)
            self.conversation = []
            self.add_and_write(system_msg)
        else:  # Load from a history_table
            # TO DO: check data format
            self.conversation = db.read_from_table(history_table)
            self.history_table = history_table
            # Delete the old one, create a new one with current time, but is it necessary?
            # db.delete_table(history_table) 
            # self.history_table = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # '2023-10-21_21-50-00'
            # db.create_table(self.history_table)

    def add_and_write(self, msg: dict):
        self.conversation.append({'timestamp': int(time.time()), 'role': msg['role'], 'content': msg['content']})
        self.write_to_table()

    def write_to_table(self):
        db.write_to_table(self.history_table, self.conversation)

    def to_context(self):
        return [{'role': item['role'], 'content': item['content']} for item in self.conversation] 
