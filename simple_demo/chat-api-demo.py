import openai
import configparser

class ChatGPTContextManager:
    def __init__(self):
        self.messages = [{"role": "system", "content": "A helpful assistant"}]
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
    # Role "user" : It means you, who is chatting or asking to chat gpt.
    # Role "assistant" : It means ChatGPT, who is answering your questions.
    # Role "system" : It means the system developer who can internally give some instructions for the conversation.

def load_config(filename='config.ini'):
    with open(filename, 'r') as file:
        print(file.read())
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        'api_key': config.get('default', 'api_key'),
        'address': config.get('default', 'address'),
        'temperature': config.getfloat('default', 'temperature'),
        'model': config.get('default', 'model')
    }

def main():
    config = load_config()
    openai.api_key = config['api_key']
    openai.api_base = config['address']
    chat_context = ChatGPTContextManager()
    
    while True:
        
        user_input = input("Your question: ")
        if (user_input == 'quit'):
            break
        
        # Add the current question to chat history list
        # You MUST send the ENTIRE chat history to API if you want it to respond based on the previous conversation.
        chat_context.add_message("user", user_input)
        
        # request the stream response, which is word by word, not response as a whole    
        response = openai.ChatCompletion.create(  
            model=config['model'],
            # Send the ENTIRE chat history
            messages = chat_context.messages,
            n = 1, # respond with only one answer
            temperature=config['temperature'],
            max_tokens=150,
            stream=True,
        )

        # collect the stream message so it prints like a type writer
        collected_messages = ''
        for chunk in response:
            chunk_message = ''
            if 'content' in chunk['choices'][0]['delta']:
                chunk_message = chunk['choices'][0]['delta']['content']  # extract the message
            collected_messages += chunk_message  # append the chunk
            print(chunk_message,end='')
        print('\n')
        chat_context.add_message("assistant", collected_messages)    

if __name__ == "__main__":
    main()
