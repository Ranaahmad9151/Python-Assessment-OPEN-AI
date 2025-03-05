import openai
import os
import time
from flask import Flask, request, jsonify

# Set OpenAI API Key (Do not hardcode API keys in production)
openai.api_key = "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"  # Replace with actual API key

class ChatGPTBotAPI:
    def __init__(self):
        self.prompts = []

    def create_prompt(self, prompt):
        self.prompts.append(prompt)
        return len(self.prompts) - 1  # Return index

    def get_response(self, prompt_index):
        """Fetch response from OpenAI API"""
        if 0 <= prompt_index < len(self.prompts):
            prompt = self.prompts[prompt_index]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response["choices"][0]["message"]["content"]
            except openai.error.RateLimitError:
                print("Rate limit exceeded. Retrying in 10 seconds...")
                time.sleep(10)  # Wait before retrying
                return "Rate limit exceeded. Try again later."

        return "Invalid prompt index"

    def update_prompt(self, prompt_index, new_prompt):
        if 0 <= prompt_index < len(self.prompts):
            self.prompts[prompt_index] = new_prompt
            return True
        return False

    def delete_prompt(self, prompt_index):
        if 0 <= prompt_index < len(self.prompts):
            del self.prompts[prompt_index]
            return True
        return False

# Initialize chatbot instance
chatbot = ChatGPTBotAPI()

# Initialize Flask app
app = Flask(__name__)

@app.route("/create_prompt", methods=["POST"])
def create_prompt():
    data = request.get_json()
    prompt = data.get("prompt")
    if prompt:
        prompt_index = chatbot.create_prompt(prompt)
        return jsonify({"message": "Prompt created", "index": prompt_index})
    return jsonify({"error": "Invalid input"}), 400

@app.route("/get_response/<int:prompt_index>", methods=["GET"])
def get_chatbot_response(prompt_index):
    response = chatbot.get_response(prompt_index)
    return jsonify({"response": response})

@app.route("/update_prompt/<int:prompt_index>", methods=["PUT"])
def update_prompt(prompt_index):
    data = request.get_json()
    new_prompt = data.get("new_prompt")
    if new_prompt and chatbot.update_prompt(prompt_index, new_prompt):
        return jsonify({"message": "Prompt updated"})
    return jsonify({"error": "Invalid index or input"}), 400

@app.route("/delete_prompt/<int:prompt_index>", methods=["DELETE"])
def delete_prompt(prompt_index):
    if chatbot.delete_prompt(prompt_index):
        return jsonify({"message": "Prompt deleted"})
    return jsonify({"error": "Invalid index"}), 400

if __name__ == "__main__":
    app.run(debug=True)
