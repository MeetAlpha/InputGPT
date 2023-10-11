import openai
class AI:
    def __init__(self, api_key, address, temperature, model, system_role):
        self.api_key = api_key
        self.address = address
        self.temperature = temperature
        self.model = model
        self.context = [{"role": "system", "content": system_role}]
        openai.api_key = api_key
        openai.api_base = address
    
    def respond(self,command: str, content: str, keyboard):
        # Add the current question to chat history list
        # You MUST send the ENTIRE chat history to API if you want it to respond based on the previous conversation.
        self.context.append({"role": "user", "content": command + content})
        
        # request the stream response, which is word by word, not response as a whole
        response = openai.ChatCompletion.create(  
            model = self.model,
            # Send the ENTIRE chat history
            messages = self.context,
            n = 1, # respond with only one answer
            temperature=self.temperature,
            max_tokens=150,
            stream=True,
        )

        # collect the stream message so it prints like a type writer
        collected_response = ''
        for chunk in response:
            delta = chunk["choices"][0]["delta"]
            msg = delta.get("content", "")  # extract the message
            collected_response += msg  # append the chunk
            print(msg,end='')
            keyboard.type(msg)  # type each chunk
        self.context.append({"role": "assistant", "content": collected_response})
