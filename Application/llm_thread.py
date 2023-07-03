from PySide6.QtCore import QThread, Signal
import tiktoken
import openai

from Application import constants


class LLMThread(QThread):
    result_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, messages):
        super().__init__()
        self.messages = messages
        self.gpt_model = constants.GPT3_5_TURBO

    def run(self):
        if self.messages:
            num_tokens = self.num_tokens_from_messages()
            if num_tokens >= constants.GPT3_TURBO_MAX_TOKENS:
                try:
                    self.summarize_conversation()
                except Exception as e:
                    return

            try:
                response = openai.ChatCompletion.create(
                    model=constants.GPT3_5_TURBO,
                    messages=self.messages,
                    max_tokens=150
                )
                # print(response)
                self.result_signal.emit(response['choices'][0]['message']['content'])
            except openai.OpenAIError as e:
                self.error_signal.emit(str(e))

    def num_tokens_from_messages(self):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(self.gpt_model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted

        # elif model == "gpt-4-0314":
        # tokens_per_message = 3
        # tokens_per_name = 1

        num_tokens = 0
        for message in self.messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        print(num_tokens)
        return num_tokens

    def summarize_conversation(self):
        num_messages = self.messages.length
        num_messages_to_summarize = num_messages / 4
        messages_to_summarize = self.messages[:num_messages_to_summarize]
        messages_to_summarize.append({"role": "system", "content": constants.CONVERSATION_SUMMARY})

        try:
            response = openai.ChatCompletion.create(
                model=constants.GPT3_5_TURBO,
                messages=messages_to_summarize,
                max_tokens=150
            )
            summary = response['choices'][0]['message']['content']
            print(summary)
        except openai.OpenAIError as e:
            self.error_signal.emit(str(e))
