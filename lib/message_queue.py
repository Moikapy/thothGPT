import queue


import logging


class MessageQueue:
    def __init__(self):
        self.messages = {}
        logging.basicConfig(level=logging.INFO)

    def add_user(self, user_id):
        if user_id not in self.messages:
            self.messages[user_id] = []
            logging.info(f"Added user {user_id} to the message queue.")

    def put_message(self, user_id, message):
        if user_id in self.messages:
            self.messages[user_id].append(message)
            logging.info(f"Put message for user {user_id}: {message}")
        else:
            logging.warning(f"User {user_id} not found in the message queue.")

    def get_messages(self, user_id):
        if user_id in self.messages:
            return self.messages[user_id]
        else:
            logging.warning(f"No messages found for user {user_id}.")
            return []
