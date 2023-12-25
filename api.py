from flask import Flask, request, jsonify
import os
from openai import OpenAI
import requests

app = Flask(__name__)

@app.route('/get_text', methods=['POST'])
def get_text():
    if request.method == 'POST':
        try:
            user_text = request.json['text']

            model_response = gpt_api(user_text)

            response = {'message': 'Text received successfully', 'user_text': user_text, 'model_response': model_response}
            return jsonify(response), 200
        except KeyError:
            error_response = {'error': 'Please provide the "text" parameter in the JSON data'}
            return jsonify(error_response), 400
    else:
        error_response = {'error': 'Invalid request method. Use POST.'}
        return jsonify(error_response), 405

def gpt_api(user_text):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Use the user's text as input to the GPT-3.5-turbo model
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": user_text},
        ],
        model="gpt-3.5-turbo",
    )
    
    # Extract the model's response
    model_response = chat_completion.choices[0].message.content
    return model_response

os.environ['OPENAI_API_KEY'] = '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'

if __name__ == '__main__':

    app.run(debug=True)/get_text


