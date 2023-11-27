from flask import Flask, request, jsonify
import json
import os
import configparser
import pandas as pd
from datetime import datetime

from utils import classification, sqlInsert, num_tokens_from_string
from chatbot import Session


#### - Config
config = configparser.RawConfigParser()
config.read('azureConfig.env')

configDict = dict(config.items('assistant'))

os.environ["OPENAI_API_KEY"] = configDict['openai_api_key']
os.environ["OPENAI_API_TYPE"] = configDict['openai_api_type']
os.environ["OPENAI_API_VERSION"] = configDict['openai_api_version']
os.environ["OPENAI_API_BASE"] = configDict['openai_api_base']

#### - App
app = Flask(__name__)

'''
{
    "user_id": "A15",
    "question": "I will be taking leave from Oct 18 to 25"
}
'''


sessions = {}

@app.route('/greet', methods=['GET'])
def greet():
    return jsonify({'message': 'Hi, I am the TSD Assistant!'})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()


    user_id = data.get('user_id', None)
    if user_id is None:
        return jsonify({'error': 'user_id is required'}), 400
    
    if user_id not in sessions:
        sessions[user_id] = Session()

    session = sessions[user_id]

    question = data.get('question', None)
    if question is None:
        return jsonify({'error': 'question is required'}), 400

    chat_history = session.chat_history

    # prompt classification
    qClass, qClassScore = classification(question)

    if qClass == "diğer":
    
        return jsonify({'answer': 'Sadece yazılımla ilgili sorulara cevap verebilirim, diğer konularla ilgili size yardımcı olamam.',
                        "prompt_token":0,
                        "ai_token":0,})
    
    else:
        result = session.conversation({"question": question, "chat_history": chat_history})
        if not session.first_iteration:
            result = session.conversation({"question": question, "chat_history": chat_history})

        chat_history.append((question, result["text"]))
        session.chat_history = chat_history

        session.first_iteration = False

        prompt_token = num_tokens_from_string(question,"cl100k_base")
        ai_token = num_tokens_from_string(result["text"],"cl100k_base")

        # sql insert statement
        df = pd.DataFrame({"UserID": [user_id],
                            "ModelName":["gpt-35-turbo-16k"],
                            "UserPrompt":[question],
                            "AiPrompt":[result["text"]],
                            "UserPromptToken":[prompt_token],
                            "AiPromptToken":[ai_token],
                            "LogTarihi": [datetime.now()]})

        sqlInsert(df, "TSD_ASISTAN_LOG")

        response_data = {
            "answer": result["text"],
            "prompt_token":prompt_token,
            "ai_token":ai_token,
        }

        return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)