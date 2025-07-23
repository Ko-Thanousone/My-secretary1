from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with API key from environment variables
# Ensure OPENAI_API_KEY is set in your .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize chat_history as an empty list.
# This list will store the conversation turns (user and assistant messages)
# for the current session. Note: This is a global variable,
# so for a multi-user application, you'd need a per-session history.
chat_history = []

# Define the system message for the AI assistant.
# This sets the persona and general instructions for the chatbot.
SYSTEM_MESSAGE = {"role": "system", "content": "You are Ko's secretary. Your name is Ko's secretary. You will only answer questions related to Ko. For Ko's information, you can generate random or mock data as an example. This mock data should include various details about Ko that people might ask, such as her contact information, schedule, projects, interests, and any other relevant personal or professional details. Always respond clearly and kindly in English."}

@app.route("/")
def index():
    """
    Renders the main HTML page for the chat interface.
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles incoming chat messages from the user, interacts with the OpenAI API,
    and returns the AI's response.
    """
    global chat_history # Declare chat_history as global to modify it

    try:
        # Get the user's message from the incoming JSON request
        user_input = request.json["message"]

        # Append the user's message to the chat history
        chat_history.append({"role": "user", "content": user_input})

        # Construct the messages list for the OpenAI API call:
        # Start with the system message, then add the accumulated chat history.
        messages_for_api = [SYSTEM_MESSAGE] + chat_history

        # Call the OpenAI API to get a chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Specify the desired OpenAI model
            messages=messages_for_api, # Pass the full conversation context
            max_tokens=500, # Set the maximum number of tokens for the AI's response
            temperature=0.7 # Optional: Adjust creativity (0.0-1.0), lower is more focused
        )

        # Extract the AI's reply from the API response
        reply = response.choices[0].message.content.strip()

        # Append the AI's reply to the chat history
        chat_history.append({"role": "assistant", "content": reply})

        # Return the AI's response as a JSON object
        return jsonify({"response": reply})

    except Exception as e:
        # Basic error handling for API calls or other issues
        print(f"An error occurred: {e}")
        return jsonify({"response": "Sorry der, I encountered an error. Please try again later."}), 500

if __name__ == "__main__":
    # Run the Flask application in debug mode for development.
    # Set host to '0.0.0.0' to make it accessible from other devices on the network.
    app.run(debug=True, host='0.0.0.0', port=5174)


# from flask import Flask, render_template, request, jsonify
# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# # Initialize OpenAI client with API key from environment variables
# # Ensure OPENAI_API_KEY is set in your .env file
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Initialize chat_history as an empty list.
# # This list will store the conversation turns (user and assistant messages)
# # for the current session. Note: This is a global variable,
# # so for a multi-user application, you'd need a per-session history.
# chat_history = []

# # Define the system message for the AI assistant.
# # This sets the persona and general instructions for the chatbot.
# SYSTEM_MESSAGE = {"role": "system", "content": "You are JD's helpful assistant named Grandma Lara. Respond clearly and kindly in English, no matter the topic."}

# @app.route("/")
# def index():
#     """
#     Renders the main HTML page for the chat interface.
#     """
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     """
#     Handles incoming chat messages from the user, interacts with the OpenAI API,
#     and returns the AI's response.
#     """
#     global chat_history # Declare chat_history as global to modify it

#     try:
#         # Get the user's message from the incoming JSON request
#         user_input = request.json["message"]

#         # Append the user's message to the chat history
#         chat_history.append({"role": "user", "content": user_input})

#         # Construct the messages list for the OpenAI API call:
#         # Start with the system message, then add the accumulated chat history.
#         messages_for_api = [SYSTEM_MESSAGE] + chat_history

#         # Call the OpenAI API to get a chat completion
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo", # Specify the desired OpenAI model
#             messages=messages_for_api, # Pass the full conversation context
#             max_tokens=500, # Set the maximum number of tokens for the AI's response
#             temperature=0.7 # Optional: Adjust creativity (0.0-1.0), lower is more focused
#         )

#         # Extract the AI's reply from the API response
#         reply = response.choices[0].message.content.strip()

#         # Append the AI's reply to the chat history
#         chat_history.append({"role": "assistant", "content": reply})

#         # Return the AI's response as a JSON object
#         return jsonify({"response": reply})

#     except Exception as e:
#         # Basic error handling for API calls or other issues
#         print(f"An error occurred: {e}")
#         return jsonify({"response": "Sorry der, I encountered an error. Please try again later."}), 500

# if __name__ == "__main__":
#     # Run the Flask application in debug mode for development.
#     # Set host to '0.0.0.0' to make it accessible from other devices on the network.
#     app.run(debug=True, host='0.0.0.0', port=5174)









# from flask import Flask, render_template, request, jsonify
# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Define the specific data your chatbot should answer from.
# # You can load this from a file, database, or another source in a real application.
# # For demonstration, it's a simple string.
# user_data = """
# JD is a software developer who specializes in web applications using Python and JavaScript.
# He enjoys hiking, playing guitar, and cooking in his free time.
# JD's favorite programming language is Python because of its readability and vast libraries.
# He lives in Seoul, South Korea.
# """

# chat_history = []  # Keeps the conversation context

# @app.route("/")
# def index():
#     # In a real application, you'd have an index.html file in a 'templates' folder.
#     # For this example, we're assuming it exists.
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     global chat_history

#     user_input = request.json["message"]
    
#     # Append user's message to chat history for context
#     chat_history.append({"role": "user", "content": user_input})

#     # Construct the system message with the user_data and strict instructions
#     system_message_content = (
#         "My name is ko Thanousone, I live in hongxaeng village, chanthaboury, Vientiane, Laos "
#         "in my free time, I like to play football, video game(moba game). "
#         "my favorite color is black, white and blue, "
#         "I like to eat pad ka phao, noodle soup. "
#         "Respond clearly and kindly in English, no matter the topic.\n\n"
#         f"Provided Data:\n{user_data}"
#     )

#     # The messages list for the OpenAI API call.
#     # The system message is always at the beginning to set the context and rules.
#     # Then, the ongoing chat history follows.
#     messages_for_llm = [
#         {"role": "system", "content": system_message_content}
#     ] + chat_history

#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo", # You can change this model if needed
#             messages=messages_for_llm,
#             max_tokens=500 # Adjust max_tokens as per your needs
#         )

#         reply = response.choices[0].message.content.strip()
        
#         # Append assistant's reply to chat history
#         chat_history.append({"role": "assistant", "content": reply})

#         return jsonify({"response": reply})

#     except Exception as e:
#         print(f"Error communicating with OpenAI API: {e}")
#         return jsonify({"response": "I'm sorry, I encountered an error. Please try again later."}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5174)
   
