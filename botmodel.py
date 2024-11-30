import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('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')

# Initialize conversation history
conversation_history = [
    {
        "role": "system",
        "content": (
            "Welcome to the claims department. Your role as a claims agent is to assist customers. "
            "Your primary goal is to provide empathetic and professional support to our customers throughout the claims process. "
            "We want you to engage with our customers in a friendly and authentic manner, and avoid using standardized or cliché phrases. "
            "Please take the time to listen actively to our customers, provide clear explanations, and be yourself. "
            "Remember, every customer is unique, and their situation requires a personalized approach. "
            "Strive to create the best customer experience possible. "
            "If the customer asks you any question other than insurance-related, just refuse to answer and say you can only answer questions related to insurance."
        )
    }
]

# Validate if user input is insurance-related
def validate_content(content):
    try:
        messages = [{"role": "user", "content": f'Is this question related to insurance? "{content}". Return result True or False only.'}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages
        )
        return response["choices"][0]["message"]["content"].strip()
    except  openai.OpenAIError as e:
        return f"Error validating content: {str(e)}"

# Summarize the conversation
def conversation_summary(content):
    try:
        messages = [{"role": "user", "content": f"Summarize this conversation array: {content}"}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages
        )
        return response["choices"][0]["message"]["content"].strip()
    except openai.OpenAIError as e:
        return f"Error summarizing conversation: {str(e)}"

# Main function to handle conversations
def run_conversation(content):
    global conversation_history
    print(f"User Input: {content}")

    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": content})
    print("Current Conversation History:", conversation_history)

    try:
        # Get GPT response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        # Extract GPT's reply
        response_message = response["choices"][0]["message"]["content"].strip()
        print("GPT Response:", response_message)

        # Add GPT response to conversation history
        conversation_history.append({"role": "assistant", "content": response_message})
        return response_message
    except openai.AuthenticationError:
        return "Error: Invalid API key. Please check your OpenAI API key."
    except openai.RateLimitError:
        return "Error: Rate limit exceeded. Please try again later."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Main interaction loop
def main():
    print("Chatbot: Welcome! Ask me questions related to insurance. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        # Validate if the input is insurance-related
        validation_result = validate_content(user_input)
        if validation_result.lower() == "true":
            # Run the conversation if valid
            bot_reply = run_conversation(user_input)
            print(f"Chatbot: {bot_reply}")
        else:
            print("Chatbot: I can only answer questions related to insurance.")

# Entry point
if __name__ == "__main__":
    main()





