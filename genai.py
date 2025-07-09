import google.generativeai as genai 
from dotenv import load_dotenv
import os

load_dotenv() 

genai.configure(api_key=os.getenv('API_KEY')) 
model = genai.GenerativeModel('gemini-1.5-flash')

def gemini(contexto):
    response = model.generate_content(f'Gere ...{contexto}')
    return response.text
