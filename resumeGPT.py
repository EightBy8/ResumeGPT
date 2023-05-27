from dotenv import load_dotenv
import os
import openai
import wordwrap
import time

load_dotenv()

"""
    TODO:
          Add install file
          Add UI
          Add file searcher
          Add walk-through PD generator
          Add pros and cons format option
"""

class resumeGPT:
    """
    A class that interacts with the OpenAI GPT-3.5-turbo model to generate responses for a resume evaluation system.

    This class provides methods to set the position description (PD), set the resume, set additional context, and
    perform a chat-based evaluation of the resume. It utilizes the OpenAI API to generate responses.

    Attributes:
        openai_api_key (str): The OpenAI API key loaded from the environment variable OPENAI_API_KEY.
        pd (str): The position description (PD) for the resume evaluation.
        model (str): The name of the GPT model to use for generating responses.
        context (list): A list of conversation context messages used for the GPT model input.
        total_tokens: The total amount of tokens used in the session.

    Methods:
        get_response(convo): Sends a conversation to the GPT model and retrieves the generated response.
        set_context(text): Sets additional context for the conversation.
        set_pd(text): Sets the position description (PD).
        set_resume(text): Sets the resume for evaluation and retrieves the model's response.
        chat(text): Sends a user message to the model and retrieves the generated response.

    """

    def __init__(self, config=None):
        """
        Initializes the resumeGPT class.

        Args:
            config (dict): Configuration parameters for the class (default: None).
                           - pd: Position description.
                           - model: Model name.
                           - context: List of conversation context.

        """

        if config is None:
            config = {"pd": "",
                      "model": "gpt-3.5-turbo",
                      "context": [{"role": "system",
                                   "content": "You take in a position description and a resume and briefly explain how "
                                              "suited they are for the job and then give a rating 1-10 based on how "
                                              "qualified they are. You also value experience in a related field the "
                                              "most. Also the stated degree level is a minimum."},
                                  {"role": "user", "content": ""},  # 1 context
                                  {"role": "assistant", "content": "Ok I'll keep that in mind. "},
                                  {"role": "user", "content": ""},  # 3 Position Description
                                  {"role": "assistant", "content": "Ok next send the resume"},
                                  {"role": "user", "content": ""},  # 5 Resume
                                  ]
                      }
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.pd = config["pd"]
        self.model = config['model']
        self.context = config['context']
        self.total_tokens = 0

    def get_response(self, convo):
        """
        Sends a message to the OpenAI API and retrieves the model's response.

        Args:
            convo (list): List of messages for the conversation.

        Returns:
            str: The model's response.

        """

        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=convo,
            temperature=0.1,
        )
        self.total_tokens += response.usage.total_tokens
        print("Tokens:", response.usage.total_tokens)
        print("Total tokens:", self.total_tokens)
        content = response.choices[0].message.content
        content = wordwrap.fill(content)
        return content

    def set_context(self, text, update_response=False):
        """
        Sets the conversation context by adding user-provided text.

        Args:
            text (str): Text to add to the context.
            update_response (bool): Whether to return an updated response to the resume.

        Returns:
            str: Confirmation message or the updated response to the resume.

        """

        content = "Before I send the PD here's some context: " + text
        del self.context[6:]
        self.context[1]["content"] = content

        if update_response:
            response = self.get_response(self.context)
            return response
        return "Context updated.\n"

    def set_pd(self, text):
        """
        Sets the position description (PD).

        Args:
            text (str): Position description.

        Returns:
            str: Confirmation message.

        """

        del self.context[6:]
        self.context[3]["content"] = "Here is the position description:\n\n" + text
        return "PD updated.\n"

    def set_resume(self, text):
        """
        Sets the resume.

        Args:
            text (str): Resume content.

        Returns:
            str: Model's response to the resume.

        """

        del self.context[6:]
        self.context[5]["content"] = "Here is the resume:\n\n" + text
        retries = 3
        for attempt in range(retries):
            try:
                response = self.get_response(self.context)
            except openai.error.RateLimitError:
                print("Rate limit exceeded. Retrying in 5 seconds...\n")
                time.sleep(3)
                continue
            else:
                return response
        print("Sorry, the model is currently overloaded with other requests. Please try again later.")
        quit()

    def chat(self, text):
        """
        Initiates a chat interaction with the model.

        Args:
            text (str): User's message.

        Returns:
            str: Model's response.

        """

        self.context.append({"role": "user", "content": text})
        retries = 3
        for attempt in range(retries):
            try:
                response = self.get_response(self.context)
            except openai.error.RateLimitError:
                print("Rate limit exceeded. Retrying in 5 seconds...\n")
                time.sleep(3)
                continue
            else:
                return response
        print("Sorry, the model is currently overloaded with other requests. Please try again later.")
        quit()


def main():
    skip = False
    convo = resumeGPT()
    user = input("Would you like to add additional context? (text/No)\n").lower()

    if user == "c" or user == "chat":
        skip = True
        print("Going straight to chat.\n")
    elif user != 'n' and user != "no":
        _ = convo.set_context(user)
        print("Ok I'll keep that in mind.\n\n")
    else:
        print("No context set.\n\n")

    if not skip:
        directory = 'PositionDescription'
        filePath = os.listdir(directory)
        f = os.path.join(directory, filePath[0])
        if f.endswith('txt') or f.endswith('pdf'):
            text = open(f).read()
            _ = convo.set_pd(text)

        directory = 'Resumes'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if f.endswith('txt') or f.endswith('pdf'):
                text = open(f).read()
                review = convo.set_resume(text)
                print(review)
                print("\n\n")

    print("\nType 'help' for commands.")
    while True:
        user = input(">> ").lower().strip()

        if user == "set pd":
            pd_input = input("Please paste the PD:\n").strip()
            if pd_input.strip() != "":
                print(convo.set_pd(pd_input))
            else:
                print("PD cannot be empty.")
        elif user == "set resume":
            resume_input = input("Please paste the resume:\n").strip()
            if resume_input.strip() != "":
                print(convo.set_resume(resume_input))
            else:
                print("Resume cannot be empty.")
        elif user == "set context":
            context_input = input("Please enter the context:\n").strip()
            if context_input.strip() != "":
                update_response = False
                user = input("Would you like to update the response? (Yes/No)\n").lower().strip()
                if user == 'y' or user == 'yes':
                    update_response = True
                print(convo.set_context(context_input, update_response))
            else:
                print("Context cannot be empty.")
        elif user == "help":
            print("set pd: Sets the position description.")
            print("set resume: Input a new resume.")
            print("set context: Gives context for the job.")
            print("Quit: Exits the program.")
        elif user == "quit" or user == "q":
            print("Quitting program...\n")
            return
        else:
            print(convo.chat(user))


if __name__ == '__main__':
    main()
