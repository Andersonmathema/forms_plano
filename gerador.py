import google.generativeai as genai 
from dotenv import load_dotenv
import os

load_dotenv() 

genai.configure(api_key=os.getenv('API_KEY_GEMINI')) 
model = genai.GenerativeModel('gemini-2.5-flash')

def gemini_ativi(contexto):
    response = model.generate_content(f'''Gere em poucas linhas um contexto de {contexto},
                                       para colocar num plano de aula na parte Atividades
                                       desenvolvidas. Não formate o texto com markdowns,
                                       só retorne o pequeno texto limpo.''')
    return response.text


def gemini_estrat(contexto):
    response = model.generate_content(f'''Gere em poucas linhas um contexto de {contexto},
                                       para colocar num plano de aula na parte de Estratégias
                                       com uso de metodologia ativa, incluindo alunos elegíveis
                                       e se possível DUA. Não formate o texto com markdowns,
                                       só retorne o pequeno texto limpo.''')
    return response.text


def gemini_rec(contexto):
    response = model.generate_content(f'''Gere em poucas linhas um contexto de {contexto},
                                       para colocar num plano de aula na parte de recuperação
                                       com adaptação/flexibilização de instrumentos de avaliação
                                       incluindo alunos elegíveis.Não formate o texto com 
                                       markdowns, só retorne o pequeno texto limpo.''')
    return response.text


def openai_ativi(contexto):
    response = model.generate_content(f'''Gere em poucas linhas um contexto de {contexto},
                                       para colocar num plano de aula na parte Atividades
                                       desenvolvidas. Não formate o texto com markdowns,
                                       só retorne o pequeno texto limpo.''')
    return response.text


def openai_estrat(contexto):
    response = model.generate_content(f'''Gere em poucas linhas um contexto de {contexto},
                                       para colocar num plano de aula na parte de Estratégias
                                       com uso de metodologia ativa, incluindo alunos elegíveis
                                       e se possível DUA. Não formate o texto com markdowns,
                                       só retorne o pequeno texto limpo.''')
    return response.text


def openai_rec(contexto):
    response = model.generate_content(f'''Gere em poucas linhas um contexto de {contexto},
                                       para colocar num plano de aula na parte de recuperação
                                       com adaptação/flexibilização de instrumentos de avaliação
                                       incluindo alunos elegíveis.Não formate o texto com 
                                       markdowns, só retorne o pequeno texto limpo.''')
    return response.text