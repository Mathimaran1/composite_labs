import openai
from flask import Flask, request, jsonify

# Set the API base URL and your API key
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = "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"

# Conversation setup
conversation_history = [
    {"role": "system", "content": "You are an expert on Composite Labs and Monad. Focus only on those topics."}
]

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Composite Labs and Monad chatbot API. Use the /chat endpoint to interact with the bot."

@app.route("/chat", methods=["POST"])
def chatbot():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Add user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Call the OpenAI API for chat completion with llama-3.3-70b-versatile
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",  # Use a Llama model
            messages=conversation_history,
            temperature=0.5,
            max_tokens=256,
            top_p=1.0
        )

        # Extract and send the assistant's response
        assistant_message = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return jsonify({"response": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
