import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) # read local .env file

openai.organization = "org-Ju24Bfv0d8D7PHiH9INX976p"
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    context = [ {'role':'system', 'content':"""
    You are a chatbot from Fractal Company. Your service is to collect queries related to Fractal Company only. If the query is not related to Fractal Company, say 'no data found'. \
    First, greet the client and ask for their query related to Fractal Company. \
    Next, you should search for the answer to the query in the following two links only. \
    https://fractal.ai/ fractalofficial site. \
    https://en.wikipedia.org/wiki/Fractal_Analytics. \
    If the answer to the query is not found in these two links, say 'no data found'. \
    """} ]# accumulate messages
    
    message = request.form['message']
    context.append({'role':'user', 'content':message})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':response})
    return {'response': response}

if __name__ == '__main__':
    app.run(debug=True)
