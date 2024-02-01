from flask import Flask, request, jsonify
import os
from openai import OpenAI
# import openai
import requests
from collections import OrderedDict
from flask_cors import CORS
import criteria

app = Flask(__name__)
CORS(app)

# rubric_criteria = None
 
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Service Up and Running'})

@app.route('/get_txt', methods=['POST'])
def get_txt():
    try:
        # Expecting 'question' and 'answer' in the JSON data
        rubric_criteria = None
        passage = request.json['passage']
        question = request.json['question']
        answer = request.json['answer']
        questionid = request.json['questionid']

        if questionid == "i":
            rubric_criteria = criteria.rubric_criteria_2i
        elif questionid == "ii":
            rubric_criteria = criteria.rubric_criteria_2ii
        elif questionid == "iii":
            rubric_criteria = criteria.rubric_criteria_2iii
        else:
            print("no option")
        

        model_response = gpt_api(question, answer, passage,rubric_criteria)
        splitted = model_response.split('\n\n')
        res = {}
        tot_m = []
        try :
            for i in range(0, len(splitted)):
                txt = splitted[i].split('\n')
                res[txt[0].split(':')[0]] = {}
                res[txt[0].split(':')[0]]['Level'] = txt[1].split(':')[1].strip()
                res[txt[0].split(':')[0]]['Marks'] = txt[2].split(':')[1].strip()
                res[txt[0].split(':')[0]]['Feedback'] = txt[3].split(':')[1].strip()

        except IndexError:
            pass
        
        response_len = len(res)
        if response_len == 1:
            tot_m = float(res['Criteria 1']['Marks'])
        elif response_len == 3:
            tot_m = float(res['Criteria 1']['Marks']) + float(res['Criteria 2']['Marks']) + float(res['Criteria 3']['Marks'])

        response = {'question': question, 'answer': answer, 'model_response': res, 'total_marks': tot_m}

        return jsonify(response), 200
    except KeyError:
        error_response = {'error': 'Please provide both "question" and "answer" parameters in the JSON data'}
        return jsonify(error_response), 400

def gpt_api(question, answer, passage, rubric_criteria):
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    client = OpenAI(api_key="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")

    # Use the user's text as input to the GPT-3.5-turbo model
    chat_completion = client.chat.completions.create(
         model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Analyse the answer to the question based on the provided rubric, and assign a level from each criteria. Output should contain just the levels and their feedback for each criteria for example Criteria 1: , level: ,marks: , feedback: "},
            {"role": "user", "content": "Passage: " + passage},
            {"role": "user", "content": "Question: " + question},
            {"role": "user", "content": "Answer: " + answer},
            {"role": "user", "content": "Marks: "  + "On the basis of the rubric criteria"},
            {"role": "user", "content": "Rubric Criteria: " + rubric_criteria}
        ]
    )

    # Extract the model's response
    model_response = chat_completion.choices[0].message.content
    return model_response

def start_server():
    return app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


