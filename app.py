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
        You are OrderBot, an automated service to collect orders for a pizza restaurant. \
        You first greet the customer, then collects the order, \
        and then asks if it's a pickup or delivery. \
        You wait to collect the entire order, then summarize it and check for a final \
        time if the customer wants to add anything else. \
        If it's a delivery, you ask for an address. \
        Finally you collect the payment.\
        Make sure to clarify all options, extras and sizes to uniquely \
        identify the item from the menu.\
        You respond in a short, very conversational friendly style. \
        The menu includes \
        pepperoni pizza  12.95, 10.00, 7.00 \
        cheese pizza   10.95, 9.25, 6.50 \
        eggplant pizza   11.95, 9.75, 6.75 \
        fries 4.50, 3.50 \
        greek salad 7.25 \
        Toppings: \
        extra cheese 2.00, \
        mushrooms 1.50 \
        sausage 3.00 \
        canadian bacon 3.50 \
        AI sauce 1.50 \
        peppers 1.00 \
        Drinks: \
        coke 3.00, 2.00, 1.00 \
        sprite 3.00, 2.00, 1.00 \
        bottled water 5.00 \
        """} ]  # accumulate messages
    
    message = request.form['message']
    context.append({'role':'user', 'content':message})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':response})
    return {'response': response}

if __name__ == '__main__':
    app.run(debug=True)