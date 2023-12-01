from openai import OpenAI
from conversation_handler import ConversationHandler
class AI:
    def __init__(self, api_key, address, temperature=1.0, model='gpt-3.5-turbo', system_role='A helpful assistant', history_table=None):
        self.api_key = api_key
        self.address = address
        self.temperature = temperature
        self.model = model
        # openai.api_key = api_key
        # openai.api_base = address
        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key = api_key,
            base_url = address
        )
        self.conversation_handler = ConversationHandler(history_table, {"role": "system", "content": system_role})
        self.context = self.conversation_handler.to_context()
    
    def respond(self, command: str, content: str, keyboard):
        # Add the current question to chat history list
        # You MUST send the ENTIRE chat history to API if you want it to respond based on the previous conversation.
        user_msg = {"role": "user", "content": command + content}
        self.context.append(user_msg)
        self.conversation_handler.add_and_write(user_msg)
        # request the stream response, which is word by word, not response as a whole
        # response = openai.ChatCompletion.create(
        response = self.client.chat.completions.create(
            model = self.model,
            # Send the ENTIRE chat history
            messages = self.context,
            n = 1, # respond with only one answer
            temperature=self.temperature,
            # max_tokens=150,
            stream=True,
        )

        # collect the stream message so it prints like a type writer
        collected_response = ''
        for chunk in response:
            # delta = chunk["choices"][0]["delta"]
            delta = chunk.choices[0].delta
            # msg = delta.get("content", "")  # extract the message
            msg = delta.content if delta.content else ''
            collected_response += msg  # append the chunk
            print(msg,end='')
            keyboard.type(msg)  # type each chunk
        print('\n')
        assist_msg = {"role": "assistant", "content": collected_response}
        self.context.append(assist_msg)
        self.conversation_handler.add_and_write(assist_msg) # Add message and write to db file
