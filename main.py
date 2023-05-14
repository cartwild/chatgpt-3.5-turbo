import openai
import telegram
# trunk-ignore(ruff/F401)
from telegram.ext import Updater, MessageHandler, Filters

# Set up OpenAI API key
# trunk-ignore(gitleaks/generic-api-key)
api_key = "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"
openai.api_key = api_key

# trunk-ignore(gitleaks/telegram-bot-api-token)
bot_token = "6074524630:AAHCIYZLfkDefkoNqFBcWKAiIdx0_-e8aO4"
bot = telegram.Bot(token=bot_token)

# Function to send a message to the OpenAI chatbot model and return its response


def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        # trunk-ignore(git-diff-check/error)
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        # The conversation history up to this point, as a list of dictionaries
        messages=message_log,
        # The maximum number of tokens (words or subwords) in the generated response
        max_tokens=3800,
        # The stopping sequence for the generated response, if any (not used here)
        stop=None,
        # The "creativity" of the generated response (higher temperature = more creative)
        temperature=0.7,
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


# Main function that runs the chatbot
def main():
    # Initialize the conversation history with a message from the chatbot
    # trunk-ignore(ruff/F841)
    message_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    # Set a flag to keep track of whether this is the first request in the conversation
    # trunk-ignore(ruff/F841)
    first_request = True

    # Start a loop that runs until the user types
