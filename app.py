import os
import openai
from dotenv import load_dotenv # Add

import json
from flask import Flask, redirect, render_template, request, url_for,jsonify
import logging
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logfile.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
)

app = Flask(__name__)
load_dotenv() # Add

openai.api_key = os.environ["OPENAI_API_KEY"]


@app.route("/")
def index():
    return render_template('index.html')

# Define route to generate completions
@app.route('/generate_summary', methods=['GET', 'POST'])
def generate_summary():
    input_url = request.args.get('input_url') if request.method == 'GET' else request.form['input_url']
    prompt = "Please summarize this article : "+str(input_url)

    messages=[
        {"role": "user", "content": prompt},
    ]

     # Generate a completion with OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2500,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the generated text from the response
        result = response['choices'][0]['message']['content']

    except RateLimitError:
        result = "The server is experiencing a high volume of requests. Please try again later."    


    return jsonify(content=result)

# if __name__ == '__main__':
#     app.run(debug=True)       
