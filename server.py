from flask import Flask, jsonify, request
from flask_cors import CORS
import textwrap
import os
import google.generativeai as genai
from googletrans import Translator
from markdown2 import markdown

os.environ['GOOGLE_API_KEY'] = "AIzaSyC45GYd0yo8AdIFPXsanZ17E6zYEmNCE8s"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

app = Flask(__name__)
translator = Translator()
CORS(app)

def to_markdown(text):
    
    text = text.replace('.', '*')
    indented_text = textwrap.indent(text, '> ')
    translated = translator.translate(indented_text, dest='si')
    translated_text = translated.text
    return markdown(translated_text)

@app.route('/data1', methods=['POST'])
def generate_and_translate():
    data = request.get_json()
    text = data['text']
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    translated_markdown = to_markdown(response.text)
    print(translated_markdown)
    return jsonify({'msg': translated_markdown})

if __name__ == "__main__":
    app.run(debug=True)
