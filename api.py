from flask import Flask, request, jsonify
import os
from openai import OpenAI
# import openai
import requests
from collections import OrderedDict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


rubric_criteria = """
Rubric Criteria:
    Criteria 1: Title of the given passage.
                Level 1: (1 Marks) Correct Title i.e., Relevant to the gist of the given passage with correct structure/mechanics. (Capitalization, Punctuation, Spelling, Grammar, etc.)
                Level 2: (0.5 Marks) Relevent but incompllete /incorrect structure.
                Level 3: (0 Marks) Wrong title i.e., Not relevent to the given passage.
    Criteria 2: Summary of the given passage. (Content and its organization)
                Level 1: (3 Marks) An excellent attempt with the most relevant content and organization, exhibiting logical transition across the body of the summary reflecting thorough grasp of the given text.
                Level 2: (2 Marks) Sustainable/sufficient attempt i.e. covering most of the parameters.
                Level 3: (1 Marks) Limited/mediocre attempt i.e. covering some of the parameters.
                Level 4: (0 Marks) Wrong answer.
    Criteria 3: Summary of the given passage. (use of language, expression, and length of the summary)
                Level 1: (2 Marks) An attempt which is grammatically and lexically correct to the maximum extent with the parameter of length preferably not exceeding half of the given passage.
                Level 2: (1 Marks) An attempt which covers the given parameters of content/expression to a sufficient extent
                Level 3: (0.5 Marks) An attempt with some aspects of the given parameters being met. 
                Level 4: (0 Marks) Flawed attempt.
 """

 
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Service Up and Running'})

@app.route('/get_txt', methods=['POST'])
def get_txt():
    try:
        # Expecting 'question' and 'answer' in the JSON data
        passage = request.json['passage']
        question = request.json['question']
        answer = request.json['answer']

        model_response = gpt_api(question, answer, passage)
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
        tot_m = float(res['Criteria 1']['Marks']) + float(res['Criteria 2']['Marks']) + float(res['Criteria 3']['Marks'])
        response = {'message': 'Evaluating Your answer based on the provided question and answer', 
                    'question': question, 'answer': answer, 'model_response': res, 'total_marks': tot_m}

        return jsonify(response), 200
    except KeyError:
        error_response = {'error': 'Please provide both "question" and "answer" parameters in the JSON data'}
        return jsonify(error_response), 400

def gpt_api(question, answer, passage):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Use the user's text as input to the GPT-3.5-turbo model
    chat_completion = client.chat.completions.create(
         model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Analyse the answer to the question based on the provided rubric, and assign a level from each criteria. Output should contain just the levels and their feedback for each criteria for example Criteria 1: , level: ,marks: , feedback: , Criteria 2: ,level: ,marks: , feedback: , Criteria 3: , level: ,marks: , feedback: "},
            {"role": "user", "content": "Passage: " + passage},
            {"role": "user", "content": "Question: " + question},
            {"role": "user", "content": "Answer: " + answer},
            {"role": "user", "content": "Marks: "  + "On the basis of the rubric criteria"},
            {"role": "user", "content": "Rubric Criteria: " + rubric_criteria}
        ]
    )

    # Analyse the answer to the question based on the provided rubric: '{question}'\n\nRubric: {rubric}. Assign a level\n\nAnswer: {answer}

    # Extract the model's response
    model_response = chat_completion.choices[0].message.content
    return model_response

def start_server():
    return app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


